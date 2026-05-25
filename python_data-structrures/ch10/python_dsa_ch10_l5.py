class BSTNode:
    def __init__(self, val=None):
        self.left = None
        self.right = None
        self.val = val

    def insert(self, val):
        # Base case: If the node was initialized empty, just assign the value
        if self.val is None:
            self.val = val
            return

        # Go left if the inserting value is less than the current node's value
        if val < self.val:
            if self.left is None:
                self.left = BSTNode(val)
            else:
                self.left.insert(val)
                
        # Go right if the inserting value is greater than or equal to the current node's value
        else:
            if self.right is None:
                self.right = BSTNode(val)
            else:
                self.right.insert(val)
