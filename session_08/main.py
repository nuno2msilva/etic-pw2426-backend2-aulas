# Run tests with: uv sync && uv run pytest test_main.py -v
from __future__ import annotations   # enables X | Y union hints on Python < 3.10


# --- Tutorial: simple function under test ---
def add(a: int | float, b: int | float) -> int | float:
    return a + b


# --- Problem: multiply function (tested in test_main.py) ---
def multiply(a: int | float, b: int | float) -> int | float:
    return a * b


# --- Challenge: recursive factorial (parametrized tests in test_main.py) ---
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)

# Example values to run main script and see outputs; tests in test_main.py cover more cases
def main():
    print("add(2, 3)      =", add(2, 3))
    print("multiply(4, 5) =", multiply(4, 5))
    print("factorial(6)   =", factorial(6))
    print("Run 'uv sync && uv run pytest test_main.py -v' to execute the test suite.")


if __name__ == "__main__":
    main()
