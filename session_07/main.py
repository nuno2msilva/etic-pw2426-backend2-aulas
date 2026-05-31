import logging
import logging.handlers
import os
import sys


# --- Tutorial: basic logging configuration ---
# stream=sys.stdout keeps logging on the same stream as print(),
# preventing interleaved output caused by stderr/stdout buffering differences
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)


# --- Problem: log at every severity level ---
def log_all_levels() -> None:
    logging.debug("DEBUG — detailed diagnostic info for developers")
    logging.info("INFO  — general confirmation that things are working")
    logging.warning("WARNING — unexpected but recoverable situation")
    logging.error("ERROR — a serious problem occurred")
    logging.critical("CRITICAL — program may not be able to continue")


# --- Challenge: rotating file handler (daily rotation, 7-day retention) ---
def setup_rotating_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when="midnight",    # rotate at midnight every day
        interval=1,
        backupCount=7,      # keep the last 7 daily log files
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(handler)
    return logger


def main():
    # Tutorial: basic logging (goes to stdout via basicConfig)
    print("Tutorial — basic logging:")
    logging.info("Application started")
    logging.error("Simulated error event")

    # Problem: all severity levels
    print("\nProblem — all log levels:")
    log_all_levels()

    # Challenge: file-based rotating logger
    print("\nChallenge — rotating file logger (writes to app.log):")
    file_logger = setup_rotating_logger("app", "app.log")
    file_logger.info("Rotating logger ready")
    file_logger.warning("This entry goes to app.log and rotates daily")
    print("  Logged to app.log (check the file for output)")

    # clean up demo log file
    if os.path.exists("app.log"):
        os.remove("app.log")


if __name__ == "__main__":
    main()
