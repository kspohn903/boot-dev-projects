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

    def rotate_left(self, pivot_parent):
        # 1. Establish a pointer to the right child (the node moving UP)
        y = pivot_parent.right

        # 2. Turn y's left subtree into pivot_parent's right subtree
        pivot_parent.right = y.left
        if y.left != self.nil:
            y.left.parent = pivot_parent

        # 3. Connect y's parent pointer to pivot_parent's original parent
        y.parent = pivot_parent.parent

        # 4. Update the parent to point down to y instead of pivot_parent
        if pivot_parent.parent is None:
            self.root = y
        elif pivot_parent == pivot_parent.parent.left:
            pivot_parent.parent.left = y
        else:
            pivot_parent.parent.right = y

        # 5. Place pivot_parent on y's left, finishing the exchange
        y.left = pivot_parent
        pivot_parent.parent = y

    def rotate_right(self, pivot_parent):
        # 1. Establish a pointer to the left child (the node moving UP)
        x = pivot_parent.left

        # 2. Turn x's right subtree into pivot_parent's left subtree
        pivot_parent.left = x.right
        if x.right != self.nil:
            x.right.parent = pivot_parent

        # 3. Connect x's parent pointer to pivot_parent's original parent
        x.parent = pivot_parent.parent

        # 4. Update the parent to point down to x instead of pivot_parent
        if pivot_parent.parent is None:
            self.root = x
        elif pivot_parent == pivot_parent.parent.right:
            pivot_parent.parent.right = x
        else:
            pivot_parent.parent.left = x

        # 5. Place pivot_parent on x's right, finishing the exchange
        x.right = pivot_parent
        pivot_parent.parent = x

    # don't touch below this line

    def insert(self, val):
        new_node = RBNode(val)
        new_node.parent = None
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.red = True

        parent = None
        current = self.root
        while current != self.nil:
            parent = current
            if new_node.val < current.val:
                current = current.left
            elif new_node.val > current.val:
                current = current.right
            else:
                return

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node
