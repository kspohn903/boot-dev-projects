import argparse
import json
import os

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    if args.command == "search":
        query = args.query
        print(f"Searching for: {query}")
        
        # Use a path relative to where you run the command (the project root)
        movie_path = "data/movies.json" 
        
        try:
            with open(movie_path, "r") as f:
                data = json.load(f)
                movies = data.get("movies", [])

            results = [m for m in movies if query in m["title"]]
            
            for i, movie in enumerate(results[:5], 1):
                print(f"{i}. {movie['title']}")
                
        except IOError as ioe:
            print(f"Error: Could not find {movie_path}. Are you in the project root?")
            ioe.print_exc()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
