import re
def get_char_counts(file_contents):
    book_character_map_by_frequency = {}
    file_contents = file_contents.lower()
    for word in file_contents.split(" "):
        for character in word:
            # Method 1: Using .get() with a default value
            book_character_map_by_frequency[character] = book_character_map_by_frequency.get(character, 0) + 1
            # Method 2: Using collections.Counter 
            # (Most Pythonic and efficient for frequency counting)
            # This is the recommended approach for large stacks of words.
            # ( Requires 'from collections import Counter' at the top of 
            #   your file )
    return book_character_map_by_frequency

def get_num_words(file_contents):
    # 1. Normalize case: Convert to lowercase
    normalized_contents = file_contents.lower()
    words = normalized_contents.split()
    
    # 2. THE CORE REGEX PATTERN: Find sequences of word characters.
    #    \b: Word boundary - ensures we get whole words.
    #    [\w']+ : Matches one or more "word characters" (\w includes a-z, A-Z, 0-9, and underscore '_')
    #              AND also explicitly includes the apostrophe (').
    #    This pattern will capture:
    #    - "hello"
    #    - "world123"
    #    - "don't" (as one word)
    #    - "it's" (as one word)
    #    - "cat's" (as one word)
    #    - "123"
    #    - "underscore_word" (as one word)

    #    What about hyphens? If the gold standard counts "self-evident" 
    #    as ONE word, then the simple [\w']+ won't do it, as the hyphen isn't 
    #    a \w. 
    #    To include hyphens within words (e.g., "self-evident" as one word):
    #    We'll use a more specific pattern: letters/numbers, and optional 
    #    hyphens or apostrophed, followed by more letters/numbers.
    
    #!!! BETTER REAL-LIFE VERSION:
    # words = re.findall(r"[a-z0-9]+(?:['\-][a-z0-9]+)*", normalized_contents)
    
    # Breakdown of this new findall pattern:
    # [a-z0-9]+ : Matches one or more lowercase letters or digits. 
    # This forms the base of a word.
    # (?:      )*: This is a non-capturing group that can appear zero or more 
    #   times.
    #   ['\-]  : Matches either a literal apostrophe (') OR a hyphen (-).
    #   [a-z0-9]+: Matches 1+ lowercase letters or digits immediately 
    #              following the apostrophe or hyphen.
    # This pattern is robust because:
    # - It will capture "hello", "123", "word-word", "don't", "cat's".
    # - It effectively treats hyphens and apostrophes as *internal* parts 
    #   of words if they are surrounded by alphanumeric characters.
    # - It will naturally split on spaces, newlines, and any other 
    #   punctuation not explicitly included.

    # 3. Filter out any empty strings or purely non-alphanumeric remnants.
    #    re.findall generally does a good job, but this is a final cleanup.
    
    # actual_words = [word for word in words if word] 
    # # Simplest way to filter out empty strings
    
    # return len(actual_words)
    return len(words)

def descending_sort(items):
    # 1. Convert the dictionary (items) into a list of (key, value) tuples
    
    # 2. Sort the list of tuples (list_of_items)
    # The .sort() method sorts the list IN PLACE and returns None.
    # We must call it and then return the sorted list.
    items.sort(key=sort_on_count, reverse=True)

    # descending_elements_dict = dict(list_of_items) 
    # 3. Return the sorted list
    return items 

def ascending_sort(items):
    # 1. Convert the dictionary (items) into a list of (key, value) tuple
    
    # 2. Sort the list of tuples (list_of_items)
    # The .sort() method sorts the list IN PLACE and returns None.
    # We must call it and then return the sorted list.
    items.sort(key=sort_on_count, reverse=False)
    
    # descending_elements_dict = dict(list_of_items)
    # 3. Return the sorted list
    return items 

def sort_on_count(item):
    return item['count']

def get_sorted_char_counts(char_counts):
    sorted_chars = []
    for char, count in char_counts.items():
        if char.isalpha():
           sorted_chars.append({"char": char, "count": count})
    sorted_chars = ascending_sort(sorted_chars)
    return sorted_chars

