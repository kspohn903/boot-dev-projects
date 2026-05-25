# import glob
import os
import re
import sys
from pprint import pprint
from stats import (get_num_words, get_char_counts, get_sorted_char_counts, ascending_sort, descending_sort)

def get_book_text(filepath):
    """
    Reads the contents of a file and returns it as a string.

    Args:
        filepath (str): The path to the file.

    Returns:
        str: The contents of the file.
    """
    try:
        with open(filepath, 'r') as file:
            return f"{file.read()}"
    except FileNotFoundError:
        return f"Error: File not found at '{filepath}'"
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    """
    Reads a book (located in the 'books' directory or a provided path)
    from the command line, counts words and character occurrences,
    and prints the results.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)

    book_arguments = sys.argv[1:]
    print("============ BOOKBOT ============")
    for book_argument in book_arguments:
        default_book_path = os.path.join("books", book_argument)

        if os.path.exists(book_argument):
           book_path = book_argument  
           # Use the provided argument as a direct path
        elif os.path.exists(default_book_path):
           book_path = default_book_path  
           # Look in the 'books' directory
        else:
           print(f"Error: Book not found at '{book_argument}' or '{default_book_path}'")
           sys.exit(1)
        print(f"Analyzing book found at {book_path}...") 
        book_content = get_book_text(book_path)

        if isinstance(book_content, str) and not book_content.startswith("Error"):
           
           print("----------- Word Count ----------")   
           num_words = get_num_words(book_content)
           print(f"Found {num_words} total words")
           
           print("--------- Character Count -------")
           char_counts = get_char_counts(book_content)
           sorted_char_counts = descending_sort(
                   get_sorted_char_counts(char_counts) 
           )
           for item in sorted_char_counts:
               print(f"{item['char']}: {item['count']}")
        else:
           print(book_content)
     
    print("============= END ===============")

if __name__ == "__main__":
    main()

