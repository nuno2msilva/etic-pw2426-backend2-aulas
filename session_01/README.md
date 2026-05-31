## Session 1: Fundamentals of Big O Notation in Python Performance

**Goal:**
Understand how algorithm complexity is measured with Big O notation and why it matters for performance in Python.

**Definition:**
Big O notation expresses the upper bound of an algorithm’s runtime relative to its input size. It helps you compare algorithms and identify potential bottlenecks. Use cases include analysing search, sort, or any iterative processes. In Python, knowing Big O is essential for writing efficient code when dealing with large datasets.

**Documentation Reference:**
- https://docs.python.org/3/tutorial/datastructures.html
- https://en.wikipedia.org/wiki/Big_O_notation
- https://www.geeksforgeeks.org/analysis-of-algorithms-set-1-asymptotic-analysis/
- https://www.bigocheatsheet.com/

### Tutorial:

- Write a simple linear search function:
```py
def linear_search(lst, target):
    for item in lst:
        if item == target:
            return True
    return False
```

- Explanation: This function’s runtime grows linearly with the size of the list, hence O(n).

- Comparison: Briefly discuss how a binary search (O(log n)) differs in performance.

### Exercise:

- Problem: Write a recursive function to calculate factorial and determine its time complexity.
- Steps to Solve:
    - Define the recursive factorial function.
    - Analyse how many times the function is called relative to the input.

### Challenge:

- Problem: Optimise a bubble sort algorithm so that it stops early if the list is already sorted.
> Hint: Use a flag to detect whether a swap occurred.
