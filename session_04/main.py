# Session 4: Multi-processing in Python for Scalability

import multiprocessing
import time


# --- Tutorial: compute square in a child process ---
def compute_square(n: int) -> None:
    time.sleep(0.5)   # simulate heavy CPU work
    print(f"  Square of {n} = {n * n}")


# --- Problem: factorial using separate processes ---
def _factorial(n: int) -> int:
    """Recursive factorial (same as session 1, reused here for multiprocessing)."""
    if n == 0:
        return 1
    return n * _factorial(n - 1)


def compute_factorial(n: int) -> None:
    print(f"  {n}! = {_factorial(n)}")


# --- Challenge: Pool — sum of squares over sublists ---
def sum_of_squares(sublist: list[int]) -> int:
    """Worker function: receives one chunk, returns its sum of squares."""
    return sum(x ** 2 for x in sublist)


def _chunks(lst: list, size: int):
    """Split lst into chunks of the given size."""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


if __name__ == "__main__":
    # Tutorial: individual processes for squares
    print("Tutorial — compute squares in separate processes:")
    numbers = [2, 3, 4, 5]
    processes = [multiprocessing.Process(target=compute_square, args=(n,)) for n in numbers]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    # Problem: factorial per process
    print("\nProblem — factorial per process:")
    targets = [5, 6, 7, 8]
    processes = [multiprocessing.Process(target=compute_factorial, args=(n,)) for n in targets]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    # Challenge: Pool distributes sublists across worker processes
    print("\nChallenge — Pool sum of squares:")
    large_list = list(range(1, 21))           # [1 … 20]
    sublists = list(_chunks(large_list, 5))   # four chunks of five

    with multiprocessing.Pool() as pool:
        results = pool.map(sum_of_squares, sublists)

    for sublist, total in zip(sublists, results):
        print(f"  sum of squares {sublist} = {total}")
    print(f"  grand total = {sum(results)}")
