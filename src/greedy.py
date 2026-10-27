"""
greedy.py
Three greedy heuristics for 0/1 knapsack:

1. Greedy-by-Value        (descending value)
2. Greedy-by-Weight       (ascending weight)
3. Greedy-by-Ratio        (descending value/weight)

Notes:
- These heuristics are NOT optimal for 0/1 knapsack.
- They run in O(n log n) due to sorting.
- Used as fast baselines for comparison with brute-force, DP, BnB, etc.
"""

from typing import List, Tuple

Item = Tuple[int, int, int]  # (value, weight, id)


def greedy_by_value(items: List[Item], capacity: int) -> Tuple[int, List[int]]:
    """Pick items in descending order of value."""
    sorted_items = sorted(items, key=lambda x: x[0], reverse=True)

    total_w, total_v = 0, 0
    sol = []

    for v, w, idx in sorted_items:
        if total_w + w <= capacity:
            sol.append(idx)
            total_w += w
            total_v += v

    return total_v, sol


def greedy_by_weight(items: List[Item], capacity: int) -> Tuple[int, List[int]]:
    """Pick items in ascending order of weight (lightest first)."""
    sorted_items = sorted(items, key=lambda x: x[1])  # smallest weight first

    total_w, total_v = 0, 0
    sol = []

    for v, w, idx in sorted_items:
        if total_w + w <= capacity:
            sol.append(idx)
            total_w += w
            total_v += v

    return total_v, sol


def greedy_by_ratio(items: List[Item], capacity: int) -> Tuple[int, List[int]]:
    """Pick items by highest value/weight ratio."""
    sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)

    total_w, total_v = 0, 0
    sol = []

    for v, w, idx in sorted_items:
        if total_w + w <= capacity:
            sol.append(idx)
            total_w += w
            total_v += v

    return total_v, sol


def greedy_all(items: List[Item], capacity: int):
    """
    Convenience wrapper returning all three greedy results.
    Returns dict:
    {
        "value": (best_value, solution),
        "weight": (best_value, solution),
        "ratio": (best_value, solution),
    }
    """
    return {
        "value": greedy_by_value(items, capacity),
        "weight": greedy_by_weight(items, capacity),
        "ratio": greedy_by_ratio(items, capacity),
    }

