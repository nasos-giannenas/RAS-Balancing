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


## Mathematical Formulation

Let

$$
A=[a_{ij}]
$$

be the original input-output matrix,

$$
r^{*} = (r_1^{*}, r_2^{*}, \ldots, r_m^{*})
$$

the target row totals, and

$$
c^{*} = (c_1^{*}, c_2^{*}, \ldots, c_n^{*})
$$

the target column totals.

The objective is to find a balanced matrix

$$
X=[x_{ij}]
$$

such that

$$
\sum_j x_{ij}=r_i^{*}
$$

and

$$
\sum_i x_{ij}=c_j^{*}.
$$

### Row Scaling (R-step)

At iteration $k$, the row adjustment factors are

$$
R_i^{(k)}
=
\frac{r_i^{*}}
{\sum_j x_{ij}^{(k-1)}}
$$

Each row is scaled according to

$$
x_{ij}^{(k+\frac12)}
=
R_i^{(k)}
x_{ij}^{(k-1)}
$$

### Column Scaling (S-step)

After row adjustment, column scaling factors are

$$
S_j^{(k)}
=
\frac{c_j^{*}}
{\sum_i x_{ij}^{(k+\frac12)}}
$$

Each column is then scaled as

$$
x_{ij}^{(k)}
=
x_{ij}^{(k+\frac12)}
S_j^{(k)}
$$

### Final Solution

After convergence, the balanced matrix can be written as

$$
X = RAS
$$

where:

- $R$ is the diagonal matrix of row scaling factors.
- $S$ is the diagonal matrix of column scaling factors.

Each element of the balanced matrix satisfies

$$
x_{ij}
=
r_i\,a_{ij}\,s_j
$$

### Convergence Criterion

The iterations continue until

$$
\max_i
\left|
\sum_j x_{ij}-r_i^{*}
\right|
<
\varepsilon
$$

and

$$
\max_j
\left|
\sum_i x_{ij}-c_j^{*}
\right|
<
\varepsilon.
$$

In other words, the algorithm alternates between row scaling and column scaling until all margins match the specified targets within a predefined tolerance.




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

Navigate to the :open_file_folder: `src` folder and then run the following command:

```bash
py RAS.py
```
