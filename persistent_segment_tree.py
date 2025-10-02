from typing import Optional, List

class PersistentSegmentTreeNode:
    """
    A node in the persistent segment tree.
    """
    def __init__(self, left: int, right: int, value: int = 0,
                 left_child: Optional['PersistentSegmentTreeNode'] = None,
                 right_child: Optional['PersistentSegmentTreeNode'] = None,
                 lazy: int = 0) -> None:
        self.left: int = left      # Start index of this segment
        self.right: int = right    # End index of this segment (exclusive)
        self.value: int = value    # The value for this segment (e.g., sum)
        self.left_child: Optional['PersistentSegmentTreeNode'] = left_child
        self.right_child: Optional['PersistentSegmentTreeNode'] = right_child
        self.lazy: int = lazy      # Lazy propagation marker

def build_segment_tree(arr: List[int], l: int, r: int) -> PersistentSegmentTreeNode:
    """Recursively builds the segment tree."""
    if l + 1 == r:
        # Leaf node
        return PersistentSegmentTreeNode(l, r, arr[l])
    m = (l + r) // 2
    left_child = build_segment_tree(arr, l, m)
    right_child = build_segment_tree(arr, m, r)
    return PersistentSegmentTreeNode(l, r, left_child.value + right_child.value, left_child, right_child)

def propagate(node: PersistentSegmentTreeNode) -> None:
    """Propagate the lazy value to the children nodes (creates new nodes for persistence)."""
    if node.lazy != 0 and node.left_child is not None and node.right_child is not None:
        m = (node.left + node.right)//2
        # Create new child nodes for persistence
        node.left_child = PersistentSegmentTreeNode(
            node.left_child.left,
            node.left_child.right,
            node.left_child.value + node.lazy * (m - node.left),
            node.left_child.left_child,
            node.left_child.right_child,
            node.left_child.lazy + node.lazy
        )
        node.right_child = PersistentSegmentTreeNode(
            node.right_child.left,
            node.right_child.right,
            node.right_child.value + node.lazy * (node.right - m),
            node.right_child.left_child,
            node.right_child.right_child,
            node.right_child.lazy + node.lazy
        )
        node.lazy = 0

def update(node: PersistentSegmentTreeNode, l: int, r: int, val: int) -> PersistentSegmentTreeNode:
    """
    Range update: Returns a new persistent version of the segment tree with [l, r) increased by val.
    """
    if node.right <= l or r <= node.left:
        return node  # No overlap, same node
    if l <= node.left and node.right <= r:
        # Complete overlap, create new node with updated lazy and value
        new_node = PersistentSegmentTreeNode(
            node.left, node.right,
            node.value + val * (node.right - node.left),
            node.left_child, node.right_child,
            node.lazy + val
        )
        return new_node
    # Partial overlap, propagate and recur
    propagate(node)
    left_child = update(node.left_child, l, r, val) if node.left_child else None
    right_child = update(node.right_child, l, r, val) if node.right_child else None
    new_node = PersistentSegmentTreeNode(
        node.left, node.right,
        (left_child.value if left_child else 0) + (right_child.value if right_child else 0),
        left_child, right_child, 0)
    return new_node

def query(node: PersistentSegmentTreeNode, l: int, r: int) -> int:
    """
    Range sum query: Returns the sum in [l, r) for a given version.
    """
    if node.right <= l or r <= node.left:
        return 0  # No overlap
    if l <= node.left and node.right <= r:
        return node.value
    propagate(node)
    left_sum = query(node.left_child, l, r) if node.left_child else 0
    right_sum = query(node.right_child, l, r) if node.right_child else 0
    return left_sum + right_sum

# Example Usage:

# Initial array
a = [1, 2, 3, 4, 5]

# Build original tree (version 0)
root_v0: PersistentSegmentTreeNode = build_segment_tree(a, 0, len(a))

# Update [1,4): add 10, create version 1
root_v1: PersistentSegmentTreeNode = update(root_v0, 1, 4, 10)

# Update [2,5): add 5, create version 2
root_v2: PersistentSegmentTreeNode = update(root_v1, 2, 5, 5)

# Query version 0
print("Query [0,5) on version 0:", query(root_v0, 0, 5))  # Output: 15

# Query version 1
print("Query [0,5) on version 1:", query(root_v1, 0, 5))  # Output: 45

# Query version 2
print("Query [0,5) on version 2:", query(root_v2, 0, 5))  # Output: 60
