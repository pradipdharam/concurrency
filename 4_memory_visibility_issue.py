""" In Python, the alternative to Java's synchronized is using 
a threading.Lock (or RLock) with a with statement. 
This ensures only one thread can execute the code inside the 
with lock: block at a time, similar to Java's synchronized.

Yes, using the same lock for get and set helps prevent memory 
visibility issues in Python.

When a thread acquires a lock, changes made to shared data become
visible to other threads when the lock is released.

This ensures all threads see the most up-to-date value."""

import threading


class SafeValue:
    def __init__(self, value=0):
        self._value = value
        self._lock = threading.Lock()

    def get(self):
        with self._lock:
            return self._value

    def set(self, value):
        with self._lock:
            self._value = value


# Usage example
safe = SafeValue(10)


def worker():
    for _ in range(1000):
        safe.set(safe.get() + 1)


threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(safe.get())

# Disclaimer: This code was generated with assistance from GitHub Copilot,
# an AI-powered coding assistant
