from sentence_transformers import SentenceTransformer
import os
import json
import numpy as np
import re

class SemanticSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Initializes the pre-trained all-MiniLM-L6-v2 model
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self.documents = None
        self.document_map = {}

    def search_chunks(self, query: str, limit: int = 10):
        # 1. Embed the query using the parent's method
        query_embedding = self.model.encode(query)
        
        # 2. Calculate similarities for all chunks
        # Reshape query for batch calculation
        similarities = np.dot(self.chunk_embeddings, query_embedding) / (
            np.linalg.norm(self.chunk_embeddings, axis=1) * 
            np.linalg.norm(query_embedding)
        )

        # 3. Aggregate: Map chunk scores back to movie indexes
        # We take the MAX score found among a movie's chunks
        movie_scores = {}
        for idx, score in enumerate(similarities):
            metadata = self.chunk_metadata[idx]
            m_idx = metadata["movie_idx"]
            
            if m_idx not in movie_scores or score > movie_scores[m_idx]:
                movie_scores[m_idx] = score
        
        # 4. Sort by score descending
        sorted_movie_indices = sorted(movie_scores.keys(), 
                                      key=lambda k: movie_scores[k], 
                                      reverse=True)
        # 5. Format Top N results
        results = []
        for m_idx in sorted_movie_indices[:limit]:
            doc = self.documents[m_idx]
            score = float(movie_scores[m_idx])
            
            results.append({
                "id": doc.get("id", m_idx),
                "title": doc.get("title", "Unknown"),
                "document": doc.get("description", "")[:100],
                "score": round(score, 4),
                "metadata": {"movie_idx": m_idx}
            })
            
        return results

    # Inside your SemanticSearch class:
    def search(self, query, limit=5):
        if self.embeddings is None:
            raise ValueError("No embeddings loaded. Call `load_or_create_embeddings` first.")

        query_embedding = self.generate_embedding(query)
        
        results = []
        for i, doc_embedding in enumerate(self.embeddings):
            score = cosine_similarity(query_embedding, doc_embedding)
            # Match the embedding index back to the original document
            doc = self.documents[i]
            results.append((score, doc))

        # Sort by score (the first element in the tuple) descending
        results.sort(key=lambda x: x[0], reverse=True)

        # Return formatted dictionaries for the top results
        return [
            {
                "score": score,
                "title": doc["title"],
                "description": doc["description"]
            }
            for score, doc in results[:limit]
        ]

    def build_embeddings(self, documents):
        self.documents = documents
        movie_strings = []
        for doc in documents:
            # Map ID to doc for quick lookup later
            self.document_map[doc['id']] = doc
            # Create the combined text representation
            movie_strings.append(f"{doc['title']}: {doc['description']}")
        
        print("Generating embeddings (this may take a minute)...")
        # Bulk encode with progress bar
        self.embeddings = self.model.encode(movie_strings, 
                                            show_progress_bar=True)

        # Ensure cache directory exists
        os.makedirs("cache", exist_ok=True)
        np.save("cache/movie_embeddings.npy", self.embeddings)
        return self.embeddings
    
    def load_or_create_embeddings(self, documents):
        self.documents = documents
        # Always populate the map for lookups
        for doc in documents:
            self.document_map[doc['id']] = doc

        cache_path = "cache/movie_embeddings.npy"
        
        if os.path.exists(cache_path):
            self.embeddings = np.load(cache_path)
            # Verify cache matches current document count
            if len(self.embeddings) == len(documents):
                return self.embeddings
        
        return self.build_embeddings(documents)

    def generate_embedding(self, text):
        # Validation for empty or whitespace strings
        if not text or text.strip() == "":
            raise ValueError("Input text cannot be empty or only whitespace")
        
        # model.encode can take a single string or a list. 
        # The assignment asks to wrap it in a list and take the first result.
        embeddings = self.model.encode([text])
        return embeddings[0]

def embed_query_text(query):
    searcher = SemanticSearch()
    # Your generate_embedding method already handles the 
    # model.encode([text])[0] logic and whitespace validation
    embedding = searcher.generate_embedding(query)
    
    print(f"Query: {query}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Shape: {embedding.shape}")

def embed_text(text):
    searcher = SemanticSearch()
    embedding = searcher.generate_embedding(text)
    
    # Printing for the CLI verification
    print(f"Text: {text}")
    print(f"First 3 dimensions: {embedding[:3]}")
    # .shape[0] works because sentence-transformers returns numpy arrays
    print(f"Dimensions: {embedding.shape[0]}")


def verify_model():
    # Instantiate the class to trigger model loading
    searcher = SemanticSearch()
    
    # Print required metadata for verification
    print(f"Model loaded: {searcher.model}")
    print(f"Max sequence length: {searcher.model.max_seq_length}")


def verify_embeddings():
    # Load the source data
    movies_file = "data/movies.json"
    try:
        with open(movies_file, "r") as f:
             data = json.load(f)
    except IOError as ioe:
        print(f"Error: {movies_file} not found. Check your current working directory.")
        ioe.print_exc()
        return
    
    # If the JSON is a dict with a 'movies' key, grab that list.
    # Otherwise, assume 'data' is already the list.
    if isinstance(data, dict) and "movies" in data:
       documents = data["movies"]
    else:
       documents = data

    # Debug check: print the first item to see what it actually is
    if len(documents) > 0:
        print(f"DEBUG: First doc type is {type(documents[0])}")
        print(f"DEBUG: First doc value: {documents[0]}")

    searcher = SemanticSearch()
    embeddings = searcher.load_or_create_embeddings(documents)
    
    print(f"Number of docs:   {len(documents)}")
    # embeddings.shape is (num_vectors, dimensions)
    print(f"Embeddings shape: {embeddings.shape[0]} vectors in {embeddings.shape[1]} dimensions")


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return 0.0 if (norm1 == 0 or norm2 == 0) else (dot_product/(norm1 * norm2))


class ChunkedSemanticSearch(SemanticSearch):
    def __init__(self, model_name="all-MiniLM-L6-v2") -> None:
        super().__init__(model_name)
        self.chunk_embeddings = None
        self.chunk_metadata = None

    def build_chunk_embeddings(self, documents, size=4, overlap=1):
        self.documents = documents
        self.document_map = {doc["title"]: doc for doc in documents}
        
        all_chunks = []
        chunk_metadata = []
        
        for doc_idx, doc in enumerate(self.documents):
            text = doc.get("description", "")
            if not text:
                continue
            
            # Semantic chunking: 4 sentences, 1 sentence overlap
            sentences = re.split(r"(?<=[.!?])\s+", text)
            
            doc_chunks = []
            start = 0
            n_sentences = len(sentences)
            while start < n_sentences:
                end = start + size
                chunk_text = " ".join(sentences[start:end])
                doc_chunks.append(chunk_text)
                if (end >= n_sentences):
                    break
                start += (size - overlap) # (size 4 - overlap 1)

            # Record metadata for each chunk in this doc
            for chunk_idx, chunk_text in enumerate(doc_chunks):
                all_chunks.append(chunk_text)
                chunk_metadata.append({
                    "movie_idx": doc_idx,
                    "chunk_idx": chunk_idx,
                    "total_chunks": len(doc_chunks)
                })

        # Generate and cache embeddings
        self.chunk_embeddings = self.model.encode(all_chunks)
        self.chunk_metadata = chunk_metadata
        
        os.makedirs("cache", exist_ok=True)
        np.save("cache/chunk_embeddings.npy", self.chunk_embeddings)
        with open("cache/chunk_metadata.json", "w") as f:
            json.dump({"chunks": chunk_metadata, "total_chunks": len(all_chunks)}, f, indent=2)
            
        return self.chunk_embeddings

    def load_or_create_chunk_embeddings(self, documents: list[dict]) -> np.ndarray:
        self.documents = documents
        self.document_map = {doc["title"]: doc for doc in documents}
        
        embed_path = "cache/chunk_embeddings.npy"
        meta_path = "cache/chunk_metadata.json"
        
        if os.path.exists(embed_path) and os.path.exists(meta_path):
            self.chunk_embeddings = np.load(embed_path)
            with open(meta_path, "r") as f:
                data = json.load(f)
                self.chunk_metadata = data["chunks"]
            return self.chunk_embeddings
        
        return self.build_chunk_embeddings(documents)
