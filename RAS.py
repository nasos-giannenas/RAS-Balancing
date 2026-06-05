import numpy as np
import pandas as pd

# -------------------------------
# RAS FUNCTION
# -------------------------------

def ras_balance(matrix, target_rows, target_cols, max_iter=500, tol=1e-12, verbose=True):
    A = np.array(matrix, dtype=float)
    r_target = np.array(target_rows, dtype=float)
    c_target = np.array(target_cols, dtype=float)

    if abs(r_target.sum() - c_target.sum()) > tol:
        raise ValueError("Row and column totals must match")

    for i in range(max_iter):
        # Row scaling
        row_sums = A.sum(axis=1)
        row_factors = np.divide(r_target, row_sums, out=np.ones_like(row_sums), where=row_sums != 0)
        A *= row_factors[:, np.newaxis]

        # Column scaling
        col_sums = A.sum(axis=0)
        col_factors = np.divide(c_target, col_sums, out=np.ones_like(col_sums), where=col_sums != 0)
        A *= col_factors

        # Convergence check
        row_diff = np.max(np.abs(A.sum(axis=1) - r_target))
        col_diff = np.max(np.abs(A.sum(axis=0) - c_target))
        error = max(row_diff, col_diff)

        if verbose:
            print(f"Iter {i+1:3d} | error = {error:.3e} | target = {tol:.1e}")

        if error < tol:
            print(f"\n✅ Converged in {i+1} iterations (final error = {error:.3e})")
            return A

    print(f"⚠️ Warning: did not converge (final error = {error:.3e})")
    return A



# -------------------------------
# 1. DEFINE 10-SECTOR IO MATRIX
# -------------------------------
sectors = [
    "Agriculture", "Mining", "Manufacturing", "Utilities",
    "Construction", "Trade", "Transport", "Finance",
    "Public", "Services"
]

# Realistic-ish IO structure with zeros (structural gaps)
M = np.array([
    [120,   0,  80,  0,  40,  60,   0,   0,   0,  50],
    [  0, 150, 120, 60,  80,   0,   0,   0,   0,  40],
    [ 60, 200, 300,120, 150, 180, 130, 110,   0, 200],
    [  0,  50,  90,140,  70,  60, 100,  80,   0, 120],
    [ 40,  30, 110, 50, 200, 140, 120,   0,   0, 100],
    [ 20,   0, 150, 40, 100, 180,  90,  60,   0, 130],
    [  0,   0, 130, 90, 110, 120, 200, 100,   0, 150],
    [  0,   0,  90, 70,  80,  60, 110, 180,   0, 140],
    [  0,   0,   0,  0,   0,  50,  40,  60, 150, 200],
    [ 30,  20, 140,110,  90, 130, 120, 150,   0, 220]
], dtype=float)

df_initial = pd.DataFrame(M, index=sectors, columns=sectors)

print("\n=== Initial Matrix ===")
print(df_initial)

print("\nRow sums:", df_initial.sum(axis=1).values)
print("Column sums:", df_initial.sum(axis=0).values)


# -------------------------------
# 2. CREATE TARGET TOTALS
# -------------------------------
row_sums = M.sum(axis=1)
col_sums = M.sum(axis=0)

# Apply macro adjustment (±10–20%)
np.random.seed(42)

row_growth = np.random.uniform(0.9, 1.2, size=len(row_sums))
col_growth = np.random.uniform(0.9, 1.2, size=len(col_sums))

target_rows = row_sums * row_growth
target_cols = col_sums * col_growth

# Scale columns to ensure totals match exactly
target_cols *= target_rows.sum() / target_cols.sum()

print("\n=== Target Totals ===")
print("Target row sums:", np.round(target_rows, 2))
print("Target col sums:", np.round(target_cols, 2))


# -------------------------------
# 3. APPLY RAS
# -------------------------------
balanced = ras_balance(M, target_rows, target_cols, verbose=True)

df_balanced = pd.DataFrame(balanced, index=sectors, columns=sectors)

print("\n=== Balanced Matrix ===")
print(df_balanced.round(2))

print("\nBalanced row sums:", df_balanced.sum(axis=1).round(2).values)
print("Balanced col sums:", df_balanced.sum(axis=0).round(2).values)


# -------------------------------
# 4. CHECK STRUCTURE PRESERVATION
# -------------------------------
ratio_before = M / M.sum()
ratio_after = balanced / balanced.sum()

diff = np.abs(ratio_before - ratio_after).mean()

print("\n=== Structure Preservation ===")
print(f"Average proportional change: {diff:.6f}")