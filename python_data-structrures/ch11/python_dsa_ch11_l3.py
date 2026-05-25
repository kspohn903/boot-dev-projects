class RBNode:
    def __init__(self, val):
        self.red = False
        self.parent = None
        self.val = val
        self.left = None
        self.right = None


class RBTree:
    def __init__(self):
        self.nil = RBNode(None)
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil

    def insert(self, val):
        # 1. Create the new node. New nodes are ALWAYS inserted as RED.
        new_node = RBNode(val)
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.red = True

        y = self.nil       # Tracks the parent pointer
        x = self.root      # Starts traversing from the root

        # 2. Standard BST Insertion (modified to look for self.nil instead of None)
        while x != self.nil:
            y = x
            if new_node.val < x.val:
                x = x.left
            else:
                x = x.right

        # Set the parent of our new node
        new_node.parent = y

        if y == self.nil:
            # Tree was empty, this is the root
            self.root = new_node
        elif new_node.val < y.val:
            y.left = new_node
        else:
            y.right = new_node

        # 3. Fix the tree properties if we violated any rules
        self._insert_fixup(new_node)

    def _insert_fixup(self, k):
        # While the parent is RED, we have a "Double Red" violation
        while k.parent.red:
            if k.parent == k.parent.parent.left:
                uncle = k.parent.parent.right
                
                # Case 1: Uncle is Red -> Recolor Parent, Uncle, and Grandparent
                if uncle.red:
                    k.parent.red = False
                    uncle.red = False
                    k.parent.parent.red = True
                    k = k.parent.parent # Move up to check grandparent
                else:
                    # Case 2: Uncle is Black and k is a Right Child -> Left Rotate
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    
                    # Case 3: Uncle is Black and k is a Left Child -> Right Rotate
                    k.parent.red = False
                    k.parent.parent.red = True
                    self._right_rotate(k.parent.parent)
            else:
                # Mirror cases when parent is a right child
                uncle = k.parent.parent.left
                if uncle.red:
                    k.parent.red = False
                    uncle.red = False
                    k.parent.parent.red = True
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.red = False
                    k.parent.parent.red = True
                    self._left_rotate(k.parent.parent)
                    
        # The root must always remain Black
        self.root.red = False

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
