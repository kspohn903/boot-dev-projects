from node import Node


class LinkedList:

    def __init__(self):
        # An empty linked list has no head node to start
        self.head = None

    def __iter__(self):
        # Start tracking from the beginning of the list
        current = self.head

        # Walk through the chain until you hit None
        while current is not None:
            # Yield the current node object itself
            yield current
            # Shift your tracking pointer to the next linked node
            current = current.next

    # don't touch below this line

    def __repr__(self):
        nodes = []
        current = self.head
        while current and hasattr(current, "val"):
            nodes.append(current.val)
            current = current.next
        return " -> ".join(nodes)
