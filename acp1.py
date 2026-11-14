from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class TreeNode:
    """Basic building block of a binary tree."""
    value: int
    left: Optional[TreeNode] = None
    right: Optional[TreeNode] = None


class BinaryTree:
    """Binary tree anchored by a root reference (or None when empty)."""

    def __init__(self, root: Optional[TreeNode] = None) -> None:
        self.root = root

    # --- Traversals ---

    def preorder(self) -> list[int]:
        """Root -> Left -> Right."""
        result: list[int] = []

        def _visit(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            result.append(node.value)
            _visit(node.left)
            _visit(node.right)

        _visit(self.root)
        return result

    def inorder(self) -> list[int]:
        """Left -> Root -> Right."""
        result: list[int] = []

        def _visit(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            _visit(node.left)
            result.append(node.value)
            _visit(node.right)

        _visit(self.root)
        return result

    def postorder(self) -> list[int]:
        """Left -> Right -> Root."""
        result: list[int] = []

        def _visit(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            _visit(node.left)
            _visit(node.right)
            result.append(node.value)

        _visit(self.root)
        return result

    def level_order(self) -> list[list[int]]:
        """Visits nodes level by level from top to bottom."""
        if self.root is None:
            return []

        levels: list[list[int]] = []
        queue: deque[TreeNode] = deque([self.root])

        while queue:
            level_size = len(queue)
            current_level: list[int] = []
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.value)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            levels.append(current_level)

        return levels

    # --- Structural Properties ---

    def size(self) -> int:
        """Total number of nodes in the tree."""
        def _count(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            return 1 + _count(node.left) + _count(node.right)

        return _count(self.root)

    def height(self) -> int:
        """Number of edges on the longest root-to-leaf path (-1 for empty tree)."""
        def _height(node: Optional[TreeNode]) -> int:
            if node is None:
                return -1
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)

    def count_leaves(self) -> int:
        """Counts nodes where both left and right children are None."""
        def _leaves(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            if node.left is None and node.right is None:
                return 1
            return _leaves(node.left) + _leaves(node.right)

        return _leaves(self.root)


if __name__ == "__main__":
    # Build a small concrete tree:
    #         1
    #       /   \
    #      2     3
    #     / \     \
    #    4   5     6
    root = TreeNode(
        1,
        left=TreeNode(2, left=TreeNode(4), right=TreeNode(5)),
        right=TreeNode(3, right=TreeNode(6)),
    )
    tree = BinaryTree(root)

    print("Pre-order:  ", tree.preorder())
    print("In-order:   ", tree.inorder())
    print("Post-order: ", tree.postorder())
    print("Level-order:", tree.level_order())
    print("Size:       ", tree.size())
    print("Height:     ", tree.height())
    print("Leaves:     ", tree.count_leaves())

    empty_tree = BinaryTree()
    print("Empty size / height:", empty_tree.size(), empty_tree.height())