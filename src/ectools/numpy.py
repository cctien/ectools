from collections.abc import Sequence

import numpy as np

from .math import number_like


def fill_diagonal(
    x: np.ndarray, value: number_like, *, offset: int = 0, axis1: int = -2, axis2: int = -1
) -> np.ndarray:
    x = x.copy()
    diag = np.diagonal(x, offset=offset, axis1=axis1, axis2=axis2)
    diag.setflags(write=True)
    diag[...] = value
    return x


def np_prng_key(random_seed: int | np.random.SeedSequence | None) -> np.random.SeedSequence:
    if isinstance(random_seed, np.random.SeedSequence):
        return random_seed
    return np.random.SeedSequence(random_seed)


def np_prng(random_seed: int | np.random.SeedSequence | None) -> np.random.Generator:
    return np.random.default_rng(np_prng_key(random_seed))


def np_generalized_concat(arrays: Sequence[np.ndarray], axis: int = 0, **kwargs) -> np.ndarray:
    try:
        return np.concatenate(arrays, axis=axis, **kwargs)
    except ValueError:
        return np.stack(arrays, axis=axis, **kwargs)


# np_prng: Callable[[int | np.random.SeedSequence | None], np.random.Generator] = cmp(
#     np.random.default_rng, np_prng_key
# )


def test_fill_diagonal_all_dimensions():
    """Comprehensive test suite for fill_diagonal with 2D and higher-dimensional arrays."""

    print("Testing fill_diagonal with 2D and higher-dimensional arrays...\n")
    tests_passed = 0
    tests_failed = 0

    # ==================== 2D ARRAY TESTS ====================
    print("=" * 60)
    print("2D ARRAY TESTS")
    print("=" * 60 + "\n")

    # Test 1: Basic 2D square matrix
    print("Test 1: Basic 2D square matrix")
    try:
        x = np.ones((3, 3))
        result = fill_diagonal(x, 0)
        expected = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
        assert np.array_equal(result, expected), "Arrays not equal"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 2: 2D non-square matrix (more columns)
    print("Test 2: 2D non-square matrix (more columns)")
    try:
        x = np.ones((3, 5))
        result = fill_diagonal(x, 0)
        expected = np.array([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1]])
        assert np.array_equal(result, expected), "Arrays not equal"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 3: 2D non-square matrix (more rows)
    print("Test 3: 2D non-square matrix (more rows)")
    try:
        x = np.ones((5, 3))
        result = fill_diagonal(x, 0)
        expected = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0], [1, 1, 1], [1, 1, 1]])
        assert np.array_equal(result, expected), "Arrays not equal"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 4: 2D positive offset
    print("Test 4: 2D positive offset")
    try:
        x = np.ones((4, 4))
        result = fill_diagonal(x, 0, offset=1)
        expected = np.array([[1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]])
        assert np.array_equal(result, expected), "Arrays not equal"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 5: 2D negative offset
    print("Test 5: 2D negative offset")
    try:
        x = np.ones((4, 4))
        result = fill_diagonal(x, 0, offset=-1)
        expected = np.array([[1, 1, 1, 1], [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1]])
        assert np.array_equal(result, expected), "Arrays not equal"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 6: 2D multiple offsets
    print("Test 6: 2D multiple offsets")
    try:
        x = np.ones((5, 5))

        for offset in [-2, -1, 0, 1, 2]:
            result = fill_diagonal(x, 0, offset=offset)
            diag = np.diagonal(result, offset=offset)
            assert np.all(diag == 0), f"Offset {offset} failed"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 7: 2D immutability
    print("Test 7: 2D immutability (original array not modified)")
    try:
        x = np.ones((3, 3))
        original = x.copy()
        result = fill_diagonal(x, 0)
        assert np.array_equal(x, original), "Original array was modified"
        assert result is not x, "Result is the same object as input"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 8: 2D different dtypes
    print("Test 8: 2D different data types")
    try:
        for dtype in [np.float32, np.float64, np.int32, np.int64, np.bool_]:
            x = np.ones((3, 3), dtype=dtype)
            result = fill_diagonal(x, 0)
            assert result.dtype == dtype, f"Wrong dtype: {result.dtype} vs {dtype}"
            assert np.all(result.diagonal() == 0), f"Diagonal not filled for dtype {dtype}"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 9: 2D fill with different values
    print("Test 9: 2D fill with different values")
    try:
        x = np.ones((3, 3))

        # Fill with integer
        result = fill_diagonal(x, 5)
        assert np.all(result.diagonal() == 5), "Integer fill failed"

        # Fill with float
        result = fill_diagonal(x, 3.14)
        assert np.allclose(result.diagonal(), 3.14), "Float fill failed"

        # Fill with negative
        result = fill_diagonal(x, -7)
        assert np.all(result.diagonal() == -7), "Negative fill failed"

        # Fill with boolean
        x_bool = np.ones((3, 3), dtype=bool)
        result = fill_diagonal(x_bool, False)
        assert np.all(result.diagonal() == False), "Boolean fill failed"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 10: 2D large offset (beyond matrix dimensions)
    print("Test 10: 2D large offset (beyond matrix dimensions)")
    try:
        x = np.ones((3, 3))
        result = fill_diagonal(x, 0, offset=5)
        # Should not crash, result should equal original
        assert np.array_equal(result, x), "Array changed unexpectedly"

        result = fill_diagonal(x, 0, offset=-5)
        assert np.array_equal(result, x), "Array changed unexpectedly"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 11: 2D edge case - 1x1 matrix
    print("Test 11: 2D edge case - 1x1 matrix")
    try:
        x = np.array([[5]])
        result = fill_diagonal(x, 0)
        assert np.array_equal(result, [[0]]), "1x1 case failed"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 12: 2D edge case - 2x2 matrix
    print("Test 12: 2D edge case - 2x2 matrix")
    try:
        x = np.array([[1, 2], [3, 4]])
        result = fill_diagonal(x, 0)
        expected = np.array([[0, 2], [3, 0]])
        assert np.array_equal(result, expected), "2x2 case failed"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 13: 2D boolean mask
    print("Test 13: 2D boolean mask")
    try:
        mask = np.ones((5, 5), dtype=bool)
        result = fill_diagonal(mask, False)

        # Check diagonal is False
        assert np.all(result.diagonal() == False), "Diagonal not False"

        # Check off-diagonal elements are True
        for i in range(5):
            for j in range(5):
                if i != j:
                    assert result[i, j] == True, f"Off-diagonal at [{i},{j}] not True"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 14: 2D large matrix
    print("Test 14: 2D large matrix")
    try:
        x = np.ones((100, 100))
        result = fill_diagonal(x, 0)
        assert np.all(result.diagonal() == 0), "Large matrix diagonal not filled"
        assert result[0, 1] == 1, "Off-diagonal changed in large matrix"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 15: 2D complex numbers
    print("Test 15: 2D complex numbers")
    try:
        x = np.ones((3, 3), dtype=complex)
        result = fill_diagonal(x, 1 + 2j)
        assert np.all(result.diagonal() == 1 + 2j), "Complex fill failed"
        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # ==================== 3D ARRAY TESTS ====================
    print("\n" + "=" * 60)
    print("3D ARRAY TESTS")
    print("=" * 60 + "\n")

    # Test 16: 3D array - basic case
    print("Test 16: 3D array - fill diagonal on last two dimensions")
    try:
        x = np.ones((2, 3, 3))
        result = fill_diagonal(x, 0, axis1=-2, axis2=-1)

        # Check shape preserved
        assert result.shape == (2, 3, 3), f"Wrong shape: {result.shape}"

        # Check diagonals filled for each batch
        for i in range(2):
            diag = np.diagonal(result[i])
            assert np.all(diag == 0), f"Batch {i} diagonal not filled"
            # Check off-diagonal elements unchanged
            assert result[i, 0, 1] == 1, f"Batch {i} off-diagonal changed"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 17: 3D array - fill diagonal on first two dimensions
    print("Test 17: 3D array - fill diagonal on first two dimensions")
    try:
        x = np.ones((4, 4, 5))
        result = fill_diagonal(x, 0, axis1=0, axis2=1)

        assert result.shape == (4, 4, 5), f"Wrong shape: {result.shape}"

        # Check diagonal along axis 0 and 1
        for k in range(5):
            diag = np.diagonal(result[:, :, k])
            assert np.all(diag == 0), f"Slice {k} diagonal not filled"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 18: 3D array with positive offset
    print("Test 18: 3D array with positive offset")
    try:
        x = np.ones((2, 4, 4))
        result = fill_diagonal(x, 0, offset=1, axis1=-2, axis2=-1)

        # Check super-diagonal for each batch
        for i in range(2):
            diag = np.diagonal(result[i], offset=1)
            assert np.all(diag == 0), f"Batch {i} offset diagonal not filled"
            # Main diagonal should be unchanged
            main_diag = np.diagonal(result[i])
            assert np.all(main_diag == 1), f"Batch {i} main diagonal changed"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 19: 3D array with negative offset
    print("Test 19: 3D array with negative offset")
    try:
        x = np.ones((3, 5, 5))
        result = fill_diagonal(x, -1, offset=-1, axis1=-2, axis2=-1)

        for i in range(3):
            diag = np.diagonal(result[i], offset=-1)
            assert np.all(diag == -1), f"Batch {i} negative offset diagonal not filled"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 20: 3D non-square matrices
    print("Test 20: 3D array with non-square matrices")
    try:
        x = np.ones((3, 4, 6))
        result = fill_diagonal(x, 0, axis1=-2, axis2=-1)

        for i in range(3):
            diag = np.diagonal(result[i])
            assert np.all(diag == 0), f"Batch {i} non-square diagonal not filled"
            assert len(diag) == 4, f"Wrong diagonal length for non-square"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 21: 3D array - different value types
    print("Test 21: 3D array with different value types")
    try:
        # Float values
        x = np.ones((2, 3, 3))
        result = fill_diagonal(x, 3.14)
        assert np.allclose(np.diagonal(result[0]), 3.14), "Float fill failed"

        # Boolean values
        x_bool = np.ones((2, 3, 3), dtype=bool)
        result = fill_diagonal(x_bool, False)
        for i in range(2):
            assert np.all(np.diagonal(result[i]) == False), f"Boolean fill failed for batch {i}"

        # Complex values
        x_complex = np.ones((2, 3, 3), dtype=complex)
        result = fill_diagonal(x_complex, 1 + 2j)
        for i in range(2):
            assert np.all(np.diagonal(result[i]) == 1 + 2j), f"Complex fill failed for batch {i}"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 22: 3D batched boolean masks (realistic use case)
    print("Test 22: 3D batched boolean masks")
    try:
        batch_size = 4
        seq_len = 8
        mask = np.ones((batch_size, seq_len, seq_len), dtype=bool)
        result = fill_diagonal(mask, False, axis1=-2, axis2=-1)

        for b in range(batch_size):
            # Check diagonal is False
            assert np.all(np.diagonal(result[b]) == False), f"Batch {b} diagonal not False"
            # Check off-diagonal is True
            assert result[b, 0, 1] == True, f"Batch {b} off-diagonal wrong"
            assert result[b, 1, 0] == True, f"Batch {b} off-diagonal wrong"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 23: 3D with all different axis combinations
    print("Test 23: 3D array with various axis combinations")
    try:
        x = np.arange(60).reshape(3, 4, 5)

        # axis1=0, axis2=1
        result1 = fill_diagonal(x.copy(), -1, axis1=0, axis2=1)
        diag1 = np.diagonal(result1, axis1=0, axis2=1)
        assert np.all(diag1 == -1), "axis1=0, axis2=1 failed"

        # axis1=0, axis2=2
        result2 = fill_diagonal(x.copy(), -2, axis1=0, axis2=2)
        diag2 = np.diagonal(result2, axis1=0, axis2=2)
        assert np.all(diag2 == -2), "axis1=0, axis2=2 failed"

        # axis1=1, axis2=2
        result3 = fill_diagonal(x.copy(), -3, axis1=1, axis2=2)
        diag3 = np.diagonal(result3, axis1=1, axis2=2)
        assert np.all(diag3 == -3), "axis1=1, axis2=2 failed"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 24: 3D immutability
    print("Test 24: 3D array immutability")
    try:
        x = np.ones((2, 3, 3))
        original = x.copy()
        result = fill_diagonal(x, 0)

        assert np.array_equal(x, original), "Original 3D array was modified"
        assert result is not x, "Result is same object as input"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 25: 3D edge case - size-1 dimensions
    print("Test 25: 3D array with size-1 dimensions")
    try:
        x = np.ones((1, 3, 3))
        result = fill_diagonal(x, 0)
        assert np.all(np.diagonal(result[0]) == 0), "Size-1 batch dimension failed"

        x = np.ones((3, 1, 1))
        result = fill_diagonal(x, 0)
        assert result.shape == (3, 1, 1), "Size-1 matrix dimensions failed"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 26: 3D with extreme offsets
    print("Test 26: 3D array with extreme offsets")
    try:
        x = np.ones((2, 5, 5))

        # Large positive offset
        result = fill_diagonal(x, 0, offset=10)
        assert result.shape == (2, 5, 5), "Extreme offset changed shape"

        # Large negative offset
        result = fill_diagonal(x, 0, offset=-10)
        assert result.shape == (2, 5, 5), "Extreme negative offset changed shape"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # ==================== 4D ARRAY TESTS ====================
    print("\n" + "=" * 60)
    print("4D ARRAY TESTS")
    print("=" * 60 + "\n")

    # Test 27: 4D array - basic case
    print("Test 27: 4D array - fill diagonal on last two dimensions")
    try:
        x = np.ones((2, 3, 4, 4))
        result = fill_diagonal(x, 0, axis1=-2, axis2=-1)

        assert result.shape == (2, 3, 4, 4), f"Wrong shape: {result.shape}"

        # Check diagonals for all batches
        for i in range(2):
            for j in range(3):
                diag = np.diagonal(result[i, j])
                assert np.all(diag == 0), f"Batch [{i},{j}] diagonal not filled"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 28: 4D array - fill diagonal on middle dimensions
    print("Test 28: 4D array - fill diagonal on dimensions 1 and 2")
    try:
        x = np.ones((2, 4, 4, 3))
        result = fill_diagonal(x, 0, axis1=1, axis2=2)

        assert result.shape == (2, 4, 4, 3), f"Wrong shape: {result.shape}"

        # Check diagonal along axis 1 and 2
        for i in range(2):
            for k in range(3):
                diag = np.diagonal(result[i, :, :, k])
                assert np.all(diag == 0), f"Slice [{i},:,:,{k}] diagonal not filled"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 29: 4D array with offset
    print("Test 29: 4D array with offset")
    try:
        x = np.ones((2, 2, 5, 5))
        result = fill_diagonal(x, 0, offset=2, axis1=-2, axis2=-1)

        for i in range(2):
            for j in range(2):
                diag = np.diagonal(result[i, j], offset=2)
                assert np.all(diag == 0), f"Batch [{i},{j}] offset diagonal not filled"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 30: 4D array immutability
    print("Test 30: 4D array immutability")
    try:
        x = np.ones((2, 2, 3, 3))
        original = x.copy()
        result = fill_diagonal(x, 0)

        assert np.array_equal(x, original), "Original 4D array was modified"
        assert result is not x, "Result is same object as input"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 31: Large 4D array (performance check)
    print("Test 31: Large 4D array (performance check)")
    try:
        x = np.ones((10, 10, 50, 50))
        result = fill_diagonal(x, 0)

        # Spot check a few diagonals
        assert np.all(np.diagonal(result[0, 0]) == 0), "Large array diagonal fill failed"
        assert np.all(np.diagonal(result[5, 5]) == 0), "Large array diagonal fill failed"
        assert np.all(np.diagonal(result[9, 9]) == 0), "Large array diagonal fill failed"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # ==================== 5D+ ARRAY TESTS ====================
    print("\n" + "=" * 60)
    print("5D+ ARRAY TESTS")
    print("=" * 60 + "\n")

    # Test 32: 5D array
    print("Test 32: 5D array")
    try:
        x = np.ones((2, 2, 2, 3, 3))
        result = fill_diagonal(x, 0, axis1=-2, axis2=-1)

        assert result.shape == (2, 2, 2, 3, 3), f"Wrong shape: {result.shape}"

        # Check a few diagonals
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    diag = np.diagonal(result[i, j, k])
                    assert np.all(diag == 0), f"5D diagonal at [{i},{j},{k}] not filled"

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Test 33: 6D array (extreme dimensionality)
    print("Test 33: 6D array")
    try:
        x = np.ones((2, 2, 2, 2, 3, 3))
        result = fill_diagonal(x, 0, axis1=-2, axis2=-1)

        assert result.shape == (2, 2, 2, 2, 3, 3), "6D shape wrong"

        # Check one diagonal
        assert np.all(np.diagonal(result[0, 0, 0, 0]) == 0), "6D diagonal not filled"
        assert np.all(np.diagonal(result[1, 1, 1, 1]) == 0), "6D diagonal not filled"
        assert np.all(np.diagonal(result[0, 1, 1, 1]) == 0), "6D diagonal not filled"
        assert np.all(np.diagonal(result[1, 0, 0, 0]) == 0), "6D diagonal not filled"
        assert np.all(np.diagonal(result[1, 0, 1, 0]) == 0), "6D diagonal not filled"
        assert np.all(result[:, :, :, :, 1, 0] == 1)
        assert np.all(result[:, :, :, :, 0, 0] == 0)

        print("✓ PASSED\n")
        tests_passed += 1
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        tests_failed += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"ALL TESTS COMPLETED: {tests_passed + tests_failed}")
    print(f"PASSED: {tests_passed}")
    print(f"FAILED: {tests_failed}")
    print("=" * 60)
    if tests_failed > 0:
        raise Exception("Some tests failed")
    else:
        print("All tests passed successfully.")
    return tests_passed, tests_failed


if __name__ == "__main__":
    test_fill_diagonal_all_dimensions()
