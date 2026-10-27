"""
brute_force.py
Systematic brute-force search for the 0/1 knapsack problem.

Features:
- Two search modes: 'combinations' (default), 'bitmask'
- Pruning: weight > capacity → skip early
- Returns: (best_value, best_solution_indices)
- Deterministic, used as correctness oracle for small instances
"""

from itertools import combinations
from typing import List, Tuple, Iterable, Optional

Item = Tuple[int, int, int]  # (value, weight, id)


def brute_force(
    items: List[Item],
    capacity: int,
    method: str = "combinations",
    enable_pruning: bool = True,
) -> Tuple[int, List[int]]:
    """
    Systematically tries all subsets to find the optimal solution.
    ONLY suitable for small n (<= 25).

    Args:
        items: list of (value, weight, id)
        capacity: max capacity
        method: 'combinations' or 'bitmask'
        enable_pruning: skip subsets whose weight exceeds capacity early

    Returns:
        best_value, best_solution (list of indices)
    """
    n = len(items)
    if n == 0:
        return 0, []

    if method == "combinations":
        return _bruteforce_combinations(items, capacity, enable_pruning)
    elif method == "bitmask":
        return _bruteforce_bitmask(items, capacity, enable_pruning)
    else:
        raise ValueError("method must be 'combinations' or 'bitmask'")


# -------------------------------------------------------------------------
# Combinations-based brute force
# -------------------------------------------------------------------------

def _bruteforce_combinations(
    items: List[Item], capacity: int, enable_pruning: bool
) -> Tuple[int, List[int]]:
    n = len(items)
    best_val = 0
    best_set: List[int] = []

    for r in range(n + 1):
        # combinations of size r
        for subset in combinations(range(n), r):
            if enable_pruning:
                # prune if too heavy
                total_w = 0
                valid = True
                for i in subset:
                    total_w += items[i][1]
                    if total_w > capacity:
                        valid = False
                        break
                if not valid:
                    continue
            else:
                total_w = sum(items[i][1] for i in subset)

            if total_w <= capacity:
                total_v = sum(items[i][0] for i in subset)
                if total_v > best_val:
                    best_val = total_v
                    best_set = list(subset)

    return best_val, best_set


# -------------------------------------------------------------------------
# Bitmask-based brute force
# -------------------------------------------------------------------------

def _bruteforce_bitmask(
    items: List[Item], capacity: int, enable_pruning: bool
) -> Tuple[int, List[int]]:
    n = len(items)
    best_val = 0
    best_set: List[int] = []

    for mask in range(1 << n):
        total_w = 0
        total_v = 0
        subset = []

        for i in range(n):
            if mask & (1 << i):
                w = items[i][1]
                v = items[i][0]
                total_w += w
                if enable_pruning and total_w > capacity:
                    break  # prune early
                subset.append(i)
                total_v += v

        if total_w <= capacity and total_v > best_val:
            best_val = total_v
            best_set = subset.copy()

    return best_val, best_set
