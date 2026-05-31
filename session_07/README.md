## Session 7: Implementing Logging Best Practices in Python

**Goal:**
Learn to integrate and configure logging in Python applications for effective debugging and monitoring.

**Definition:**
Logging captures runtime events, errors, and general application flow. Python's built-in logging module, along with third-party libraries like loguru, provides flexibility and ease of use. It is essential for debugging, performance monitoring, and security auditing in production systems.

**Documentation Reference:**

- https://docs.python.org/3/library/logging.html
- https://loguru.readthedocs.io/en/stable/
- https://realpython.com/python-logging/

**Setup:**
```bash
uv sync
uv run python main.py
```

**Tutorial:**
- Basic Logging Setup:
    - Configure the built-in logging module.
```py
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log')
logging.info("This is an info message")
logging.error("This is an error message")
```
- Using loguru:
    - Install and use loguru for a simpler logging experience.
```py
    from loguru import logger

    logger.add("file.log", rotation="1 MB")
    logger.debug("Debug message")
    logger.info("Info message")
    logger.error("Error message")
```
    Explanation: The examples show both native and third-party logging configurations.

### Exercise:

- Problem: Create a Python script that logs messages at DEBUG, INFO, WARNING, and ERROR levels.
    - Steps to Solve:
        - Configure logging using the built-in module.
        - Log messages at different severity levels.

### Challenge:

- Problem: Enhance the logging setup to rotate log files daily and include detailed timestamps.
    - Hint: Use TimedRotatingFileHandler from the logging.handlers module.
