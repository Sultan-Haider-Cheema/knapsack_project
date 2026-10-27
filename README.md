# Empirical Evaluation of Knapsack Algorithms

This project presents a rigorous empirical evaluation of exact and approximation
algorithms for the **0/1 Knapsack Problem**. The study combines controlled
synthetic experiments with established **OR-Library (MKNAP1)** benchmark
instances that provide known optimal solutions.

All results, figures, and numerical values reported in the accompanying PDF
report are **directly generated from the provided Jupyter notebooks**, ensuring
full reproducibility.

---

## Project Structure

```
knapsack_project/
│
├── src/
│   ├── brute_force.py
│   ├── greedy.py
│   ├── dp.py
│   ├── branch_and_bound.py
│   ├── utils.py
│   └── generator.py
│
├── notebooks/
│   ├── analysis.ipynb
│   ├── benchmarks.ipynb
│   └── benchmarks/
│       └── orlib/
│           └── mknap1.txt
│
├── report/
│   └── report.pdf
│
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.9 or higher
- pip

---

## Installation

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

---

## Running the Experiments

Launch Jupyter:

```bash
jupyter notebook
```

Run the notebooks in this order:

1. `notebooks/analysis.ipynb` — synthetic experiments  
2. `notebooks/benchmarks.ipynb` — OR-Library benchmarks

---

## Reproducibility

- Fixed random seeds
- No external solvers
- All figures generated directly from notebooks

---

## Author

Muhammad Sultan Haidar Cheema  
Advanced Algorithms — Master’s Project (2025–2026)
