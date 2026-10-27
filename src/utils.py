"""
utils.py
Common helpers for the knapsack project:
- value_of_solution, weight_of_solution
- validate_solution
- pretty_print_instance
- timing utilities
"""

from typing import List, Tuple, Iterable
import time
import functools

Item = Tuple[int, int, int]  # (value, weight, id)
Solution = List[int]  # list of item indices


def value_of_solution(items: List[Item], sol: Iterable[int]) -> int:
    """Return total value of solution (indices)."""
    return sum(items[i][0] for i in sol)


def weight_of_solution(items: List[Item], sol: Iterable[int]) -> int:
    """Return total weight of solution (indices)."""
    return sum(items[i][1] for i in sol)


def validate_solution(items: List[Item], sol: Iterable[int], capacity: int) -> bool:
    """Check capacity constraint and valid indices (no duplicates)."""
    sol_list = list(sol)
    if len(sol_list) != len(set(sol_list)):
        return False
    if any((i < 0 or i >= len(items)) for i in sol_list):
        return False
    return weight_of_solution(items, sol_list) <= capacity


def pretty_print_instance(items: List[Item], capacity: int, n_head: int = 10):
    """Pretty-print a small instance for debugging/inspection."""
    print(f"Capacity: {capacity}, n_items: {len(items)}")
    print("id\tvalue\tweight")
    for v, w, i in items[:n_head]:
        print(f"{i}\t{v}\t{w}")
    if len(items) > n_head:
        print("... (remaining items omitted)")


def timeit(func):
    """Decorator returning (runtime_seconds, returned_value) when called as func(*args, **kwargs)."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        res = func(*args, **kwargs)
        t1 = time.perf_counter()
        return (t1 - t0), res
    return wrapper
