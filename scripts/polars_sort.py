"""
Test script to verify if Polars DataFrame sorting with maintain_order=True
preserves the original order for equal values (stable sort).
"""

# python scripts/polars_sort.py

import random
from typing import List, Tuple

import numpy as np
import polars as pl


def test_basic_stability():
    """Test basic sort stability with simple data."""
    print("=" * 60)
    print("TEST 1: Basic Stability Test")
    print("=" * 60)

    # Create a DataFrame with duplicate values in the sort column
    df = pl.DataFrame(
        {
            "sort_key": [1, 2, 1, 2, 1, 2, 3, 3],
            "original_order": [0, 1, 2, 3, 4, 5, 6, 7],
            "data": ["a", "b", "c", "d", "e", "f", "g", "h"],
        }
    )

    print("Original DataFrame:")
    print(df)

    # Sort with maintain_order=True
    sorted_df = df.sort("sort_key", maintain_order=True)

    print("\nSorted DataFrame (maintain_order=True):")
    print(sorted_df)

    # Check if the original order is preserved for equal values
    for key in sorted_df["sort_key"].unique().sort():
        mask = sorted_df["sort_key"] == key
        original_orders = sorted_df.filter(mask)["original_order"].to_list()

        # Check if original orders are in ascending order (stable)
        is_stable = original_orders == sorted(original_orders)
        print(f"\nKey {key}: original_orders = {original_orders}, stable = {is_stable}")

    return sorted_df


def test_with_nulls():
    """Test sort stability with null values."""
    print("\n" + "=" * 60)
    print("TEST 2: Stability Test with Nulls")
    print("=" * 60)

    # Create a DataFrame with nulls
    df = pl.DataFrame(
        {
            "sort_key": [None, 1, None, 1, 2, None, 2, 1],
            "original_order": [0, 1, 2, 3, 4, 5, 6, 7],
            "data": ["a", "b", "c", "d", "e", "f", "g", "h"],
        }
    )

    print("Original DataFrame:")
    print(df)

    # Sort with maintain_order=True
    sorted_df = df.sort("sort_key", maintain_order=True)

    print("\nSorted DataFrame (maintain_order=True):")
    print(sorted_df)

    # Check stability for null values
    null_mask = sorted_df["sort_key"].is_null()
    null_orders = sorted_df.filter(null_mask)["original_order"].to_list()
    print(
        f"\nNull values: original_orders = {null_orders}, stable = {null_orders == sorted(null_orders)}"
    )

    # Check stability for non-null values
    for key in [1, 2]:
        mask = sorted_df["sort_key"] == key
        original_orders = sorted_df.filter(mask)["original_order"].to_list()
        is_stable = original_orders == sorted(original_orders)
        print(f"Key {key}: original_orders = {original_orders}, stable = {is_stable}")

    return sorted_df


def test_multiple_runs():
    """Test if sorting produces consistent results across multiple runs."""
    print("\n" + "=" * 60)
    print("TEST 3: Consistency Across Multiple Runs")
    print("=" * 60)

    # Create a DataFrame with many duplicates
    np.random.seed(42)
    n = 100
    df = pl.DataFrame(
        {
            "sort_key": np.random.choice([1, 2, 3, 4, 5], n),
            "original_order": list(range(n)),
            "data": [f"row_{i}" for i in range(n)],
        }
    )

    print(f"DataFrame shape: {df.shape}")
    print(f"Unique sort_key values: {df['sort_key'].unique().sort().to_list()}")

    # Sort multiple times and check consistency
    results = []
    for i in range(10):
        sorted_df = df.sort("sort_key", maintain_order=True)
        results.append(sorted_df["original_order"].to_list())

    # Check if all runs produce the same result
    all_same = all(r == results[0] for r in results)
    print(f"\nAll 10 runs produced the same result: {all_same}")

    if not all_same:
        print("WARNING: Different results detected across runs!")
        for i, result in enumerate(results[:3]):  # Show first 3 different results
            print(f"Run {i}: {result[:20]}...")  # Show first 20 elements

    return all_same


def test_lazy_vs_eager():
    """Test if lazy and eager evaluation produce the same stable sort."""
    print("\n" + "=" * 60)
    print("TEST 4: Lazy vs Eager Stability")
    print("=" * 60)

    # Create test data
    df = pl.DataFrame(
        {
            "sort_key": [2, 1, 2, 1, 3, 1, 3, 2],
            "original_order": [0, 1, 2, 3, 4, 5, 6, 7],
            "data": ["a", "b", "c", "d", "e", "f", "g", "h"],
        }
    )

    # Eager sort
    eager_sorted = df.sort("sort_key", maintain_order=True)

    # Lazy sort
    lazy_sorted = df.lazy().sort("sort_key", maintain_order=True).collect()

    print("Eager sort result:")
    print(eager_sorted)

    print("\nLazy sort result:")
    print(lazy_sorted)

    # Check if results are identical
    are_equal = eager_sorted.equals(lazy_sorted)
    print(f"\nEager and lazy sorts produce identical results: {are_equal}")

    return are_equal


def test_multi_column_sort():
    """Test stability when sorting by multiple columns."""
    print("\n" + "=" * 60)
    print("TEST 5: Multi-Column Sort Stability")
    print("=" * 60)

    df = pl.DataFrame(
        {
            "key1": [1, 1, 2, 2, 1, 2, 1, 2],
            "key2": ["a", "b", "a", "b", "a", "a", "b", "b"],
            "original_order": [0, 1, 2, 3, 4, 5, 6, 7],
            "data": [f"row_{i}" for i in range(8)],
        }
    )

    print("Original DataFrame:")
    print(df)

    # Sort by multiple columns with maintain_order=True
    sorted_df = df.sort(["key1", "key2"], maintain_order=True)

    print("\nSorted by ['key1', 'key2'] with maintain_order=True:")
    print(sorted_df)

    # Group by the sort keys and check stability within each group
    for (k1, k2), group_df in sorted_df.group_by(["key1", "key2"], maintain_order=True):
        orders = group_df["original_order"].to_list()
        is_stable = orders == sorted(orders)
        print(f"Group ({k1}, {k2}): orders = {orders}, stable = {is_stable}")

    return sorted_df


def test_large_dataset():
    """Test stability on a larger dataset with many duplicates."""
    print("\n" + "=" * 60)
    print("TEST 6: Large Dataset Stability Test")
    print("=" * 60)

    # Create a larger dataset
    n = 10000
    random.seed(42)

    # Create data with many duplicates (only 10 unique values for 10000 rows)
    df = pl.DataFrame(
        {"sort_key": [random.randint(0, 9) for _ in range(n)], "original_order": list(range(n))}
    )

    print(f"DataFrame shape: {df.shape}")
    print(f"Unique sort_key values: {sorted(df['sort_key'].unique().to_list())}")

    # Sort with maintain_order=True
    sorted_df = df.sort("sort_key", maintain_order=True)

    # Check stability for each key value
    all_stable = True
    for key in range(10):
        mask = sorted_df["sort_key"] == key
        original_orders = sorted_df.filter(mask)["original_order"].to_list()
        is_stable = original_orders == sorted(original_orders)

        if not is_stable:
            all_stable = False
            print(f"Key {key}: NOT STABLE! First few orders: {original_orders[:10]}...")

    print(f"\nAll groups maintain stable order: {all_stable}")

    # Additional check: verify the sort actually worked
    sort_keys = sorted_df["sort_key"].to_list()
    is_sorted = sort_keys == sorted(sort_keys)
    print(f"Sort keys are properly sorted: {is_sorted}")

    return all_stable


def main():
    """Run all stability tests."""
    print("\n" + "=" * 60)
    print("POLARS SORT STABILITY TEST SUITE")
    print(f"Polars version: {pl.__version__}")
    print("=" * 60)

    # Run all tests
    results = []

    # Test 1: Basic stability
    test_basic_stability()

    # Test 2: Stability with nulls
    test_with_nulls()

    # Test 3: Consistency across runs
    consistent = test_multiple_runs()
    results.append(("Consistency across runs", consistent))

    # Test 4: Lazy vs Eager
    lazy_eager_same = test_lazy_vs_eager()
    results.append(("Lazy vs Eager identical", lazy_eager_same))

    # Test 5: Multi-column sort
    test_multi_column_sort()

    # Test 6: Large dataset
    large_stable = test_large_dataset()
    results.append(("Large dataset stability", large_stable))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")

    print("\nNOTE: Check the detailed output above to see if sort is stable")
    print("for individual groups within each test.")

    # Final verdict
    all_passed = all(r[1] for r in results)
    if all_passed:
        print("\n✓ Overall: Polars sort with maintain_order=True appears to be STABLE")
    else:
        print("\n✗ Overall: Some stability issues detected. Check details above.")


if __name__ == "__main__":
    main()


import polars as pl

# Make a DataFrame with a key that has ties and a column capturing original order.
df = pl.DataFrame(
    {
        "key": [2, 1, 2, 1, 2, 1],  # ties on 1 and 2
        "value": ["a", "b", "c", "d", "e", "f"],  # we'll track relative order within each key
    }
).with_row_index(
    name="orig_pos"
)  # 0..n-1 original row numbers

# print("Original:")
# print(df)

# Unstable (default) vs. stable sort on the single key.
unstable = df.sort("key", maintain_order=False)
stable = df.sort("key", maintain_order=True)

# print("\nUnstable sort (maintain_order=False):")
# print(unstable.select("key", "value", "orig_pos"))

# print("\nStable sort (maintain_order=True):")
# print(stable.select("key", "value", "orig_pos"))


# Programmatic check: for each key, verify that the 'orig_pos' ordering is increasing.
def is_stable(sorted_df):
    ok = True
    for k, group in sorted_df.group_by("key", maintain_order=True):
        # extract original positions in the order they appear after sort
        pos = group["orig_pos"].to_list()
        if pos != sorted(pos):
            print(f"Key {k}: order within ties changed -> {pos}")
            ok = False
    return ok


print("\nStability check (should be False, then True):")
print("unstable:", is_stable(unstable))
print("stable  :", is_stable(stable))

# Extra: demonstrate multi-key equivalence.
# Sorting by key stably is equivalent to a multi-key sort where the tie-breaker is orig_pos.
stable_via_tiebreak = df.sort(["key", "orig_pos"])
# print("\nStable via explicit tie-breaker (key, orig_pos):")
# print(stable_via_tiebreak.select("key", "value", "orig_pos"))

assert (
    stable.select("value").to_series().to_list()
    == stable_via_tiebreak.select("value").to_series().to_list()
)
print("\nAssertion passed: maintain_order=True == adding original-position as a tiebreaker.")


import polars as pl

# 1. Create sample data with a clear original order marker
data = {
    "group_key": ["a", "a", "b", "a", "b", "a"],
    "original_order": [0, 1, 2, 3, 4, 5],
    "value": ["apple", "ant", "bear", "avocado", "bat", "apricot"],
}
df = pl.DataFrame(data)

# print("--- Original DataFrame ---")
# print(df)

# --- Test Case: maintain_order=True ---
# Correction: Use .implode() instead of .list() for aggregation.
# print("\n--- Test with maintain_order=True ---")
result_maintain_order = df.group_by("group_key", maintain_order=True).agg(
    pl.col("original_order").implode().alias("order_list"),
    pl.col("value").implode().alias("value_list"),
)
# print(result_maintain_order)

# --- Verification Logic ---
group_a_data = result_maintain_order.filter(pl.col("group_key") == "a")
observed_order = group_a_data.get_column("order_list")[0].to_list()
expected_order = [0, 1, 3, 5]

print(f"\n--- Verification for Group 'a' ---")
print(f"Expected intra-group order: {expected_order}")
print(f"Observed intra-group order: {observed_order}")

assert observed_order == expected_order, "Intra-group order failed verification!"
print("Verification successful: Intra-group order is maintained.")
