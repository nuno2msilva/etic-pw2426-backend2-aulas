import asyncio
import time


# --- Tutorial: create_task + gather ---
async def task_function(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} completed"


async def tutorial_tasks() -> list[str]:
    task1 = asyncio.create_task(task_function("Task 1", 1))
    task2 = asyncio.create_task(task_function("Task 2", 2))
    return await asyncio.gather(task1, task2)   # runs concurrently


# --- Problem: multiple tasks with per-task timeout + graceful cancellation ---
async def run_with_timeout(name: str, delay: float, timeout: float) -> str:
    try:
        # shield keeps the inner task alive even if wait_for raises
        return await asyncio.wait_for(task_function(name, delay), timeout=timeout)
    except asyncio.TimeoutError:
        return f"{name} timed out (>{timeout}s)"


async def run_tasks_with_timeout(configs: list[tuple[str, float]], timeout: float) -> list[str]:
    """Launch all tasks concurrently, each with the same timeout budget."""
    coroutines = [run_with_timeout(name, delay, timeout) for name, delay in configs]
    return await asyncio.gather(*coroutines)


# --- Challenge: rate limiter via Semaphore ---
# Semaphore allows at most `max_concurrent` tasks to run at the same time
async def _rate_limited_task(semaphore: asyncio.Semaphore, name: str, delay: float) -> str:
    async with semaphore:               # blocks here when limit is reached
        await asyncio.sleep(delay)
        return f"{name} done"


async def run_rate_limited(max_concurrent: int, tasks: list[tuple[str, float]]) -> list[str]:
    semaphore = asyncio.Semaphore(max_concurrent)
    coroutines = [_rate_limited_task(semaphore, name, delay) for name, delay in tasks]
    return await asyncio.gather(*coroutines)


def main():
    # Tutorial
    print("Tutorial — concurrent tasks:")
    results = asyncio.run(tutorial_tasks())
    print(" ", results)

    # Problem
    print("\nProblem — tasks with 1.5 s timeout:")
    configs = [("Fast", 0.5), ("Medium", 1.2), ("Slow", 3.0)]
    results = asyncio.run(run_tasks_with_timeout(configs, timeout=1.5))
    for r in results:
        print(" ", r)

    # Challenge
    print("\nChallenge — rate limiter (max 2 concurrent):")
    tasks = [(f"Job-{i}", 0.5) for i in range(6)]
    start = time.perf_counter()
    results = asyncio.run(run_rate_limited(max_concurrent=2, tasks=tasks))
    elapsed = time.perf_counter() - start
    for r in results:
        print(" ", r)
    # with 6 tasks and limit=2 → 3 batches of 2 → ~1.5 s total
    print(f"  elapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
