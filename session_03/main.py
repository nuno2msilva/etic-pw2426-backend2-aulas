import threading
import time
import urllib.request
import os


# --- Tutorial: basic thread ---
# Runs in a separate OS thread; ideal for I/O-bound work
def print_numbers():
    for i in range(5):
        print(f"  number: {i}")
        time.sleep(0.2)


# --- Problem: two threads printing letters and numbers concurrently ---
def print_letters():
    for letter in "ABCDE":
        print(f"  letter: {letter}")
        time.sleep(0.15)


def print_numbers_concurrent():
    for i in range(1, 6):
        print(f"  number: {i}")
        time.sleep(0.15)


# --- Challenge: multi-threaded file downloader ---
def _download_file(url: str, dest: str) -> None:
    """Download a single file; called from a dedicated thread."""
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"  Downloaded {url} → {dest}")
    except Exception as exc:
        print(f"  Failed {url}: {exc}")
    finally:
        # clean up the temp file so the demo leaves no debris
        if os.path.exists(dest):
            os.remove(dest)


def download_concurrently(urls: list[str]) -> None:
    threads = [
        threading.Thread(target=_download_file, args=(url, f"file_{i}.tmp"))
        for i, url in enumerate(urls)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()   # wait for all downloads to finish


def main():
    # Tutorial: single thread
    print("Tutorial — single thread:")
    t = threading.Thread(target=print_numbers)
    t.start()
    t.join()

    # Problem: two concurrent threads
    print("\nProblem — letters and numbers concurrently:")
    t_letters = threading.Thread(target=print_letters)
    t_numbers = threading.Thread(target=print_numbers_concurrent)
    t_letters.start()
    t_numbers.start()
    t_letters.join()
    t_numbers.join()

    # Challenge: concurrent downloads (small public resources)
    print("\nChallenge — concurrent downloads:")
    urls = [
        "https://example.com",
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
    ]
    download_concurrently(urls)


if __name__ == "__main__":
    main()
