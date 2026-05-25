class BSTNode:
    def get_min(self):
        # Start at the current node
        current = self
        # Keep moving left as long as a left child exists
        while current.left is not None:
            current = current.left
        # Return the value of the leftmost node
        return current.val

    def get_max(self):
        # Start at the current node
        current = self
        # Keep moving right as long as a right child exists
        while current.right is not None:
            current = current.right
        # Return the value of the rightmost node
        return current.val

    # don't touch below this line

    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val = val

    def insert(self, val):
        if not self.val:
            self.val = val
            return

        if self.val == val:
            return

        if val < self.val:
            if self.left:
                self.left.insert(val)
                return
            self.left = BSTNode(val)
            return

        if self.right:
            self.right.insert(val)
            return
        self.right = BSTNode(val)
