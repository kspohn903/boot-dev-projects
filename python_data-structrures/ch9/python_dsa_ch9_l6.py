from node import Node

class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        # Note: 'self.next' is not a valid property of the list container itself, 
        # only individual Node objects have a 'next'. You can safely remove it.

    def add_to_tail(self, node):
        # Base case: If the list is empty, new node is both head and tail
        if self.head is None:
            self.head = node
            self.tail = node
            return

        # Connect the current tail node to our new node
        self.tail.next = node
        # Move the tail pointer to the new end of the list
        self.tail = node

    def add_to_head(self, node):
        # Base case: If the list is empty, new node is both head and tail
        if self.head is None:
            self.head = node
            self.tail = node
            return

        # Point the new node to the old head
        node.next = self.head
        # Move the head pointer to the new start of the list
        self.head = node

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next

    # don't touch below this line

    def __repr__(self):
        nodes = []
        current = self.head
        while current and hasattr(current, "val"):
            nodes.append(current.val)
            current = current.next
        return " -> ".join(nodes)
