## Session 10: Security in Python Web Applications

**Goal:**
Learn techniques to secure Python web applications against common vulnerabilities by building a complete Django application with comprehensive security measures.

**Definition:**
Security in Python involves applying best practices to prevent attacks such as SQL injection, XSS, CSRF, and more. It includes validating user input, using secure authentication methods, secure session management, and implementing proper error handling. These measures are critical in protecting sensitive data and maintaining user trust in web applications.

**Documentation Reference:**

- https://owasp.org/www-project-top-ten/
- https://docs.djangoproject.com/en/5.0/topics/security/
- https://docs.djangoproject.com/en/5.0/ref/csrf/

**Setup:**
```bash
uv sync
uv run python manage.py migrate      # Create database tables
uv run python manage.py runserver    # Start development server
```

Then visit: **http://localhost:8000**

**Tutorial:**

This session implements a complete Django security application with five key features.

### 1. CSRF Protection (Cross-Site Request Forgery)
- Django's `CsrfViewMiddleware` automatically protects all forms
- Every POST/PUT/DELETE request validates a CSRF token
- Tokens are auto-generated and embedded in forms via `{% csrf_token %}`

**Implementation:**
- All forms in [templates/](templates/) include `{% csrf_token %}`
- Middleware is enabled in [myproject/settings.py](myproject/settings.py)
- See [myapp/forms.py](myapp/forms.py) for form definitions

### 2. Secure Session Management
- Sessions are stored server-side (not in cookies)
- Cookies have `HttpOnly` flag (prevents JavaScript access)
- `SameSite=Strict` mitigates CSRF attacks
- Sessions expire when browser closes

**Configuration in [myproject/settings.py](myproject/settings.py):**
```python
SESSION_COOKIE_HTTPONLY = True      # Prevent XSS access
SESSION_COOKIE_SAMESITE = "Strict"  # Prevent CSRF
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

### 3. Input Validation & Sanitisation
- All user inputs validated via Django forms
- Custom validators check format, length, and patterns
- XSS prevention through HTML escaping in [myapp/forms.py](myapp/forms.py)

**Features:**
- Username: alphanumeric + underscore, 3–20 chars
- Email validation (built-in Django)
- Password strength enforcement (Django's built-in validators)
- Comment sanitisation: `html.escape()` neutralises XSS payloads

### 4. Authentication & Access Control
- User registration and login with secure password hashing via `create_user()`
- `@login_required` on the comment submission view
- `@require_http_methods(["POST"])` to enforce correct HTTP method

See [myapp/views.py](myapp/views.py).

### 5. Audit Trail
- `Comment.user` — foreign key to the authenticated user
- `Comment.created_at` — auto-populated timestamp (`auto_now_add=True`)

See [myapp/models.py](myapp/models.py).

**Project Layout:**
```
session_10/
├── myproject/        # Django project (settings, urls, wsgi)
├── myapp/            # application (models, views, forms, admin)
│   └── migrations/
├── templates/        # HTML templates (base, home, login, register)
├── main.py           # standalone demo (no dependencies required)
└── manage.py
```

### Exercise

**Steps to Verify:**
1. Register a new account at http://localhost:8000/register
2. Login and submit a comment
3. Try injecting HTML/JavaScript in the comment field
   - Example: `<script>alert('xss')</script>`
   - Notice it is safely HTML-escaped and displayed as text
4. Check that CSRF token is present in form source (`{% csrf_token %}`)
5. In browser DevTools, verify session cookie has `HttpOnly` flag

### Challenge

**Problem:**
Secure a Django application by implementing comprehensive security measures: CSRF protection, secure session management, and input validation.

**Solution Implemented:**
- ✅ CSRF protection via middleware + form tokens
- ✅ Secure session management with HttpOnly cookies
- ✅ Input validation through Django forms
- ✅ XSS prevention via html.escape()
- ✅ User authentication system
- ✅ Audit trail (Comment linked to user + timestamp)

**To Test:**
```bash
uv run python manage.py runserver

# Access admin panel (create superuser first)
uv run python manage.py createsuperuser
# Then visit: http://localhost:8000/admin
```
