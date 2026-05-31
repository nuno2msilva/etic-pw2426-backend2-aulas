## Session 10: Enhancing Security in Python Applications

**Goal:**
Learn techniques to secure Python web applications against common vulnerabilities by building a complete Django application with comprehensive security measures.

**Definition:**
Security in Python involves applying best practices to prevent attacks such as SQL injection, XSS, CSRF, and more. It includes validating user input, using secure authentication methods, secure session management, and implementing proper error handling. These measures are critical in protecting sensitive data and maintaining user trust in web applications.

**Documentation Reference:**

- https://owasp.org/www-project-top-ten/
- https://docs.djangoproject.com/en/5.0/topics/security/
- https://docs.djangoproject.com/en/5.0/ref/csrf/
- https://fastapi.tiangolo.com/advanced/security/

**Setup:**
```bash
uv sync
python manage.py migrate      # Create database tables
python manage.py runserver    # Start development server
```

Then visit: **http://localhost:8000**

**Tutorial:**

This session implements a complete Django security application with three key features:

### 1. CSRF Protection (Cross-Site Request Forgery)
- Django's `CsrfViewMiddleware` automatically protects all forms
- Every POST/PUT/DELETE request validates a CSRF token
- Tokens are auto-generated and embedded in forms via `{% csrf_token %}`

**Implementation:**
- All forms in `templates/` include `{% csrf_token %}`
- Middleware is enabled in [myproject/settings.py](myproject/settings.py#L29)
- See [myapp/forms.py](myapp/forms.py) for form definitions

### 2. Secure Session Management
- Sessions are stored server-side (not in cookies)
- Cookies have `HttpOnly` flag (prevents JavaScript access)
- `SameSite=Strict` mitigates CSRF attacks
- Sessions expire when browser closes

**Configuration in [myproject/settings.py](myproject/settings.py#L73-L85):**
```python
SESSION_COOKIE_SECURE = False      # Set True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True     # Prevent XSS access
SESSION_COOKIE_SAMESITE = 'Strict' # Prevent CSRF
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

### 3. Input Validation & Sanitization
- All user inputs validated via Django forms
- Custom validators check format, length, patterns
- XSS prevention through HTML escaping
- Input sanitization in [myapp/forms.py](myapp/forms.py)

**Features:**
- Username validation (alphanumeric + underscore only)
- Email validation (built-in)
- Password strength enforcement (min 8 chars)
- Comment sanitization (HTML-escape dangerous content)

**Key Files:**
- [myapp/forms.py](myapp/forms.py) — Form validation and sanitization
- [myapp/views.py](myapp/views.py) — Views with security decorators
- [myapp/models.py](myapp/models.py) — Database models with audit trail
- [myproject/settings.py](myproject/settings.py) — Security configuration

### Exercise:

**Problem:** 
Understand how each security layer protects the application.

**Steps to Verify:**
1. Register a new account at http://localhost:8000/register
2. Login and submit a comment
3. Try injecting HTML/JavaScript in the comment field
   - Example: `<script>alert('xss')</script>`
   - Notice it's safely HTML-escaped and displayed as text
4. Check that CSRF token is present in form source (`{% csrf_token %}`)
5. In browser DevTools, verify session cookie has `HttpOnly` flag

### Challenge:

**Problem:** 
Secure a Django application by implementing comprehensive security measures: CSRF protection, secure session management, and input validation.

**Solution Implemented:**
- ✅ CSRF protection via middleware + form tokens
- ✅ Secure session management with HttpOnly cookies
- ✅ Input validation through Django forms
- ✅ XSS prevention via HTML escaping
- ✅ User authentication system
- ✅ Audit trail (each comment linked to user + timestamp)

**Additional Security Features:**
- Password hashing (Django's built-in via `create_user()`)
- Authentication required decorators (`@login_required`)
- HTTP method restrictions (`@require_http_methods`)
- Security headers configured (X-Frame-Options, CSP)

**To Test:**
```bash
# Run the server
python manage.py runserver

# Access admin panel (create superuser first)
python manage.py createsuperuser
# Then visit: http://localhost:8000/admin
```

**Hint:** 
Use Django's built-in security middleware and forms. All major protections are already implemented through Django's default settings and our custom forms/views.

