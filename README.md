# RAS Matrix Balancing (Python)

## Overview

This repository provides a simple Python implementation of the **RAS method** (also known as *iterative proportional fitting*) for matrix balancing.

The script demonstrates how to adjust an **input–output (IO) table** so that:

- Row totals match specified targets (e.g. sector outputs)
- Column totals match specified targets (e.g. sector inputs)
- The internal structure (relative proportions) of the matrix is preserved

The example uses a **10-sector economic input–output table**, including structural zeros.

---

## What the Script Does

The script performs the following steps:

1. **Defines an input–output matrix**
   - 10 economic sectors (e.g. Agriculture, Manufacturing, Services)
   - Contains inter-sector flows
   - Includes structural zeros (no interaction between some sectors)

2. **Generates updated totals**
   - Simulates new macroeconomic information (e.g. revised national accounts)
   - Applies random growth factors to row and column sums

3. **Applies the RAS algorithm**
   - Iteratively rescales rows and columns
   - Converges to match the new totals
   - Prints iteration progress and error reduction

4. **Outputs results**
   - Initial matrix and totals
   - Target totals
   - Balanced matrix
   - Final row/column sums
   - Structure preservation metric

---

## The RAS Method (Brief Explanation)

The RAS method balances a matrix through iterative scaling:

- **R-step (Row scaling):** adjusts rows to match target row totals  
- **S-step (Column scaling):** adjusts columns to match target column totals  

These steps repeat until convergence is achieved.

The method is:

- Fast (vectorized operations in NumPy)
- Stable for non-negative matrices
- Widely used in:
  - Input–output economics
  - Supply–use tables
  - Transport modeling (OD matrices)

---

## How to Run

### 1. Requirements

- Python 3.8+
- NumPy
- Pandas

Install dependencies (if needed):

```bash
pip install numpy pandas
```

### 2. Script execution

```bash
py RAS.py
```
