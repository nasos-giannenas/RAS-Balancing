# RAS Matrix Balancing (Python)

## Overview

This repository provides a simple Python implementation of the **RAS method** (also known as *iterative proportional fitting*) for matrix balancing.

The script demonstrates how to adjust an **input–output (IO) table** so that:

- Row totals match specified targets (e.g. sector outputs)
- Column totals match specified targets (e.g. sector inputs)
- The internal structure (relative proportions) of the matrix is preserved

The matrix and target totals are read from an Excel workbook.

---

## What the Script Does

The script performs the following steps:

1. **Reads the initial matrix to be balanced**
   - Reads the worksheet `IO_Matrix`
   - Located in:
     ```
     ../input/io_input_with_targets.xlsx
     ```
   - Contains inter-sector flows
   - Includes structural zeros (no interaction between some sectors)

2. **Reads target totals**
   - Reads the worksheet `Targets`
   - Uses supplied row and column totals
   - No target generation is performed within the script

3. **Applies the RAS algorithm**
   - Iteratively rescales rows and columns
   - Converges to match the target totals
   - Prints iteration progress and error reduction

4. **Outputs results**
   - Initial matrix and totals
   - Target totals
   - Balanced matrix
   - Final row/column sums
   - Structure preservation metric

5. **Saves the balanced matrix**
   - Automatically creates the output folder if it does not exist
   - Writes the balanced matrix to:
     ```
     ../output/balanced_output.xlsx
     ```
   - Uses worksheet:
     ```
     Balanced_Matrix
     ```

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

Let:

- `A = [a(i,j)]` be the original matrix
- `r*` be the target row totals
- `c*` be the target column totals

The goal is to find a balanced matrix `X` such that:

```
sum_j X(i,j) = r*(i)
sum_i X(i,j) = c*(j)
```

### Row Scaling

For each row `i`:

```
R(i) = r*(i) / sum_j X(i,j)
```

Update the row:

```
X(i,j) = R(i) * X(i,j)
```

### Column Scaling (S-step)

For each column `j`:

```
S(j) = c*(j) / sum_i X(i,j)
```

Update the column:

```
X(i,j) = X(i,j) * S(j)
```

### Convergence

Iterate until convergence is reached:

```
max |CurrentRowTotal - TargetRowTotal| < ε,
max |CurrentColumnTotal - TargetColumnTotal| < ε
```

where `ε` is a user-defined residual.

### Final Solution

After convergence:

```
X = R * A * S
```

where:

- `R` is a diagonal matrix of row multipliers
- `S` is a diagonal matrix of column multipliers

Each cell satisfies:

```
X(i,j) = R(i) * A(i,j) * S(j)
```

---

## Input File Structure

The script expects an Excel workbook located at:

```
../input/io_input_with_targets.xlsx
```

### Worksheet: `IO_Matrix`

Contains the matrix to be balanced.

### Worksheet: `Targets`

Contains the target totals with the following fields:

- `Sector`
- `TargetRowTotal`
- `TargetColTotal`

The sum of all target row totals must equal the sum of all target column totals.

---

## Output File

After a successful run, the script creates:

```
../output/balanced_output.xlsx
```

The balanced matrix is written to the worksheet:

```
Balanced_Matrix
```

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

### 2. Prepare/modify the Input File

Place:

```
io_input_with_targets.xlsx
```

inside the `input` folder.

Expected structure:

```text
project/
│
├── input/
│   └── io_input_with_targets.xlsx
│
├── output/
│
└── src/
    └── RAS.py
```

### 3. Script execution

Navigate to the :open_file_folder: `src` folder and then run the following command:

```bash
py RAS.py
```

The script will:

1. Read the IO matrix from `../input/io_input_with_targets.xlsx`
2. Read the target totals from the `Targets` worksheet
3. Perform RAS balancing
4. Create `../output` if it does not already exist
5. Save the balanced matrix to:

```text
../output/balanced_output.xlsx
```