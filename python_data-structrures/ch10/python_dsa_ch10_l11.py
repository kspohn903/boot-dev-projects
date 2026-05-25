class BSTNode:
    def preorder(self, visited):
        # 1. Base case: if the node has no value, just return
        if self.val is None:
            return visited

        # 2. Visit the current node first (Root)
        visited.append(self.val)

        # 3. Recursively traverse the Left subtree if it exists
        if self.left is not None:
            self.left.preorder(visited)

        # 4. Recursively traverse the Right subtree if it exists
        if self.right is not None:
            self.right.preorder(visited)

        # 5. Return the accumulated list of visited values
        return visited

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
