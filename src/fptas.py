"""
fptas.py
Fully Polynomial-Time Approximation Scheme (FPTAS)
for 0/1 Knapsack.

Steps:
1. Scale down values using K = ε * Vmax / n
2. Apply DP on scaled values
3. Reconstruct solution
Guarantee: (1 - ε)-approximation
"""

from typing import List, Tuple
import math

Item = Tuple[int, int, int]   # (value, weight, id)


def fptas_knapsack(items: List[Item], capacity: int, eps: float = 0.1):
    n = len(items)
    values = [v for (v, w, idx) in items]

    Vmax = max(values)
    K = eps * Vmax / n

    # Scale values
    scaled_values = [math.floor(v / K) for (v, w, idx) in items]
    sum_scaled = sum(scaled_values)

    # -------------------------------------------------------------
    # DP on scaled values
    # dp[i][sv] = minimum weight to achieve scaled value 'sv'
    # -------------------------------------------------------------
    INF = 10**15
    dp = [ [INF] * (sum_scaled + 1) for _ in range(n + 1) ]
    dp[0][0] = 0

    for i in range(1, n + 1):
        v, w, idx = items[i - 1]
        sv = scaled_values[i - 1]

        for tot_v in range(sum_scaled + 1):
            # option 1: don't take item
            dp[i][tot_v] = dp[i - 1][tot_v]

            # option 2: take item if possible
            if tot_v - sv >= 0:
                dp[i][tot_v] = min(
                    dp[i][tot_v],
                    dp[i - 1][tot_v - sv] + w
                )

    # -------------------------------------------------------------
    # Find best achievable scaled value within capacity
    # -------------------------------------------------------------
    best_scaled = 0
    for tot_v in range(sum_scaled + 1):
        if dp[n][tot_v] <= capacity:
            best_scaled = tot_v

    # -------------------------------------------------------------
    # Reconstruct solution
    # -------------------------------------------------------------
    sol = []
    i = n
    sv = best_scaled

    while i > 0:
        if dp[i][sv] == dp[i - 1][sv]:
            # item not taken
            i -= 1
        else:
            # item taken
            sol.append(items[i - 1][2])  # original ID
            sv -= scaled_values[i - 1]
            i -= 1

    sol.reverse()

    # Compute true value
    true_value = sum(items[i][0] for i in sol)
    return true_value, sol
