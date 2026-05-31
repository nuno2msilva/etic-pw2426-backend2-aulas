import html
import re

_USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,20}$")


def sanitise_username(raw: str) -> str:
    stripped = raw.strip()
    if not _USERNAME_RE.match(stripped):
        raise ValueError(f"Invalid username: '{stripped}'")
    return stripped


def sanitise_text(raw: str) -> str:
    """HTML-escape free-text input to neutralise XSS payloads."""
    return html.escape(raw.strip())


def main():
    print("=== Session 10 — Security (standalone demo) ===\n")

    print("Input sanitisation (stdlib only, no dependencies):")
    print(f"  sanitise_username('alice_01')        : {sanitise_username('alice_01')}")
    print(f"  sanitise_text('<script>xss</script>'): {sanitise_text('<script>xss</script>')}")
    try:
        sanitise_username("bad name!")
    except ValueError as e:
        print(f"  rejected invalid username            : {e}")

    print()
    print("Django security features (requires uv sync + manage.py migrate):")
    print("  CSRF protection      — CsrfViewMiddleware + {% csrf_token %} in every form")
    print("  Secure sessions      — HttpOnly=True, SameSite=Strict, expires on browser close")
    print("  Input validation     — Django forms with custom validators + html.escape()")
    print("  Authentication       — @login_required, password hashing via create_user()")
    print("  Audit trail          — Comment.user FK + Comment.created_at auto-timestamp")
    print()
    print("Start the web app:")
    print("  uv sync && python manage.py migrate && python manage.py runserver")
    print("  Visit: http://localhost:8000")


if __name__ == "__main__":
    main()
