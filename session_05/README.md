## Session 5: Asynchronous Programming in Python with asyncio and FastAPI

**Goal:**
Learn to write non-blocking code using asyncio and integrate it into a FastAPI endpoint.

**Definition:**
Asynchronous programming allows concurrent execution of tasks without waiting for each to complete sequentially. In Python, the asyncio library provides tools to write such code, which is especially useful for I/O-bound operations like web requests or database calls. This enables scalable web services by handling multiple requests simultaneously.

**Documentation Reference:**

- https://docs.python.org/3/library/asyncio.html
- https://fastapi.tiangolo.com/async/
- https://realpython.com/async-io-python/

**Setup:**
```bash
uv sync
```

**Tutorial:**
- Step-by-Step Example:

    - Create an asynchronous function using async def and await.
    - Define a FastAPI endpoint that calls this async function.
```py
    from fastapi import FastAPI
    import asyncio

    app = FastAPI()

    async def simulated_io_task():
        await asyncio.sleep(1)
        return "Data fetched!"

    @app.get("/async-data")
    async def get_data():
        result = await simulated_io_task()
        return {"message": result}
```
- Run the server:
```bash
uv run uvicorn main:app --reload
```
- Explanation: The endpoint /async-data executes the async task without blocking other requests.

### Exercise:

- Problem: Create a FastAPI endpoint that concurrently fetches data from two simulated sources using asyncio.gather.

    - Steps to Solve:
        - Define two async functions that simulate data fetching.
        - Use asyncio.gather to run them concurrently.


### Challenge:

- Problem:Develop an asynchronous web scraper that fetches HTML content from multiple URLs concurrently using aiohttp.
    - Hint: Use the aiohttp library with asyncio.gather.
