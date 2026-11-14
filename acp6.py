class PathAddressedBinaryTree:
    """Binary tree structure where each node is located by a path of '0' (left) and '1' (right) steps."""

    def __init__(self) -> None:
        self._nodes: dict[str, object] = {}

    def set_root(self, value: object) -> str:
        """Places the root node at the empty path ''."""
        self._nodes[""] = value
        return ""

    @staticmethod
    def left_path(path: str) -> str:
        return f"{path}0"

    @staticmethod
    def right_path(path: str) -> str:
        return f"{path}1"

    @staticmethod
    def parent_path(path: str) -> str | None:
        if path == "":
            return None
        return path[:-1]

    def attach_left(self, parent: str, value: object) -> str:
        if parent not in self._nodes:
            raise KeyError(f"Parent path {parent!r} does not exist")
        child = self.left_path(parent)
        self._nodes[child] = value
        return child

    def attach_right(self, parent: str, value: object) -> str:
        if parent not in self._nodes:
            raise KeyError(f"Parent path {parent!r} does not exist")
        child = self.right_path(parent)
        self._nodes[child] = value
        return child

    def has_node(self, path: str) -> bool:
        return path in self._nodes

    def is_leaf(self, path: str) -> bool:
        if path not in self._nodes:
            return False
        has_l = self.left_path(path) in self._nodes
        has_r = self.right_path(path) in self._nodes
        return not has_l and not has_r

    def depth(self, path: str) -> int:
        if path not in self._nodes:
            raise KeyError(f"Path {path!r} does not exist")
        return len(path)

    def children_of(self, path: str) -> dict[str, tuple[str, object]]:
        """Returns existing 'left' and 'right' branches as {side: (child_path, value)}."""
        if path not in self._nodes:
            raise KeyError(f"Path {path!r} does not exist")
        branches: dict[str, tuple[str, object]] = {}
        lp = self.left_path(path)
        rp = self.right_path(path)
        if lp in self._nodes:
            branches["left"] = (lp, self._nodes[lp])
        if rp in self._nodes:
            branches["right"] = (rp, self._nodes[rp])
        return branches

    def leaves(self) -> list[tuple[str, object]]:
        return [(p, v) for p, v in sorted(self._nodes.items()) if self.is_leaf(p)]

    def subtree_paths(self, root_path: str = "") -> list[str]:
        """Lists all populated paths rooted at `root_path` in lexicographic path order."""
        if root_path not in self._nodes:
            return []
        return sorted(p for p in self._nodes if p.startswith(root_path))


if __name__ == "__main__":
    # Structure:
    #         "Core" ("")
    #        /        \
    #   "West" ("0")  "East" ("1")
    #      \            /     \
    # "WestRight"  "EastLeft" "EastRight"
    #   ("01")       ("10")     ("11")
    ptree = PathAddressedBinaryTree()
    root = ptree.set_root("Core")
    w = ptree.attach_left(root, "West")
    e = ptree.attach_right(root, "East")
    ptree.attach_right(w, "WestRight")
    ptree.attach_left(e, "EastLeft")
    ptree.attach_right(e, "EastRight")

    for path in ptree.subtree_paths():
        print(
            f"path={path or 'ROOT':<4} | "
            f"val={ptree._nodes[path]!r:<11} | "
            f"depth={ptree.depth(path)} | "
            f"parent={ptree.parent_path(path)!r:<4} | "
            f"leaf={ptree.is_leaf(path)} | "
            f"children={ptree.children_of(path)}"
        )

    print("Leaves:", ptree.leaves())
    print("Subtree under '1':", ptree.subtree_paths("1"))