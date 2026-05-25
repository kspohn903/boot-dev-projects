def letter_combinations(digits):
    # 1. If the input string is empty, return an empty list
    if not digits:
        return []
        
    # 2. Define a result list containing just an empty string to start
    result = [""]
    
    # 3. Iterate over the input digits
    for digit in digits:
        # 4. Handle invalid characters
        if digit not in digit_to_letters:
            raise ValueError(f"invalid digit: {digit}")
            
        # 5. Get the string of letters represented by the current digit
        letters = digit_to_letters[digit]
        
        # 6. Define an empty new_result list
        new_result = []
        
        # 7. Enter two nested for loops
        for combo in result:
            for letter in letters:
                # Append combo + letter to new_result
                new_result.append(combo + letter)
                
        # 8. Set result equal to new_result inside the main loop
        result = new_result
        
    # 9. Return the final result
    return result


# Don't touch below this line

digit_to_letters = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}
