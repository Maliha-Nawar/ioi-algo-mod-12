from __future__ import annotations
from collections import deque
from typing import Any


class Cell:
    """Storage unit holding a payload and up to two branch references."""

    def __init__(self, payload: Any) -> None:
        self.payload = payload
        self.first_child: Cell | None = None
        self.second_child: Cell | None = None


class LinkedBinaryTree:
    """General binary tree supporting search, level-wise insertion, and deletion."""

    def __init__(self) -> None:
        self.anchor: Cell | None = None

    def has_item(self, target: Any) -> bool:
        """Breadth-first lookup checking every reachable cell."""
        if self.anchor is None:
            return False

        frontier: deque[Cell] = deque([self.anchor])
        while frontier:
            current = frontier.popleft()
            if current.payload == target:
                return True
            if current.first_child is not None:
                frontier.append(current.first_child)
            if current.second_child is not None:
                frontier.append(current.second_child)
        return False

    def append_breadth_first(self, item: Any) -> None:
        """Places item into the first open child position encountered level by level."""
        fresh = Cell(item)
        if self.anchor is None:
            self.anchor = fresh
            return

        frontier: deque[Cell] = deque([self.anchor])
        while frontier:
            current = frontier.popleft()

            if current.first_child is None:
                current.first_child = fresh
                return
            frontier.append(current.first_child)

            if current.second_child is None:
                current.second_child = fresh
                return
            frontier.append(current.second_child)

    def prune_item(self, target: Any) -> bool:
        """Removes target by swapping in the deepest rightmost payload and detaching it.

        Returns True if an item was removed, False if target was absent.
        """
        if self.anchor is None:
            return False

        # Single-cell tree edge case
        if (
            self.anchor.first_child is None
            and self.anchor.second_child is None
        ):
            if self.anchor.payload == target:
                self.anchor = None
                return True
            return False

        frontier: deque[Cell] = deque([self.anchor])
        matched_cell: Cell | None = None
        last_seen: Cell | None = None
        parent_of_last: dict[int, Cell] = {}

        while frontier:
            current = frontier.popleft()
            last_seen = current

            if current.payload == target and matched_cell is None:
                matched_cell = current

            if current.first_child is not None:
                parent_of_last[id(current.first_child)] = current
                frontier.append(current.first_child)

            if current.second_child is not None:
                parent_of_last[id(current.second_child)] = current
                frontier.append(current.second_child)

        if matched_cell is None or last_seen is None:
            return False

        # Copy deepest rightmost payload into matched_cell, then drop last_seen
        matched_cell.payload = last_seen.payload
        parent = parent_of_last[id(last_seen)]
        if parent.second_child is last_seen:
            parent.second_child = None
        else:
            parent.first_child = None

        return True

    def snapshot_levels(self) -> list[list[Any]]:
        """Helper to inspect payloads grouped by distance from anchor."""
        if self.anchor is None:
            return []

        rows: list[list[Any]] = []
        frontier: deque[Cell] = deque([self.anchor])

        while frontier:
            row_len = len(frontier)
            row: list[Any] = []
            for _ in range(row_len):
                current = frontier.popleft()
                row.append(current.payload)
                if current.first_child is not None:
                    frontier.append(current.first_child)
                if current.second_child is not None:
                    frontier.append(current.second_child)
            rows.append(row)

        return rows


if __name__ == "__main__":
    tree = LinkedBinaryTree()
    for val in ["A", "B", "C", "D", "E", "F"]:
        tree.append_breadth_first(val)

    print("Levels after insert:", tree.snapshot_levels())
    print("Contains 'E':        ", tree.has_item("E"))
    print("Contains 'Z':        ", tree.has_item("Z"))

    removed = tree.prune_item("B")
    print("Pruned 'B':          ", removed)
    print("Levels after prune:  ", tree.snapshot_levels())