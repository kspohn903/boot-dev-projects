class BSTNode:
    def delete(self, val):
        # 1. Check if the current node is empty (has no value)
        if self.val is None:
            return None

        # 2. If the value to delete is less than the current node's value
        if val < self.val:
            if self.left:
                self.left = self.left.delete(val)
            return self

        # 3. If the value to delete is greater than the current node's value
        elif val > self.val:
            if self.right:
                self.right = self.right.delete(val)
            return self

        # 4. If the value to delete equals the current node's value
        else:
            # Case A: No right child -> bypass current node by returning left child
            if self.right is None:
                return self.left

            # Case B: No left child -> bypass current node by returning right child
            if self.left is None:
                return self.right

            # Case C: Both left and right children exist
            # Start at the right child
            successor = self.right
            # Walk left until you find the smallest node in that right subtree
            while successor.left is not None:
                successor = successor.left
            
            # Copy the next largest value into the current node's value
            self.val = successor.val
            
            # Delete that successor value from the right subtree and update the right child reference
            self.right = self.right.delete(successor.val)
            
            # Return the current node
            return self

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

    def get_min(self):
        current = self
        while current.left is not None:
            current = current.left
        return current.val

    def get_max(self):
        current = self
        while current.right is not None:
            current = current.right
        return current.val
