#!/usr/bin/env python3
import argparse
import sys
from lib.semantic_search import *
import re

def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("verify-embeddings")

    # Add the verify subparser
    subparsers.add_parser("verify", help="Verify the embedding model is loaded correctly")

    embed_parser = subparsers.add_parser("embed-text")
    embed_parser.add_argument("text", type=str, help="The text to convert to an embedding")

    embed_query_parser = subparsers.add_parser("embed-query")
    embed_query_parser.add_argument("query", type=str, help="The search query to convert to an embedding")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query", type=str)
    search_parser.add_argument("--limit", type=int, default=5)
    
    chunk_parser = subparsers.add_parser("chunk")
    chunk_parser.add_argument("text", type=str, help="The text to be chunked")
    chunk_parser.add_argument("--chunk-size", type=int, 
                                              default=200, 
                                              help="Number of words per chunk")

    chunk_parser.add_argument("--overlap", type=int, default=0, help="Number of overlapping words between chunks")
    
    sem_chunk_parser = subparsers.add_parser("semantic-chunk")
    sem_chunk_parser.add_argument("text", type=str)
    sem_chunk_parser.add_argument("--max-chunk-size", type=int, default=4)
    sem_chunk_parser.add_argument("--overlap", type=int, default=0)

    chunk_embed_parser = subparsers.add_parser("embed-chunks")

    search_chunked_parser = subparsers.add_parser("search-chunked")
    search_chunked_parser.add_argument("query", type=str)
    search_chunked_parser.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()
    movies_file = "data/movies.json"
    match args.command:
        # In match statement:
        case "search-chunked":
            # Using your existing load_movies function
            documents = load_movies() 
            searcher = ChunkedSemanticSearch()
            
            searcher.load_or_create_chunk_embeddings(documents)
    
            results = searcher.search_chunks(args.query, args.limit)
    
            for i, res in enumerate(results, 1):
                print(f"\n{i}. {res['title']} (score: {res['score']:.4f})")
                print(f"   {res['document']}...")

        case "embed-chunks":
            with open(movies_file, "r") as f:
                 data = json.load(f)
                 if isinstance(data, dict) and "movies" in data:
                    documents = data["movies"]
                 else:
                    documents = data
    
            searcher = ChunkedSemanticSearch()
            embeddings = searcher.load_or_create_chunk_embeddings(documents)
            print(f"Generated {len(embeddings)} chunked embeddings")

        case "semantic-chunk":
            # 1. Strip the initial input
            text = args.text.strip()
            if not text:
               print(f"Semantically chunking 0 characters")
               return # Returns empty list essentially

            # 2. Check for the "single sentence without punctuation" edge case
            # This prevents the regex from failing to find a split point
            if not any(text.endswith(p) for p in [".", "!", "?"]):
               sentences = [text]
            else:
            # 3. Split using the regex
               sentences = re.split(r"(?<=[.!?])\s+", text)
    
            # 4. Clean up individual sentences and filter out empty ones
            cleaned_sentences = []
            for s in sentences:
                stripped_s = s.strip()
                if stripped_s:
                   cleaned_sentences.append(stripped_s)

            # 5. Sliding window logic (using cleaned_sentences)
            max_size = args.max_chunk_size
            overlap = args.overlap
            chunks = []
            start_index = 0
            
            n_cleaned_sentences = len(cleaned_sentences)
            while (start_index < n_cleaned_sentences):
                  end_index = start_index + max_size
                  chunk_slice = cleaned_sentences[start_index:end_index]
                  chunks.append(" ".join(chunk_slice))
                  start_index += (max_size - overlap)
                  if (end_index >= n_cleaned_sentences):
                     break

            # 6. Output
            print(f"Semantically chunking {len(args.text)} characters")
            for i, chunk in enumerate(chunks, 1):
                print(f"{i}. {chunk}")

        case "chunk":
            words = args.text.split()
            size = args.chunk_size
            overlap = getattr(args, 'overlap', 0)
    
            if overlap >= size:
               print("Error: Overlap must be smaller than chunk size.")
               return

            chunks = []
            start_index = 0
    
            # Use a while loop to manually control the sliding window
            while start_index < len(words):
                # Slice the words from current start to size
                end_index = start_index + size
                chunk_words = words[start_index:end_index]
        
                # Join words back into a string and store
                chunks.append(" ".join(chunk_words))
        
                # Move the start_index forward by (size - overlap)
                # This creates the "sliding window" effect
                start_index += (size - overlap)
        
                # If we've reached or passed the end, break
                if end_index >= len(words):
                   break
            
            print(f"Chunking {len(args.text)} characters")
            for i, chunk in enumerate(chunks, 1):
                print(f"{i}. {chunk}")

        case "search":
            # 1. Load Data
            with open("data/movies.json", "r") as f:
                 data = json.load(f)
                 if isinstance(data, dict) and "movies" in data:
                    documents = data["movies"]
                 else:
                    documents = data
                 
            # 2. Initialize and Load Embeddings
            searcher = SemanticSearch()
            searcher.load_or_create_embeddings(documents)
    
            # 3. Perform Search
            results = searcher.search(args.query, args.limit)
    
            # 4. Print results
            for i, res in enumerate(results, 1):
                print(f"{i}. {res['title']} (score: {res['score']:.4f})")
                print(f"  {res['description'][:100]}...")
                print()
        
        case "embed-query":
            embed_query_text(args.query)
        case "verify-embeddings":
            verify_embeddings()
        case "verify":
            verify_model()
        case "embed-text":
            embed_text(args.text)
        case _:
            parser.print_help()

def load_movies(data_directory="data", movies_file="movies.json"):
    with open(f"{data_directory}/{movies_file}", "r") as f:
         data = json.load(f)
    # Handle both list format and {"movies": [...]} dict format
    if(isinstance(data,dict) and "movies" in data):
      return data["movies"]
    else:
      return data

if __name__ == "__main__":
    main()
