## Session 6: Advanced Async Patterns and Concurrency Techniques

**Goal:**
Explore advanced asynchronous programming concepts to manage tasks, handle timeouts, and coordinate concurrent operations efficiently.

**Definition:**
Beyond basic async functions, advanced patterns include task scheduling, handling cancellations, and synchronising shared resources with locks or semaphores. These techniques help in building high-load systems and real-time data processing pipelines. They are crucial when developing scalable web applications and services that demand robust concurrency management.

**Documentation Reference:**

- https://docs.python.org/3/library/asyncio-task.html
- https://realpython.com/python-async-features/
- https://medium.com/@kennethreitz/async-await-in-python-3-5-7b580ca64b73

**Tutorial:**
- Creating Tasks:
    - Use asyncio.create_task to run coroutines concurrently.
```py
import asyncio

async def task_function(name, delay):
    await asyncio.sleep(delay)
    return f"{name} completed"

async def main():
    task1 = asyncio.create_task(task_function("Task 1", 1))
    task2 = asyncio.create_task(task_function("Task 2", 2))
    results = await asyncio.gather(task1, task2)
    print(results)

asyncio.run(main())
```

- Handling Timeouts:
    - Use asyncio.wait_for to set timeouts.
```py
    async def timeout_task():
        await asyncio.sleep(2)
        return "Completed"

    async def main_timeout():
        try:
            result = await asyncio.wait_for(timeout_task(), timeout=1)
        except asyncio.TimeoutError:
            result = "Task timed out"
        print(result)

    asyncio.run(main_timeout())
```
- Explanation: This demonstrates cancelling a task if it exceeds the allotted time.

### Exercise:

- Problem: Write an async function that launches several tasks with a timeout and handles cancellations gracefully.
    -Steps to Solve:
        - Create multiple tasks using create_task.
        - Wrap them with asyncio.wait_for and handle possible timeouts.

### Challenge:

- Problem: Implement an asynchronous rate limiter that allows only a fixed number of tasks per second.
    - Hint: Use an asyncio semaphore to control the concurrency.