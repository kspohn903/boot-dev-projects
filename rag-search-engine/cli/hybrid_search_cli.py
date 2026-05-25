import argparse
import json
from lib.hybrid_search import HybridSearch
from . import *

# Assuming you have your load_movies helper available
def load_movies():
    with open("data/movies.json", "r") as f:
        data = json.load(f)
    return data["movies"] if isinstance(data, dict) and "movies" in data else data

def main() -> None:
    parser = argparse.ArgumentParser(description="Hybrid Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Placeholder for future hybrid commands
    subparsers.add_parser("search")
    
    # Add the normalize command
    norm_parser = subparsers.add_parser("normalize")
    norm_parser.add_argument("scores", type=float, nargs="*", 
                                       help="List of scores to normalize")

    weighted_parser = subparsers.add_parser("weighted-search")
    weighted_parser.add_argument("query", type=str)
    weighted_parser.add_argument("--alpha", type=float, default=0.5)
    weighted_parser.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()

    match args.command:
        case "weighted-search":
            documents = load_movies()
            searcher = HybridSearch(documents)
            results = searcher.weighted_search(args.query, args.alpha, 
                                                           args.limit)
    
            for i, res in enumerate(results[:args.limit], 1):
                print(f"{i}. {res['title']}")
                print(f"  Hybrid Score: {res['hybrid_score']:.3f}")
                print(f"  BM25: {res['bm25']:.3f}, Semantic: {res['semantic']:.3f}")
                print(f"  {res['document']}...")
        case "normalize":
            if not args.scores:
                return

            min_score = min(args.scores)
            max_score = max(args.scores)

            # Edge case: all scores are the same
            if min_score == max_score:
               for _ in args.scores:
                   print(f"* {1.0000:.4f}")
                   return
            # Apply Min-Max Normalization
            for score in args.scores:
                normalized = (score - min_score) / (max_score - min_score)
                print(f"* {normalized:.4f}")
        
        case "search":
            print("Hybrid search command recognized, but logic is pending implementation.")
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
