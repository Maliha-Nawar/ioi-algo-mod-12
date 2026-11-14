class BiLinkNode:
    """Binary tree node storing an element plus parent and child references."""

    def __init__(self, element, up=None, down_left=None, down_right=None):
        self.element = element
        self.up = up
        self.down_left = down_left
        self.down_right = down_right

    def is_root(self) -> bool:
        return self.up is None

    def is_terminal(self) -> bool:
        return self.down_left is None and self.down_right is None

    def sibling(self):
        """Returns the other child of this node's parent, or None if unavailable."""
        if self.up is None:
            return None
        if self.up.down_left is self:
            return self.up.down_right
        if self.up.down_right is self:
            return self.up.down_left
        return None


class BiLinkTree:
    """Binary tree structure supporting bidirectional navigation and ancestor checks."""

    def __init__(self, head: BiLinkNode | None = None):
        self.head = head

    def attach_left(self, parent: BiLinkNode, element) -> BiLinkNode:
        if parent.down_left is not None:
            raise ValueError("Left slot already occupied")
        child = BiLinkNode(element=element, up=parent)
        parent.down_left = child
        return child

    def attach_right(self, parent: BiLinkNode, element) -> BiLinkNode:
        if parent.down_right is not None:
            raise ValueError("Right slot already occupied")
        child = BiLinkNode(element=element, up=parent)
        parent.down_right = child
        return child

    def lineage(self, node: BiLinkNode) -> list:
        """Traces elements from `node` upward to `head`."""
        path = []
        cursor = node
        while cursor is not None:
            path.append(cursor.element)
            cursor = cursor.up
        return path

    def all_nodes(self) -> list[BiLinkNode]:
        """Collects every node in pre-order (self, left subtree, right subtree)."""
        collected: list[BiLinkNode] = []

        def _scan(current: BiLinkNode | None) -> None:
            if current is None:
                return
            collected.append(current)
            _scan(current.down_left)
            _scan(current.down_right)

        _scan(self.head)
        return collected


if __name__ == "__main__":
    # Structure:
    #        "Root"
    #        /    \
    #   "Alpha"  "Beta"
    #    /    \
    # "Gamma" "Delta"
    root_node = BiLinkNode("Root")
    tree = BiLinkTree(head=root_node)

    alpha = tree.attach_left(root_node, "Alpha")
    beta = tree.attach_right(root_node, "Beta")
    gamma = tree.attach_left(alpha, "Gamma")
    delta = tree.attach_right(alpha, "Delta")

    for n in tree.all_nodes():
        sib = n.sibling().element if n.sibling() else None
        print(
            f"Element={n.element:<6} | "
            f"root={str(n.is_root()):<5} | "
            f"terminal={str(n.is_terminal()):<5} | "
            f"sibling={str(sib):<6} | "
            f"lineage={tree.lineage(n)}"
        )