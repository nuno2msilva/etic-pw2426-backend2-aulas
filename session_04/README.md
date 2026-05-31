## Session 4: Multi-processing in Python for Scalability
**Goal:**
Understand how to run tasks concurrently in separate processes to boost performance in CPU-bound tasks.

**Definition:**
Multi-processing uses separate processes with their own memory space, bypassing the Global Interpreter Lock (GIL). This technique is ideal for CPU-intensive tasks such as heavy computations or large data processing, where parallel execution on multiple cores can lead to significant speed improvements. It is commonly used in scenarios that require isolated execution environments.

**Documentation Reference:**

- https://docs.python.org/3/library/multiprocessing.html
- https://realpython.com/python-multiprocessing/
- https://www.geeksforgeeks.org/multiprocessing-python-set-1/

**Tutorial:**
- Introduction: Explain the difference between threading and multi-processing.
- Step-by-Step Example:
    - Import the multiprocessing module.
    -  Define a simple function (e.g., compute a square).
    - Create and start multiple processes.
```py
import multiprocessing
import time

def compute_square(n):
    time.sleep(1)  # Simulate a heavy computation
    print(f"Square of {n} is {n*n}")

if __name__ == "__main__":
    numbers = [2, 3, 4, 5]
    processes = []
    for number in numbers:
        p = multiprocessing.Process(target=compute_square, args=(number,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

```
- Explanation: Each process runs independently, and joining ensures all complete before the script ends.

### Exercise:

- Problem: Create a program that concurrently computes the factorial of several numbers using multi-processing.
- Steps to Solve:
    - Define a recursive factorial function.
    - Spawn a process for each number in a list.

### Challenge:

- Problem: Create a multi-process program that divides a large list of numbers into sublists and computes the sum of squares for each sublist concurrently.
- Hint:
  Use the Pool class from the multiprocessing module.