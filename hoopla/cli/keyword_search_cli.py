#!/usr/bin/env python3
import argparse
import json
import string
from typing import List, Dict, Any
import os
from pathlib import Path
# >>> ADD NLTK IMPORTS FOR STEMMING
# NOTE: Requires 'uv add nltk==3.9.1'
import nltk
from nltk.stem import PorterStemmer

# === Path setup (Robust method using absolute paths) ===
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_FILE_PATH = PROJECT_ROOT / "data" / "movies.json" 
STOPWORDS_FILE_PATH = PROJECT_ROOT / "data" / "stopwords.txt"

# === Global Text Processing Tools Initialization ===
PUNCTUATION_TRANSLATOR = str.maketrans('', '', string.punctuation)

# 1. Initialize the stemmer globally
STEMMER = PorterStemmer() 

# === STOPWORDS Loading ===
STOPWORDS = set() 
try:
    with open(STOPWORDS_FILE_PATH, 'r') as f:
        stopwords_list = f.read().splitlines()
        STOPWORDS = set(stopwords_list)
except FileNotFoundError:
    print(f"Error: Stopwords file not found at {STOPWORDS_FILE_PATH}")
except Exception as e:
    print(f"An error occurred loading stopwords: {e}")
# ============================================================

def remove_punctuation(text: str) -> str:
    """Removes all standard punctuation from a string."""
    return text.translate(PUNCTUATION_TRANSLATOR)

def tokenize(text: str) -> List[str]:
    """
    Removes punctuation, converts to lowercase, splits text into tokens, 
    removes stop words, and applies stemming.
    """
    # 1. Remove punctuation and convert to lowercase
    processed_text = remove_punctuation(text).lower()
    
    # 2. Split on whitespace
    tokens = processed_text.split()
    
    # 3. Remove stop words
    filtered_tokens = [token for token in tokens if token not in STOPWORDS]

    # 4. Apply stemming to each remaining token
    stemmed_tokens = [STEMMER.stem(token) for token in filtered_tokens]
    
    return stemmed_tokens


def keyword_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Performs a token-based keyword search with full text processing (case, 
    punctuation, stop words, stemming).
    """
    try:
        # Use the robust absolute path constant
        with open(DATA_FILE_PATH, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_FILE_PATH}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {DATA_FILE_PATH}")
        return []

    all_movies = data.get("movies", [])
    results = []

    # Tokenize the query (now includes stemming)
    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    # Iterate over all movies and check their "title"
    for movie in all_movies:
        movie_title = movie.get("title", "")
        
        # Tokenize the title (now includes stemming)
        title_tokens = tokenize(movie_title)
        
        # Matching Logic: Check if at least one query token matches ANY title token
        is_match = False
        for q_token in query_tokens:
            for t_token in title_tokens:
                # With stemming, we switch to exact match (==) for precision
                if q_token == t_token: # <--- IMPORTANT: Changed to exact match (==)
                    is_match = True
                    break 
            if is_match:
                break 
        
        if is_match:
            results.append(movie)

    # Truncate the list to a maximum of 'max_results', order by IDs ascending.
    results.sort(key=lambda x: x.get("id"))
    return results[:max_results]


def print_results(query: str, results: List[Dict[str, Any]]) -> None:
    """
    Prints the search query and the list of results in the required format.
    """
    print(f"Searching for: {query}")
    if not results:
        return

    for i, movie in enumerate(results, 1):
        print(f"{i}. {movie.get('title', 'Untitled Movie')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            query = args.query
            search_results = keyword_search(query)
            print_results(query, search_results)
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
