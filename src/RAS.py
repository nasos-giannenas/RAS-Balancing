import numpy as np
import pandas as pd
import os

# -------------------------------
# RAS FUNCTION
# -------------------------------

def ras_balance(matrix, target_rows, target_cols, max_iter=500, tol=1e-12, verbose=True):
    A = np.array(matrix, dtype=float)
    r_target = np.array(target_rows, dtype=float)
    c_target = np.array(target_cols, dtype=float)

    if abs(r_target.sum() - c_target.sum()) > tol:
        raise ValueError("Row and column totals must match")

    print('   ---   Balancing   ---   ')
    print('')
    print('Iteration| Error             | Target Error')
    print('')

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
# 1. READ INPUT FROM EXCEL
# -------------------------------

input_file = "../input/io_input_with_targets.xlsx"

# IO matrix sheet
df_initial = pd.read_excel(
    input_file,
    sheet_name="IO_Matrix",
    index_col=0
)

# Targets sheet
targets_df = pd.read_excel(
    input_file,
    sheet_name="Targets"
)

M = df_initial.values
sectors = df_initial.index.tolist()


# -------------------------------
# 2. READ TARGET TOTALS
# -------------------------------

target_rows = targets_df["TargetRowTotal"].values
target_cols = targets_df["TargetColTotal"].values

print("\n=== Target Totals ===")
print("Target row sums:", np.round(target_rows, 2))
print("Target col sums:", np.round(target_cols, 2))
print('')


# -------------------------------
# 3. APPLY RAS
# -------------------------------
balanced = ras_balance(M, target_rows, target_cols, verbose=True)

df_balanced = pd.DataFrame(balanced, index=sectors, columns=sectors)


# Save balanced matrix
output_dir = "../output"
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "balanced_output.xlsx")

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    df_balanced.to_excel(
        writer,
        sheet_name="Balanced_Matrix"
    )


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

# print("\n=== Structure Preservation ===")
# print(f"Average proportional change: {diff:.6f}")



print('')
print(f"\nBalanced matrix written to output/ folder")
