## Session 3: Mastering Multi-threading in Python

**Goal:**
Learn how to run code concurrently using threads to improve performance for I/O-bound tasks.

**Definition:**
Multi-threading splits a program into multiple threads running in parallel. In Python, this is ideal for I/O-bound operations because threads share the same memory space. Use cases include network operations, file I/O, and handling multiple user requests. Despite the Global Interpreter Lock (GIL), multi-threading remains effective for many practical scenarios.

**Documentation Reference:**
- https://docs.python.org/3/library/threading.html
- https://realpython.com/intro-to-python-threading/
- https://www.tutorialspoint.com/python/python_multithreading.htm

### Tutorial:

- Introduction: Explain the threading module.

```py
import threading
import time

def print_numbers():
    for i in range(5):
        print(i)
        time.sleep(1)

thread = threading.Thread(target=print_numbers)
thread.start()
thread.join()
```
- Explanation: This runs the print_numbers function in a separate thread.
- Discussion: Mention when to use threads (e.g., I/O-bound tasks).

### Exercise:

- Problem: Create two threads that print letters and numbers concurrently.
- Steps to Solve:
    - Define two functions—one for letters and one for numbers.
    - Create and start a thread for each function.

### Challenge:

- Problem: Create a multi-threaded program that downloads multiple files concurrently from given URLs.
- Hint: Use the threading module along with urllib.request.urlretrieve.www