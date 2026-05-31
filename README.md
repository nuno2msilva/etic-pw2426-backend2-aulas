# Backend II — Aulas Remaster

A session-by-session Python backend course covering performance, concurrency, web frameworks, testing, and AI agents. Each session is self-contained with a standalone `main.py` that runs without extra packages, plus optional framework-specific code unlocked after `uv sync`.

## Cleanup (restore freshly-cloned state)

```bash
make clean            # all sessions
make clean-session_00 # one session
```

---

## Session 01 — Big O Notation

Big O notation is the standard way to express how an algorithm's runtime or memory usage scales with input size. Understanding it is essential for making informed decisions about which data structures and algorithms to reach for when working with large datasets.

This session covers three progressively complex examples:

- **Linear search O(n)** — iterates through a list item by item until a match is found; runtime grows proportionally with the list size.
- **Recursive factorial O(n)** — the function calls itself `n` times before reaching the base case (`0! = 1`), making the call stack depth directly proportional to the input.
- **Optimised bubble sort O(n²) → O(n)** — the classic O(n²) sort is improved with an early-exit flag: if a full pass completes without any swaps, the list is already sorted and the algorithm stops immediately, achieving O(n) on already-sorted input.

```bash
cd session_01 && uv run python main.py
```

---

## Session 02 — Design Patterns

Design patterns are battle-tested solutions to recurring software design problems. They provide a shared vocabulary among developers and help build codebases that are easier to reason about, extend, and maintain.

This session implements three fundamental patterns from the Gang of Four catalogue:

- **Singleton** — ensures only one instance of a class ever exists, sharing the same object across the entire application. Useful for database connections, configuration managers, and loggers.
- **Factory** — decouples object creation from the code that uses the objects. A factory function receives a string or enum and returns the correct concrete class (e.g. `"circle"` → `Circle`, `"square"` → `Square`), so callers never need to import or instantiate concrete types directly.
- **Observer** — implements a publish/subscribe mechanism where a `Subject` maintains a list of `Observer` objects and notifies all of them whenever its state changes. The foundation of event-driven architectures and UI frameworks.

```bash
cd session_02 && uv run python main.py
```

---

## Session 03 — Multi-threading

Multi-threading lets a program run multiple units of work concurrently within the same process, sharing the same memory space. In Python, threads are best suited for **I/O-bound** tasks — operations that spend most of their time waiting on the network, disk, or external services — because the Global Interpreter Lock (GIL) prevents true parallel CPU execution.

Topics covered:

- Creating and starting threads with `threading.Thread`, passing functions and arguments.
- Synchronising threads with `.join()` to wait for all work to complete before continuing.
- Running two threads concurrently that each print different sequences (letters and numbers), demonstrating interleaved execution.
- A practical multi-threaded file downloader that fetches multiple URLs at the same time using `urllib.request.urlretrieve`, reducing total wait time compared to sequential downloads.

```bash
cd session_03 && uv run python main.py
```

---

## Session 04 — Multi-processing

Where threads are limited by the GIL for CPU-intensive work, `multiprocessing` spawns separate OS processes — each with its own Python interpreter and memory space — allowing true parallel execution across multiple CPU cores.

Topics covered:

- Spawning individual `multiprocessing.Process` objects to run a compute-heavy function (e.g. computing squares with a simulated delay) across multiple cores simultaneously.
- Using `multiprocessing.Pool` for a higher-level interface: `pool.map()` automatically distributes work across a pool of worker processes and collects the results.
- A parallel sum-of-squares challenge that partitions a large list into sub-lists, sends each to a different worker, and aggregates the partial results — a basic map-reduce pattern.
- The critical `if __name__ == "__main__":` guard required on Windows/macOS to prevent recursive spawning.

```bash
cd session_04 && uv run python main.py
```

---

## Session 05 — Async / FastAPI

Asynchronous programming with `asyncio` allows a single thread to manage thousands of concurrent I/O operations by suspending work on tasks that are waiting (e.g. a network response) and resuming other tasks in the meantime — without the overhead of creating threads or processes.

Topics covered:

- `async def` and `await` — defining coroutines and suspending them at I/O boundaries.
- `asyncio.gather()` — running multiple coroutines concurrently and waiting for all of them, reducing total latency to roughly the duration of the slowest task rather than the sum of all.
- FastAPI integration — defining `async` endpoint handlers that call awaitable functions, keeping the server non-blocking and able to serve many requests simultaneously.
- An async web scraper using `aiohttp` that fetches HTML content from multiple URLs concurrently, demonstrating a real-world I/O-bound workload.

```bash
cd session_05 && uv sync && uv run uvicorn main:app --reload
```

---

## Session 06 — Advanced Async Patterns

Building on the asyncio fundamentals, this session introduces the higher-level primitives needed to write production-grade async code that handles failures, enforces deadlines, and controls concurrency.

Topics covered:

- **`asyncio.create_task()`** — schedules a coroutine to run concurrently without blocking the caller, similar to spawning a background thread but lighter-weight.
- **`asyncio.wait_for()`** — wraps a coroutine with a deadline; raises `asyncio.TimeoutError` if the task doesn't complete in time, allowing graceful degradation.
- **Cancellation handling** — catching `asyncio.CancelledError` inside a task to perform cleanup before the task is torn down.
- **`asyncio.Semaphore` as a rate limiter** — caps how many coroutines are allowed to execute simultaneously, preventing a flood of concurrent requests from overwhelming a downstream service or API rate limit.

```bash
cd session_06 && uv run python main.py
```

---

## Session 07 — Logging

Logging is the primary observability tool in production systems. Done well, it lets you diagnose issues without a debugger and understand application behaviour over time — done poorly, it produces noise that obscures real problems.

Topics covered:

- **`logging.basicConfig()`** — configuring the root logger with a severity level, timestamp format, and output stream. Using `stream=sys.stdout` avoids interleaved output caused by stderr/stdout buffering differences.
- **All five severity levels** in practice: `DEBUG` (detailed diagnostics), `INFO` (general flow), `WARNING` (unexpected but recoverable), `ERROR` (a failure occurred), `CRITICAL` (system may not continue).
- **`TimedRotatingFileHandler`** — rotates log files at midnight daily and retains the last 7 files, preventing unbounded disk growth in long-running applications.
- **loguru** (via `uv sync`) — a third-party library that simplifies logging configuration to a single `logger.add()` call with automatic rotation, compression, and coloured output.

```bash
cd session_07 && uv sync && uv run python main.py
```

---

## Session 08 — pytest Basics

Automated tests are the safety net that lets you refactor and extend code with confidence. `pytest` is the de-facto Python testing framework: it discovers tests automatically, produces readable failure output, and provides powerful features that make tests concise and maintainable.

Topics covered:

- Writing basic test functions with `assert` statements — no boilerplate classes required.
- **Fixtures** — using `@pytest.fixture` to set up shared state (e.g. a database connection or a pre-populated object) that is injected into tests by name, keeping tests independent and DRY.
- **`@pytest.mark.parametrize`** — running the same test function against multiple input/output pairs in a single decorator, used here to verify a recursive factorial against several known values without duplicating test code.
- Running the suite with `uv run pytest` and interpreting the output: passed/failed counts, assertion introspection, and traceback context.

```bash
cd session_08 && uv sync && uv run pytest -v
```

---

## Session 09 — Django + pytest-django

This session introduces real-world Django project structure and testing strategy using a fully wired Django 6 project with an in-memory SQLite test database.

**Project layout:**
```
session_09/
├── myproject/        # Django project (settings, urls, wsgi)
├── myapp/            # application (models, views, admin, apps)
├── tests/            # pytest-django test suite
│   └── test_models.py
├── conftest.py       # Django settings for pytest (uses :memory: SQLite)
└── manage.py
```

Topics covered:

- **Django models** — `Item` (name + value) and `BlogPost` (title, content, published_date) using `CharField`, `IntegerField`, `TextField`, and `DateField`; custom methods `summary()` and `is_published()`.
- **`@pytest.mark.django_db`** — grants a test access to the test database, which is created fresh and rolled back after every test for full isolation.
- **Fixtures** — a `sample_posts` fixture that pre-populates the database, demonstrating how to share setup across multiple tests.
- **`@pytest.mark.parametrize`** — verifying `summary()` behaviour for short and long content in a single parametrized test.
- **`manage.py`** — applying migrations and running the development server against a real SQLite file.

```bash
cd session_09 && uv sync && uv run pytest tests/ -v
```

---

## Session 10 — Security

Web applications are constantly targeted by automated attacks. This session covers the most common vulnerability classes and shows how to defend against them with a complete Django application.

Topics covered:

- **CSRF protection** — Django's `CsrfViewMiddleware` automatically validates tokens on all POST/PUT/DELETE requests. Every form includes `{% csrf_token %}` which prevents cross-site request forgery attacks.
- **Secure session management** — Django sessions are stored server-side with `HttpOnly` cookies (prevents XSS JavaScript access), `SameSite=Strict` (mitigates CSRF), and automatic expiration on browser close.
- **Input validation & sanitisation** — Django forms validate all user inputs with custom validators checking format, length, and patterns. XSS prevention through HTML-escaping dangerous content (`<script>alert(1)</script>` becomes `&lt;script&gt;alert(1)&lt;/script&gt;`).
- **Authentication & access control** — user login/registration with secure password hashing, `@login_required` decorators, and user-specific data isolation.
- **Audit trails** — each user action is linked to the authenticated user account with automatic timestamps for accountability.

```bash
cd session_10 && uv sync && python manage.py migrate && python manage.py runserver
```

---

## Session 11 — GraphQL

GraphQL gives API clients precise control over what data they fetch, eliminating over-fetching (receiving fields you don't need) and under-fetching (needing multiple round-trips). This session implements a GraphQL API with Strawberry, a modern Python library that uses type annotations as the schema definition.

Topics covered:

- **Schema types** — `@strawberry.type` classes (`User`, `Post`, `UserWithPosts`) map directly to Python dataclasses, keeping the schema and the code in sync.
- **Queries** — resolvers for `user(id)`, `users()`, and `userWithPosts(id, token)`, backed by an in-memory dictionary that stands in for a real database.
- **Mutations** — an `updateUserName(id, newName)` mutation that modifies state and returns the updated object.
- **Authenticated resolver** — the `userWithPosts` query validates a `token` argument before returning nested post data, showing how to guard resolvers without HTTP middleware.
- **FastAPI integration** — mounting the Strawberry `GraphQL` ASGI app at `/graphql`, which also serves the interactive GraphiQL explorer in the browser.

```bash
cd session_11 && uv sync && uv run uvicorn main:app --reload
```

---

## Session 12 — gRPC

gRPC is a high-performance RPC framework from Google that uses Protocol Buffers (a compact binary format) for serialisation instead of JSON. It is widely used for microservice-to-microservice communication where throughput and latency matter.

Topics covered:

- **`.proto` file** — defining two services (`CubeService` with a unary RPC, `StreamService` with a server-side streaming RPC) and the shared `NumberRequest`/`NumberReply` message types.
- **Code generation** — `grpc_tools.protoc` compiles the `.proto` file into `service_pb2.py` (message classes) and `service_pb2_grpc.py` (client stubs and server base classes).
- **Server implementation** — `CubeServicer.GetCube()` returns the cube of a number; `StreamServicer.CountUp()` is a generator that `yield`s successive `NumberReply` messages, demonstrating server-side streaming.
- **Client** — connecting via `grpc.insecure_channel`, calling the unary RPC, and consuming the streaming response in a `for` loop.
- A standalone simulation class mirrors the same logic without grpcio, so `main.py` is runnable immediately.

```bash
cd session_12 && uv sync && uv run python main.py
```

---

## Session 13 — Web Best Practices

Good web application structure is about more than just making things work — it's about making them easy to maintain, debug, and extend. This session compares Django and FastAPI side by side and implements production-quality patterns in both.

Topics covered:

- **Project structure** — Django's convention-over-configuration layout (apps, models, views) vs FastAPI's explicit, code-first approach (routers, Pydantic schemas, dependency injection).
- **CORS middleware** — adding `CORSMiddleware` in FastAPI to control which origins are allowed to make cross-origin requests from a browser.
- **Global exception handler** — a FastAPI `@app.exception_handler(Exception)` that catches unhandled errors, logs them with the full traceback, and returns a consistent `500` JSON response instead of leaking internal details.
- **Pydantic models** — using `BaseModel` for request body validation; FastAPI automatically returns a `422 Unprocessable Entity` with field-level error details if the input doesn't conform.
- **Structured error responses** — consistent `{"detail": "..."}` format for both 404 and 422 errors, mirrored in the standalone stdlib HTTP server.

```bash
cd session_13 && uv sync && uv run uvicorn main:app --reload
```

---

## Session 14 — AI Agents (Intro)

AI agents are software components that perceive input, apply decision logic, and produce a response — forming the building block of conversational interfaces and task automation systems. This session introduces the concept using a standalone implementation that mirrors the CrewAI interface.

Topics covered:

- **Base `Agent` class** — a minimal agent that echoes back any query, establishing the `respond(query)` interface used throughout the session.
- **`GreetingAgent`** — extends the base class to return a fixed reply when a specific trigger phrase (`"hello"`) is detected, and falls back to the parent behaviour otherwise.
- **`KeywordAgent`** — a configurable agent that maps keywords to canned responses using a dictionary. All keys are lowercased at construction time so matching is case-insensitive. If no keyword matches, a configurable default reply is returned.
- **CrewAI integration** — the standalone classes use the same `Agent(name=...)` / `agent.respond(query)` interface as the real CrewAI framework, so swapping in `from crewai import Agent` is a one-line change.

```bash
cd session_14 && uv run python main.py
```

---

## Session 15 — Advanced AI Agents

This session extends the agent model with state persistence, real-time external data, and structured query parsing — capabilities that distinguish a basic echo bot from a useful assistant.

Topics covered:

- **`StatefulAgent`** — stores every query in a `history` list. Responding with `"history"` causes the agent to replay all previous queries, demonstrating how an agent can maintain context across a conversation turn.
- **`WeatherAgent`** — integrates with the `wttr.in` public weather API (no API key required). A query prefixed with `"weather "` triggers an HTTP call, parses the JSON response, and returns the current temperature in Celsius for the given city.
- **`SmartAgent`** — a structured-query dispatcher that routes requests by prefix: `"weather <city>"` → weather lookup, `"time"` → current UTC time from `datetime.utcnow()`, `"history"` → conversation replay, anything else → an explicit "I don't know" fallback.
- Error handling in the weather fetch — network failures and API errors are caught and returned as human-readable messages rather than raising exceptions.

```bash
cd session_15 && uv run python main.py
```
