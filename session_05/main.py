# Session 5: Asynchronous Programming with asyncio and FastAPI

# Because of dependencies, to run this session, run the following command from the root of the project:
# cd session_05 && uv sync && uv run python main.py
import asyncio

try:
    from fastapi import FastAPI
    import aiohttp
    _FASTAPI_AVAILABLE = True
except ImportError:
    _FASTAPI_AVAILABLE = False


# --- Tutorial: basic async function ---
async def simulated_io_task() -> str:
    await asyncio.sleep(1)   # non-blocking wait (simulates DB / HTTP call)
    return "Data fetched!"


# --- Problem: asyncio.gather — two concurrent data sources ---
async def fetch_source_a() -> dict:
    await asyncio.sleep(0.5)
    return {"source": "A", "data": "payload from source A"}


async def fetch_source_b() -> dict:
    await asyncio.sleep(0.7)
    return {"source": "B", "data": "payload from source B"}


async def fetch_both() -> list[dict]:
    # gather runs both coroutines concurrently; total wait ≈ max(0.5, 0.7)
    result_a, result_b = await asyncio.gather(fetch_source_a(), fetch_source_b())
    return [result_a, result_b]


# --- Challenge: async web scraper with aiohttp ---
async def _fetch_html(session, url: str) -> dict:
    async with session.get(url) as response:
        text = await response.text()
        return {"url": url, "status": response.status, "length": len(text)}


async def scrape_urls(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [_fetch_html(session, url) for url in urls]
        return await asyncio.gather(*tasks)   # all requests in flight at once


# --- FastAPI app (only wired when the package is installed) ---
if _FASTAPI_AVAILABLE:
    app = FastAPI()

    @app.get("/async-data")
    async def get_data():
        result = await simulated_io_task()
        return {"message": result}

    @app.get("/combined-data")
    async def get_combined():
        return {"results": await fetch_both()}

    @app.get("/scrape")
    async def scrape():
        urls = ["https://example.com", "https://httpbin.org/get"]
        return {"results": await scrape_urls(urls)}


def main():
    # Tutorial
    result = asyncio.run(simulated_io_task())
    print("Tutorial:", result)

    # Problem
    combined = asyncio.run(fetch_both())
    print("Problem:", combined)

    # Challenge (requires network + aiohttp)
    if _FASTAPI_AVAILABLE:
        urls = ["https://example.com", "https://httpbin.org/get"]
        scraped = asyncio.run(scrape_urls(urls))
        print("Challenge (scraper):", scraped)
    else:
        print("Challenge: install aiohttp to run the scraper")


if __name__ == "__main__":
    main()
