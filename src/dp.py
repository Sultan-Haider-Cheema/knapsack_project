"""
dp.py
Dynamic Programming algorithms for 0/1 Knapsack:

1. dp_bottom_up
2. dp_bottom_up_reconstruct
3. dp_top_down
4. dp_top_down_reconstruct

Each algorithm returns:
    (best_value, selected_items)
"""

from typing import List, Tuple, Dict
Item = Tuple[int, int, int]    # (value, weight, id)


# =============================================================
# 1. DP BOTTOM-UP  (table of size n x capacity)
# =============================================================
def dp_bottom_up(items: List[Item], capacity: int) -> Tuple[int, List[int]]:
    n = len(items)

    # dp[i][w] = best value using first i items with weight limit w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        v, w, idx = items[i-1]
        for cap in range(0, capacity + 1):
            if w > cap:
                dp[i][cap] = dp[i-1][cap]
            else:
                dp[i][cap] = max(dp[i-1][cap], v + dp[i-1][cap - w])

    return dp[n][capacity], []   # no reconstruction


# =============================================================
# 2. DP BOTTOM-UP WITH RECONSTRUCTION
# =============================================================
def dp_bottom_up_reconstruct(items: List[Item], capacity: int) -> Tuple[int, List[int], List[List[int]]]:
    n = len(items)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # fill table
    for i in range(1, n + 1):
        v, w, idx = items[i-1]
        for cap in range(capacity + 1):
            if w > cap:
                dp[i][cap] = dp[i - 1][cap]
            else:
                dp[i][cap] = max(dp[i - 1][cap], v + dp[i - 1][cap - w])

    # reconstruct
    sol = []
    cap = capacity
    i = n

    while i > 0:
        v, w, idx = items[i-1]
        if dp[i][cap] == dp[i-1][cap]:    # item not taken
            i -= 1
        else:                             # item taken
            sol.append(idx)
            cap -= w
            i -= 1

    sol.reverse()
    return dp[n][capacity], sol, dp


# =============================================================
# 3. DP TOP-DOWN WITH MEMOIZATION
# =============================================================
def dp_top_down(items: List[Item], capacity: int) -> Tuple[int, List[int]]:
    from functools import lru_cache

    n = len(items)

    @lru_cache(None)
    def solve(i, cap):
        if i == n or cap <= 0:
            return 0

        v, w, idx = items[i]

        # skip item
        best = solve(i+1, cap)

        # take item if possible
        if w <= cap:
            best = max(best, v + solve(i+1, cap - w))

        return best

    best_value = solve(0, capacity)
    return best_value, []   # reconstruction handled below


# =============================================================
# 4. DP TOP-DOWN WITH RECONSTRUCTION
# =============================================================
def dp_top_down_reconstruct(items: List[Item], capacity: int) -> Tuple[int, List[int]]:
    from functools import lru_cache

    n = len(items)

    @lru_cache(None)
    def solve(i, cap):
        if i == n or cap <= 0:
            return 0

        v, w, idx = items[i]

        # skip
        skip_val = solve(i+1, cap)

        # take (if possible)
        if w <= cap:
            take_val = v + solve(i+1, cap - w)
            return max(skip_val, take_val)
        else:
            return skip_val

    best_value = solve(0, capacity)

    # reconstruction
    sol = []
    i, cap = 0, capacity

    while i < n and cap > 0:
        v, w, idx = items[i]

        if w <= cap:
            # if taking gives optimal
            if solve(i, cap) == v + solve(i+1, cap - w):
                sol.append(idx)
                cap -= w
                i += 1
                continue

        # otherwise: skip
        i += 1

    return best_value, sol
