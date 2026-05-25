class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
   
    def pop(self):
        # Guard clause: Can't pop from an empty stack
        if self.size() == 0:
            return None
        # FIX: Python's built-in .pop() removes and returns the LAST item
        return self.items.pop()

    def peek(self):
        # Guard clause: Can't peek an empty stack
        if self.size() == 0:
           return None
        # FIX: Peek at the LAST item in the list (the top of the stack)
        return self.items[-1]

    def size(self):
        return len(self.items)
