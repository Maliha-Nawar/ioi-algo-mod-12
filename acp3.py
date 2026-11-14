class BNode:
    """Single node in a binary tree with data and up to two child links."""

    __slots__ = ("data", "left_ptr", "right_ptr")

    def __init__(self, data, left_ptr=None, right_ptr=None):
        self.data = data
        self.left_ptr = left_ptr
        self.right_ptr = right_ptr

    def is_leaf(self):
        return self.left_ptr is None and self.right_ptr is None

    def direct_children(self):
        return [child for child in (self.left_ptr, self.right_ptr) if child is not None]


class PointerBinaryTree:
    """Represents a binary tree structure anchored at a top (root) node."""

    def __init__(self, top=None):
        self.top = top

    def is_empty(self):
        return self.top is None

    def total_nodes(self):
        def _count(node):
            if node is None:
                return 0
            return 1 + _count(node.left_ptr) + _count(node.right_ptr)

        return _count(self.top)

    def leaf_values(self):
        leaves = []

        def _collect(node):
            if node is None:
                return
            if node.is_leaf():
                leaves.append(node.data)
                return
            _collect(node.left_ptr)
            _collect(node.right_ptr)

        _collect(self.top)
        return leaves

    def parent_child_edges(self):
        """Returns (parent_data, child_data) pairs showing structural links."""
        edges = []

        def _walk(node):
            if node is None:
                return
            for child in node.direct_children():
                edges.append((node.data, child.data))
            _walk(node.left_ptr)
            _walk(node.right_ptr)

        _walk(self.top)
        return edges


if __name__ == "__main__":
    # Constructing structural links explicitly:
    #        10
    #       /  \
    #     20    30
    #    /      / \
    #  40     50   60
    node_40 = BNode(40)
    node_50 = BNode(50)
    node_60 = BNode(60)
    node_20 = BNode(20, left_ptr=node_40)
    node_30 = BNode(30, left_ptr=node_50, right_ptr=node_60)
    root_10 = BNode(10, left_ptr=node_20, right_ptr=node_30)

    tree = PointerBinaryTree(top=root_10)

    print("Empty tree?:", tree.is_empty())
    print("Root data:  ", tree.top.data)
    print("Total nodes:", tree.total_nodes())
    print("Leaf values:", tree.leaf_values())
    print("Edges:      ", tree.parent_child_edges())