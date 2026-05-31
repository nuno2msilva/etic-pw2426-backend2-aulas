import pytest
from main import add, multiply, factorial


# --- Tutorial: test the add function (from the README example) ---
def test_add():
    assert add(2, 3) == 5


# --- Problem: tests for multiply ---
def test_multiply_positive():
    assert multiply(4, 5) == 20


def test_multiply_by_zero():
    assert multiply(9, 0) == 0


def test_multiply_floats():
    assert multiply(2.5, 4) == pytest.approx(10.0)


# --- Challenge: parametrized factorial tests ---
@pytest.mark.parametrize("n, expected", [
    (0, 1),
    (1, 1),
    (2, 2),
    (5, 120),
    (10, 3628800),
])
def test_factorial(n, expected):
    assert factorial(n) == expected


def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        factorial(-1)
