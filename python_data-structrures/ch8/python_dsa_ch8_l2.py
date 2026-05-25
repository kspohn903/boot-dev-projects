class Queue:

    def __init__(self):
        self.items = []

    def push(self, item):
        # Add the item to the back of the queue (the end of the list)
        self.items.append(item)

    def pop(self):
        # Guard clause: Can't pop from an empty queue
        if self.size() == 0:
            return None
        # Remove and return the front of the queue (the very first element)
        return self.items.pop(0)

    def peek(self):
        # Guard clause: Can't peek into an empty queue
        if self.size() == 0:
            return None
        # Look at the front of the queue without removing it
        return self.items[0]

    def size(self):
        # Return the total number of items currently in the queue
        return len(self.items)
