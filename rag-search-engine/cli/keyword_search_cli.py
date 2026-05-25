import argparse
import json
import string
import os
import pickle
import sys
import math
from collections import Counter
from nltk.stem import PorterStemmer

def process_text(text: str, stopwords: set[str]) -> list[str]:
    translator = str.maketrans('', '', string.punctuation)
    normalized = text.lower().translate(translator)
    tokens = normalized.split()
    stemmer = PorterStemmer()
    return [stemmer.stem(t) for t in tokens if t and t not in stopwords]

BM25_K1 = 1.5
BM25_B = 0.75

class InvertedIndex:
    def __init__(self, stopwords: set[str]):
        self.index: dict[str, set[int]] = {}
        self.docmap: dict[int, dict] = {}
        self.stopwords = stopwords
        self.term_frequencies: dict[int, Counter] = {}
        # New attribute for length normalization
        self.doc_lengths = {} 
        self.stopwords = stopwords

    def bm25(self, doc_id: int, term: str) -> float:
        """Calculate the combined BM25 score for a single term and document."""
        tf_score = self.get_bm25_tf(doc_id, term)
        idf_score = self.get_bm25_idf(term)
        return tf_score * idf_score

    def bm25_search(self, query: str, limit: int) -> list[tuple[int, float]]:
        """Rank documents based on the sum of BM25 scores for all query tokens."""
        # Process the query into stemmed tokens
        query_tokens = process_text(query, self.stopwords)
        scores = {}

        # Calculate scores for every document in the collection
        for doc_id in self.docmap:
            total_score = 0.0
            for token in query_tokens:
                # Use the token directly since it's already processed
                # Note: get_bm25_tf/idf internally process text, so ensure 
                # consistency or pass the raw token if your methods allow.
                try:
                    total_score += self.bm25(doc_id, token)
                except:
                    # Handle cases where a token might result in 0 tokens after processing
                    continue
            scores[doc_id] = total_score

        # Sort by score descending and return the top results
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_docs[:limit]

    def __get_avg_doc_length(self) -> float:
        """Helper to calculate average length across the dataset."""
        return 0.0 if (not self.doc_lengths) else (sum(self.doc_lengths.values()) / len(self.doc_lengths))

    def get_bm25_tf(self, doc_id:int, term:str, k1:float=BM25_K1, b:float = BM25_B):
        """Calculate the saturated and length-normalized TF score."""
        tf = self.get_tf(doc_id, term)
        
        # 1. Calculate the normalization factor
        avg_len = self.__get_avg_doc_length()
        doc_len = self.doc_lengths.get(doc_id, 0)
        
        # length_norm = 1 - b + b * (doc_length / avg_doc_length)
        length_norm = (1 - b) + (b * (doc_len / avg_len))
        
        # 2. Apply to the saturation formula
        # tf_component = (tf * (k1 + 1)) / (tf + k1 * length_norm)
        return (tf * (k1 + 1)) / (tf + k1 * length_norm)

    def get_bm25_idf(self, term: str) -> float:
        # 1. Tokenize and validate the input term
        tokens = process_text(term, self.stopwords)
        if len(tokens) != 1:
            raise Exception("term must be a single token")
        
        target_token = tokens[0]
        
        # 2. Identify N (total docs) and df (doc frequency)
        N = len(self.docmap)
        df = len(self.index.get(target_token, set()))
        
        # 3. Apply the BM25 IDF formula with Laplace smoothing
        # Formula: log((N - df + 0.5) / (df + 0.5) + 1)
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
        
        return idf

    def __add_document(self, doc_id: int, text: str):
        tokens = process_text(text, self.stopwords)
        # Track the document length (token count)
        self.doc_lengths[doc_id] = len(tokens) 
        self.term_frequencies[doc_id] = Counter(tokens)
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def get_tf(self, doc_id: int, term: str) -> int:
        tokens = process_text(term, self.stopwords)
        if len(tokens) != 1:
            raise Exception("term must be a single token")
        
        token = tokens[0]
        # Return frequency from Counter, default to 0
        doc_counts = self.term_frequencies.get(doc_id, Counter())
        return doc_counts.get(token, 0)

    def get_documents(self, term: str) -> list[int]:
        # Perform O(1) lookup on the index dictionary[cite: 1, 3]
        doc_ids = self.index.get(term, set())
        return sorted(list(doc_ids))

    def build(self, movies: list[dict]):
        for movie in movies:
            doc_id = movie["id"]
            self.docmap[doc_id] = movie
            full_text = f"{movie['title']} {movie['description']}"
            self.__add_document(doc_id, full_text)

    #                                             index_abs_path, docmap_abs_path, frequencies_abs_path, doc_lengths_abs_path
    def save(self, base_dir = "cache",  pickle_files=["index.pkl", "docmap.pkl", "term_frequencies.pkl", "doc_lengths.pkl"]):
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        paths = [ f"{base_dir}/{pickle_file}" for pickle_file in pickle_files ]
        
        with open(paths[0], "rb") as f: self.index = pickle.load(f)
        with open(paths[1], "rb") as f: self.docmap = pickle.load(f)
        with open(paths[2], "rb") as f: self.term_frequencies = pickle.load(f)
        with open(paths[3], "rb") as f: self.doc_lengths = pickle.load(f)

    #                                             index_abs_path, docmap_abs_path, frequencies_abs_path, doc_lengths_abs_path
    def load(self, base_dir="cache", pickle_files=["index.pkl", "docmap.pkl", "term_frequencies.pkl", "doc_lengths.pkl"]):
        paths = [ f"{base_dir}/{pickle_file}" for pickle_file in pickle_files ]

        if not all(os.path.exists(p) for p in paths):
            raise IOError("Index files not found. Run 'build' first.")
        
        # Manually assign each loaded file to the correct attribute
        with open(paths[0], "rb") as f: self.index = pickle.load(f)
        with open(paths[1], "rb") as f: self.docmap = pickle.load(f)
        with open(paths[2], "rb") as f: self.term_frequencies = pickle.load(f)
        with open(paths[3], "rb") as f: self.doc_lengths = pickle.load(f)

def main() -> None:
    def bm25_tf_command(doc_id, term, k1, b, inv_index):
        """Loads the index and returns the saturated TF score."""
        inv_index.load()
        return inv_index.get_bm25_tf(doc_id, term, k1, b)

    def bm25_idf_command(term: str, inv_index: InvertedIndex) -> float:
        inv_index.load()
        return inv_index.get_bm25_idf(term)

    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search movies")
    search_parser.add_argument("query", type=str, help="Search query")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build index")

    # New TF command
    tf_parser = subparsers.add_parser("tf", help="Get term frequency")
    tf_parser.add_argument("doc_id", type=int, help="Document ID")
    tf_parser.add_argument("term", type=str, help="Term to count")

    # New IDF command
    idf_parser = subparsers.add_parser("idf", help="Get inverse document frequency")
    idf_parser.add_argument("term", type=str, help="Term to calculate IDF for")

    # New TF-IDF command
    tfidf_parser = subparsers.add_parser("tfidf", help="Get TF-IDF score")
    tfidf_parser.add_argument("doc_id", type=int, help="Document ID")
    tfidf_parser.add_argument("term", type=str, help="Term to calculate score for")
    
    # Add the bm25idf subparser
    bm25_idf_parser = subparsers.add_parser("bm25idf", help="Get BM25 IDF score for a given term")
    bm25_idf_parser.add_argument("term", type=str, help="Term to get BM25 IDF score for")

    # Add bm25tf subparser
    bm25_tf_parser = subparsers.add_parser(
        "bm25tf", help="Get BM25 TF score for a given document ID and term"
    )
    
    #bm25 Modified subparser IDF/TF
    bm25_tf_parser.add_argument("doc_id", type=int, help="Document ID")
    bm25_tf_parser.add_argument("term", type=str, help="Term to get BM25 TF score for")
    bm25_tf_parser.add_argument("k1", type=float, nargs='?', default=BM25_K1, help="Tunable BM25 K1 parameter")
    bm25_tf_parser.add_argument("b", type=float, nargs='?', default=BM25_B, help="Tunable BM25 B parameter")
    
    # Add the bm25search subparser
    bm25search_parser = subparsers.add_parser("bm25search", help="Search movies using full BM25 scoring")
    bm25search_parser.add_argument("query", type=str, help="Search query")
    bm25search_parser.add_argument("--limit", type=int, default=5, help="Number of results to return")

    args = parser.parse_args()
    LIMIT = int(os.environ.get("LIMIT", 5))

    stopwords = set()
    try:
        with open("data/stopwords.txt", "r") as f:
            stopwords = set(f.read().splitlines())
    except IOError as ioe:
        print("File I/O Error has occurred!")
        ioe.print_exc()

    inv_index = InvertedIndex(stopwords)

    match args.command:
        case "bm25search":
            try:
                inv_index.load()
                results = inv_index.bm25_search(args.query, args.limit)
                
                for i, (doc_id, score) in enumerate(results, 1):
                    movie = inv_index.docmap[doc_id]
                    title = movie.get("title", "Unknown")
                    print(f"{i}. ({doc_id}) {title} - Score: {score:.2f}")
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

        case "bm25tf":
            try:
                bm25tf = bm25_tf_command(args.doc_id, args.term, args.k1, args.b, inv_index)
                print(f"BM25 TF score of '{args.term}' in document '{args.doc_id}': {bm25tf:.2f}")
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

        case "bm25idf":
            try:
                # Call the command and print formatted to 2 decimal places
                bm25idf_score = bm25_idf_command(args.term, inv_index)
                print(f"BM25 IDF score of '{args.term}': {bm25idf_score:.2f}")
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

        case "tfidf":
            try:
                inv_index.load()
                
                # 1. Calculate TF using your InvertedIndex method
                tf = inv_index.get_tf(args.doc_id, args.term)
                
                # 2. Calculate IDF
                stemmed_tokens = process_text(args.term, stopwords)
                term_match_doc_count = 0
                if stemmed_tokens:
                    target_token = stemmed_tokens[0]
                    term_match_doc_count = len(inv_index.index.get(target_token, set()))
                
                total_doc_count = len(inv_index.docmap)
                idf = math.log((total_doc_count + 1) / (term_match_doc_count + 1))
                # 3. Combine metrics: TF * IDF
                tf_idf = tf * idf
                
                # 4. Print formatted to 2 decimal places
                print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tf_idf:.2f}")

            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)
                
        case "idf":
            try:
                inv_index.load()
                
                # 1. Process the term to match the index keys
                stemmed_tokens = process_text(args.term, stopwords)
                if not stemmed_tokens:
                    # If the term is a stopword or empty, 
                    # it won't be in the index
                    term_match_doc_count = 0
                else:
                    target_token = stemmed_tokens[0]
                    # 2. Get the count of documents containing this term
                    term_match_doc_count = len(inv_index.index.get(target_token, set()))

                # 3. Apply the IDF formula
                # Total doc count is the size of our docmap silo
                total_doc_count = len(inv_index.docmap)
                
                idf = math.log((total_doc_count + 1) / (term_match_doc_count + 1) )
                # 4. Print formatted to 2 decimal places
                print(f"Inverse document frequency of '{args.term}': {idf:.2f}")

            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)
                
        case "build":
            with open("data/movies.json", "r") as f: data = json.load(f)
            inv_index.build(data.get("movies", []))
            inv_index.save()
            print("Index built and saved to cache/")

        case "search":
            try:
                inv_index.load()
            except IOError as ioe:
                print(f"Error: {ioe}")
                sys.exit(1)

            print(f"Searching for: {args.query}")
            query_tokens = process_text(args.query, stopwords)
            
            results = []
            seen_ids = set()

            # Iterate over query tokens and use the index for matching
            for token in query_tokens:
                doc_ids = inv_index.get_documents(token)
                for d_id in doc_ids:
                    if d_id not in seen_ids:
                        results.append(inv_index.docmap[d_id])
                        seen_ids.add(d_id)
                    # Stop once we hit the limit[cite: 1]
                    if len(results) >= LIMIT:
                        break
                if len(results) >= LIMIT:
                    break

            for i, movie in enumerate(results, 1):
                print(f"{i}. {movie['title']} (ID: {movie['id']})")
        
        case "tf":
            try:
                inv_index.load()
                # Print the frequency for the given ID and term[cite: 5]
                count = inv_index.get_tf(args.doc_id, args.term)
                print(count)
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
