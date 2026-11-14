class ArrayBackedTree:
    """Index-mapped binary tree structure stored in a flat slot list.

    For any populated node at index `idx`:
      - left child slot  -> 2 * idx + 1
      - right child slot -> 2 * idx + 2
      - parent slot      -> (idx - 1) // 2  (for idx > 0)
    Unoccupied positions hold None.
    """

    def __init__(self, slot_capacity: int = 15) -> None:
        self.slot_capacity = slot_capacity
        self.slots: list = [None] * slot_capacity

    def _ensure_capacity(self, needed_index: int) -> None:
        while needed_index >= len(self.slots):
            self.slots.extend([None] * len(self.slots))

    def attach_root(self, value) -> int:
        """Places the root element at index 0 and returns its index."""
        self.slots[0] = value
        return 0

    def left_of(self, idx: int) -> int:
        return 2 * idx + 1

    def right_of(self, idx: int) -> int:
        return 2 * idx + 2

    def parent_of(self, idx: int) -> int | None:
        if idx <= 0:
            return None
        return (idx - 1) // 2

    def link_left(self, parent_idx: int, value) -> int:
        """Attaches a left child to an existing node and returns the child index."""
        if parent_idx < 0 or parent_idx >= len(self.slots) or self.slots[parent_idx] is None:
            raise IndexError("Parent slot is empty or out of bounds")
        child_idx = self.left_of(parent_idx)
        self._ensure_capacity(child_idx)
        self.slots[child_idx] = value
        return child_idx

    def link_right(self, parent_idx: int, value) -> int:
        """Attaches a right child to an existing node and returns the child index."""
        if parent_idx < 0 or parent_idx >= len(self.slots) or self.slots[parent_idx] is None:
            raise IndexError("Parent slot is empty or out of bounds")
        child_idx = self.right_of(parent_idx)
        self._ensure_capacity(child_idx)
        self.slots[child_idx] = value
        return child_idx

    def has_left(self, idx: int) -> bool:
        l_idx = self.left_of(idx)
        return l_idx < len(self.slots) and self.slots[l_idx] is not None

    def has_right(self, idx: int) -> bool:
        r_idx = self.right_of(idx)
        return r_idx < len(self.slots) and self.slots[r_idx] is not None

    def is_terminal(self, idx: int) -> bool:
        """True when a populated node has neither a left nor a right child."""
        if idx < 0 or idx >= len(self.slots) or self.slots[idx] is None:
            return False
        return not self.has_left(idx) and not self.has_right(idx)

    def node_depth(self, idx: int) -> int:
        """Number of parent steps from `idx` up to root index 0."""
        depth = 0
        curr = idx
        while curr > 0:
            curr = (curr - 1) // 2
            depth += 1
        return depth

    def active_count(self) -> int:
        return sum(1 for item in self.slots if item is not None)

    def structural_links(self) -> list[tuple[str, int, int]]:
        """Lists ('left'|'right', parent_idx, child_idx) for every populated link."""
        links: list[tuple[str, int, int]] = []
        for idx, val in enumerate(self.slots):
            if val is None:
                continue
            if self.has_left(idx):
                links.append(("left", idx, self.left_of(idx)))
            if self.has_right(idx):
                links.append(("right", idx, self.right_of(idx)))
        return links


if __name__ == "__main__":
    # Build structure:
    #         "R" (idx 0)
    #        /   \
    #    "L" (1)  "Ri" (2)
    #     /         \
    # "LL" (3)     "RiR" (6)
    atree = ArrayBackedTree(slot_capacity=7)
    r = atree.attach_root("R")
    l1 = atree.link_left(r, "L")
    r1 = atree.link_right(r, "Ri")
    ll = atree.link_left(l1, "LL")
    rr = atree.link_right(r1, "RiR")

    print("Raw slots:       ", atree.slots)
    print("Active nodes:    ", atree.active_count())
    print("Links (dir,p,c): ", atree.structural_links())
    for label, pos in [("R", r), ("L", l1), ("Ri", r1), ("LL", ll), ("RiR", rr)]:
        print(
            f"Node {label} @ idx {pos}: "
            f"parent={atree.parent_of(pos)}, "
            f"depth={atree.node_depth(pos)}, "
            f"terminal={atree.is_terminal(pos)}"
        )