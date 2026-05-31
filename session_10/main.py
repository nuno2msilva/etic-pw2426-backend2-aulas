import html
import re
from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

# --- Security constants ---
SECRET_KEY = "change-me-in-production"   # must be long + random in real apps
ALGORITHM = "HS256"

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ---------------------------------------------------------------------------
# Input sanitisation helpers
# ---------------------------------------------------------------------------

_USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,32}$")


def sanitise_username(raw: str) -> str:
    stripped = raw.strip()
    if not _USERNAME_RE.match(stripped):
        raise ValueError(f"Invalid username: '{stripped}'")
    return stripped


def sanitise_text(raw: str) -> str:
    """HTML-escape free-text input to neutralise XSS payloads."""
    return html.escape(raw.strip())


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------

def create_access_token(data: dict, expires_minutes: int = 30) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------------------------------------------------------------------
# Tutorial: JWT-protected endpoint
# ---------------------------------------------------------------------------

@app.post("/token")
async def login(username: str = Query(...), password: str = Query(...)):
    # In production: verify against a hashed password in the database
    if username == "admin" and password == "secret":
        return {"access_token": create_access_token({"sub": username}), "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect credentials")


@app.get("/secure-data")
async def secure_data(user: dict = Depends(verify_token)):
    return {"data": "Secure Information", "user": user}


# ---------------------------------------------------------------------------
# Problem: input validation + sanitisation endpoint
# ---------------------------------------------------------------------------

class UserInput(BaseModel):
    username: str
    comment: str


@app.post("/submit")
async def submit(body: UserInput):
    try:
        safe_username = sanitise_username(body.username)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"username": safe_username, "comment": sanitise_text(body.comment)}


# ---------------------------------------------------------------------------
# Standalone demo
# ---------------------------------------------------------------------------

def main():
    print("Input sanitisation demo:")
    print("  sanitise_username('alice')           :", sanitise_username("alice"))
    print("  sanitise_text('<script>xss</script>'):", sanitise_text("<script>xss</script>"))
    try:
        sanitise_username("bad name!")
    except ValueError as e:
        print("  rejected invalid username            :", e)

    print("\nRun the API server with: uv run uvicorn main:app --reload")
    print("  POST /token?username=admin&password=secret  → JWT")
    print("  GET  /secure-data  (Bearer token required)")
    print("  POST /submit       {\"username\": \"alice\", \"comment\": \"<b>hi</b>\"}")


if __name__ == "__main__":
    main()
