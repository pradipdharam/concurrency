# Example: Exception in a thread is not caught by the main thread

import threading
import time


def worker():
    time.sleep(1)
    raise ValueError("Exception from thread!")


def main():
    try:
        t = threading.Thread(target=worker)
        t.start()
        t.join()
    except ValueError as e:
        print(f"Caught exception in main: {e}")
    else:
        print("No exception caught in main thread.")


if __name__ == "__main__":
    main()

# Output:
# Exception in thread Thread-1:
# Traceback (most recent call last):
#   ...
# ValueError: Exception from thread!
# No exception caught in main thread.

# Disclaimer: This code was generated with assistance from GitHub Copilot,
# an AI-powered coding assistant
