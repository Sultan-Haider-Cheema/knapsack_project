"""
generator.py
Robust knapsack instance generator.

Features:
- Multiple distributions for values and weights: uniform, normal (truncated), poisson, exponential (rounded),
  and custom user-supplied arrays.
- Capacity control: capacity_ratio (fraction of total weight), absolute capacity, or target packing difficulty.
- Reproducible RNG via seed.
- Save / load instances to JSON or CSV.
- Return items as List of tuples (value:int, weight:int, id:int).
- Utilities for generating family of instances for experiments.
"""

from typing import List, Tuple, Optional, Sequence, Union, Dict, Any
import numpy as np
import random
import json
import csv
import os

Item = Tuple[int, int, int]  # (value, weight, id)


def _truncate_to_int_array(arr: np.ndarray, min_val=1, max_val=None) -> np.ndarray:
    """Round and clip numpy array to integer positive values."""
    arr = np.rint(arr).astype(int)
    arr[arr < min_val] = min_val
    if max_val is not None:
        arr[arr > max_val] = max_val
    return arr


def _rng(seed: Optional[int]):
    """Return numpy RandomState and python random seeded deterministically if seed provided."""
    if seed is not None:
        np_random = np.random.RandomState(seed)
        random.seed(seed)
    else:
        np_random = np.random.RandomState()
    return np_random


def generate_instance(
    n: int,
    capacity_ratio: float = 0.5,
    value_dist: str = "uniform",
    weight_dist: str = "uniform",
    value_params: Optional[Dict[str, Any]] = None,
    weight_params: Optional[Dict[str, Any]] = None,
    seed: Optional[int] = None,
    min_value: int = 1,
    max_value: Optional[int] = 1000,
    min_weight: int = 1,
    max_weight: Optional[int] = 1000,
    absolute_capacity: Optional[int] = None,
    ensure_integer: bool = True,
) -> Tuple[List[Item], int]:
    """
    Generate a single 0/1-knapsack instance.

    Args:
        n: number of items.
        capacity_ratio: fraction of total weight to set capacity to (ignored if absolute_capacity provided).
        value_dist: one of ['uniform','normal','poisson','exponential'] or 'custom' (then value_params['array'] required)
        weight_dist: same as value_dist but for weights.
        value_params: distribution parameters (e.g. {'low':1,'high':100} for uniform)
        weight_params: same for weights
        seed: optional RNG seed for reproducibility
        min_value/max_value/min_weight/max_weight: clipping for produced ints
        absolute_capacity: set exact capacity (overrides capacity_ratio)
        ensure_integer: round to ints if True

    Returns:
        (items, capacity) where items is list[(value, weight, id)]
    """
    if n <= 0:
        raise ValueError("n must be > 0")

    value_params = {} if value_params is None else dict(value_params)
    weight_params = {} if weight_params is None else dict(weight_params)

    prng = _rng(seed)

    def _sample(dist: str, params: Dict[str, Any], min_v: int, max_v: Optional[int]):
        if dist == "uniform":
            low = params.get("low", 1)
            high = params.get("high", 100)
            arr = prng.randint(low, high + 1, size=n)
        elif dist == "normal":
            mu = params.get("mu", 50)
            sigma = params.get("sigma", 15)
            arr = prng.normal(mu, sigma, size=n)
            arr = _truncate_to_int_array(arr, min_v, max_v)
            return arr
        elif dist == "poisson":
            lam = params.get("lam", 20)
            arr = prng.poisson(lam, size=n)
            arr = _truncate_to_int_array(arr, min_v, max_v)
            return arr
        elif dist == "exponential":
            scale = params.get("scale", 10.0)
            arr = prng.exponential(scale, size=n)
            arr = _truncate_to_int_array(arr, min_v, max_v)
            return arr
        elif dist == "custom":
            arr_src = params.get("array")
            if arr_src is None:
                raise ValueError("For 'custom' distribution provide 'array' in params")
            if isinstance(arr_src, Sequence):
                arr = np.array(arr_src)
                if len(arr) != n:
                    # if single value provided, broadcast
                    if arr.size == 1:
                        arr = np.full(n, arr.item())
                    else:
                        raise ValueError("Custom array length must be n")
            else:
                raise ValueError("custom 'array' must be a sequence")
        else:
            raise ValueError(f"Unknown distribution '{dist}'")
        if ensure_integer and not isinstance(arr, np.ndarray):
            arr = np.array(arr)
        if ensure_integer:
            arr = _truncate_to_int_array(arr, min_v, max_v)
        return arr

    values = _sample(value_dist, value_params, min_value, max_value)
    weights = _sample(weight_dist, weight_params, min_weight, max_weight)

    # ensure arrays are ints
    values = np.rint(values).astype(int)
    weights = np.rint(weights).astype(int)
    values[values < min_value] = min_value
    weights[weights < min_weight] = min_weight
    if max_value is not None:
        values[values > max_value] = max_value
    if max_weight is not None:
        weights[weights > max_weight] = max_weight

    total_weight = int(weights.sum())
    if absolute_capacity is not None:
        capacity = max(1, int(absolute_capacity))
    else:
        # capacity ratio sometimes set too small; ensure at least 1
        capacity = max(1, int(total_weight * capacity_ratio))

    items: List[Item] = [(int(values[i]), int(weights[i]), int(i)) for i in range(n)]
    return items, capacity


# Save / load utilities ----------------------------------------------------

def save_instance_json(items: List[Item], capacity: int, filepath: str):
    """Save knapsack instance to JSON (list of dicts + capacity)."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    payload = {
        "capacity": int(capacity),
        "items": [{"id": int(i[2]), "value": int(i[0]), "weight": int(i[1])} for i in items],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_instance_json(filepath: str) -> Tuple[List[Item], int]:
    """Load knapsack instance saved with save_instance_json."""
    with open(filepath, "r", encoding="utf-8") as f:
        payload = json.load(f)
    capacity = int(payload["capacity"])
    items = [(int(d["value"]), int(d["weight"]), int(d["id"])) for d in payload["items"]]
    return items, capacity


def save_instance_csv(items: List[Item], capacity: int, filepath: str):
    """Save knapsack instance in CSV: id,value,weight and capacity saved as first line (#capacity,<value>)."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["#capacity", capacity])
        writer.writerow(["id", "value", "weight"])
        for v, w, i in items:
            writer.writerow([i, v, w])


def load_instance_csv(filepath: str) -> Tuple[List[Item], int]:
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        capacity = None
        rows = []
        for row in reader:
            if not row:
                continue
            if row[0].startswith("#capacity"):
                # format: #capacity,123
                if len(row) >= 2 and row[1]:
                    capacity = int(row[1])
                continue
            # skip header like id,value,weight
            if row[0].lower() == "id":
                continue
            # otherwise parse id,value,weight
            if len(row) >= 3:
                idx = int(row[0])
                val = int(row[1])
                wt = int(row[2])
                rows.append((val, wt, idx))
        if capacity is None:
            raise ValueError("CSV instance missing capacity line '#capacity,<int>'")
        return rows, capacity


# Batch generator helper ---------------------------------------------------

def family_of_instances(
    ns: Sequence[int],
    repeats: int = 3,
    capacity_ratios: Union[Sequence[float], float] = 0.5,
    value_dist: str = "uniform",
    weight_dist: str = "uniform",
    value_params: Optional[Dict[str, Any]] = None,
    weight_params: Optional[Dict[str, Any]] = None,
    seed: Optional[int] = None,
):
    """
    Yield a family of instances for experiments. Yields tuples: (items, capacity, meta_dict)
    meta_dict contains {'n', 'seed', 'capacity_ratio', ...}
    """
    seed_base = seed if seed is not None else random.randint(0, 2**31 - 1)
    if isinstance(capacity_ratios, float):
        capacity_ratios = [capacity_ratios] * len(ns)
    for i_idx, n in enumerate(ns):
        for r in range(repeats):
            s = seed_base + i_idx * 1000 + r
            cap_ratio = capacity_ratios[i_idx] if i_idx < len(capacity_ratios) else capacity_ratios[-1]
            items, capacity = generate_instance(
                n=n,
                capacity_ratio=cap_ratio,
                value_dist=value_dist,
                weight_dist=weight_dist,
                value_params=value_params,
                weight_params=weight_params,
                seed=s,
            )
            meta = {"n": n, "repeat": r, "seed": s, "capacity_ratio": cap_ratio}
            yield items, capacity, meta

