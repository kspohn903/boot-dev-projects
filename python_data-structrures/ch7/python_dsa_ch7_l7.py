from stack import Stack


def is_balanced(input_str):
    stack = Stack()  
    # Initialize an empty stack
    for char in input_str:
        if char == "(":
           # Found an opening parenthesis, push it to track it
           stack.push(char)
        elif char == ")":
           # Found a closing parenthesis; check if there is a matching opener
           if stack.size() == 0:
              return False  # Extra closing parenthesis found!
           stack.pop()

    # If the stack is empty, every '(' had a matching ')'
    return (stack.size() == 0)
