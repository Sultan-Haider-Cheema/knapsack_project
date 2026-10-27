"""
branch_and_bound.py
Branch and Bound solver for 0/1 Knapsack.
Uses best-first search with fractional bound.
"""

from typing import List, Tuple, Dict
import heapq

Item = Tuple[int, int, int]  # (value, weight, id)


# ----------------------------------------------------------
# Helper: Compute upper bound using fractional knapsack
# ----------------------------------------------------------
def fractional_bound(items: List[Item], capacity: int, level: int, current_value: int, current_weight: int) -> float:
    if current_weight > capacity:
        return 0  # infeasible → no bound

    remaining_cap = capacity - current_weight
    bound = current_value

    # Items sorted by ratio (best first)
    for i in range(level, len(items)):
        v, w, idx = items[i]
        if w <= remaining_cap:
            remaining_cap -= w
            bound += v
        else:
            # take fractional part
            bound += v * (remaining_cap / w)
            break

    return bound


# ----------------------------------------------------------
# Node structure for priority queue (max-heap using -bound)
# ----------------------------------------------------------
class Node:
    def __init__(self, level, value, weight, bound, taken):
        self.level = level
        self.value = value
        self.weight = weight
        self.bound = bound
        self.taken = taken  # list of item indices taken so far

    def __lt__(self, other):
        # max-heap based on bound → invert comparison
        return self.bound > other.bound


# ----------------------------------------------------------
# Branch and Bound Solver
# ----------------------------------------------------------
def branch_and_bound(items: List[Item], capacity: int):
    # Sort items by decreasing value/weight ratio (important!)
    items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)

    # Priority queue (max-heap)
    pq = []

    # Statistics
    stats = {
        "nodes_expanded": 0,
        "nodes_pruned": 0,
        "bound_calls": 0,
    }

    # Root node
    root = Node(
        level=0,
        value=0,
        weight=0,
        bound=fractional_bound(items, capacity, 0, 0, 0),
        taken=[]
    )
    stats["bound_calls"] += 1

    heapq.heappush(pq, root)

    best_value = 0
    best_solution = []

    # ------------------------------------------------------
    # Main Loop
    # ------------------------------------------------------
    while pq:
        node = heapq.heappop(pq)
        stats["nodes_expanded"] += 1

        # If bound is worse than current best, prune
        if node.bound <= best_value:
            stats["nodes_pruned"] += 1
            continue

        level = node.level

        # If we've processed all items, skip
        if level >= len(items):
            continue

        # -------------------------
        # Left child = Take item
        # -------------------------
        v, w, idx = items[level]
        left_weight = node.weight + w
        left_value = node.value + v

        if left_weight <= capacity:
            # Valid candidate
            if left_value > best_value:
                best_value = left_value
                best_solution = node.taken + [idx]

        # Compute bound for left child
        left_bound = fractional_bound(items, capacity, level + 1, left_value, left_weight)
        stats["bound_calls"] += 1

        if left_bound > best_value:
            heapq.heappush(
                pq,
                Node(level + 1, left_value, left_weight, left_bound, node.taken + [idx])
            )
        else:
            stats["nodes_pruned"] += 1

        # -------------------------
        # Right child = Skip item
        # -------------------------
        right_bound = fractional_bound(items, capacity, level + 1, node.value, node.weight)
        stats["bound_calls"] += 1

        if right_bound > best_value:
            heapq.heappush(
                pq,
                Node(level + 1, node.value, node.weight, right_bound, node.taken)
            )
        else:
            stats["nodes_pruned"] += 1

    return best_value, best_solution, stats
