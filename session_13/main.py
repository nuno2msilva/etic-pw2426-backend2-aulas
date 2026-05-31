import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

app = FastAPI(title="Session 13 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory item store
# ---------------------------------------------------------------------------

_items: list[dict] = []

# ---------------------------------------------------------------------------
# Challenge: global exception handler — consistent 500 response
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error: %s", exc, exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# ---------------------------------------------------------------------------
# Tutorial: Hello World endpoint
# ---------------------------------------------------------------------------

# Django equivalent:
#   from django.http import JsonResponse
#   def index(request): return JsonResponse({"message": "Hello from Django"})

@app.get("/")
async def index():
    return {"message": "Hello from FastAPI"}


# ---------------------------------------------------------------------------
# Problem: CRUD endpoints with Pydantic validation and structured errors
# ---------------------------------------------------------------------------

class ItemModel(BaseModel):
    name: str
    value: float


@app.post("/items", status_code=201)
async def create_item(item: ItemModel):
    _items.append(item.model_dump())
    logger.info("Created: %s", item.name)
    return {"created": item.model_dump()}


@app.get("/items/{name}")
async def get_item(name: str):
    for item in _items:
        if item["name"] == name:
            return item
    raise HTTPException(status_code=404, detail=f"'{name}' not found")


# ---------------------------------------------------------------------------
# Standalone demo
# ---------------------------------------------------------------------------

def main():
    print("Run the API server with: uv run uvicorn main:app --reload")
    print("  GET  /                  → Hello World")
    print("  POST /items             body: {\"name\": \"widget\", \"value\": 9.99}")
    print("  GET  /items/{name}      → item or 404")


if __name__ == "__main__":
    main()
