"""I do not see race condition at all
You're absolutely right to be skeptical—race conditions in Python threads using 
CPython may not manifest easily due to the Global Interpreter Lock (GIL).

Even though Python threads can interleave operations in a way that theoretically 
causes a race condition, the GIL often serializes thread execution just enough 
that it appears safe in simple CPU-bound operations like counter += 1.
"""

import threading
import time

# Shared variable
counter = 0


def increment():
    global counter
    for _ in range(100000):
        counter += 1  # This operation is not atomic!


# Create two threads that run the increment function
thread1 = threading.Thread(target=increment)
thread2 = threading.Thread(target=increment)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

# Expected: 200000 (100000 + 100000), Actual: often less due to race condition
print("Final counter value:", counter)

"""But: the race condition is still real, just harder to observe without 
forcing it to manifest. Let me help you see it more clearly.

🔁 Force the Race Condition to Appear
We can do two things:
Add a tiny sleep between reading and writing the shared variable.
Split the += into explicit load/modify/store steps.
Here's a modified version that forces the race condition:

### Output:
This gives me output close to 100000 and not 500000
Each thread is:
Reading the current value of counter
Sleeping for 50 microseconds — letting another thread run and 
possibly update the counter

Writing back its stale version + 1, overwriting whatever happened 
during the sleep

This results in most of the increments being lost, and only a 
small fraction (e.g., ~100,000 out of 500,000) actually being committed.
"""


counter = 0


def increment():
    global counter
    for _ in range(100000):
        current = counter  # Read
        time.sleep(0.00001)  # Force thread switch
        counter = current + 1  # Write


# Start two threads
thread1 = threading.Thread(target=increment)
thread2 = threading.Thread(target=increment)
thread3 = threading.Thread(target=increment)
thread4 = threading.Thread(target=increment)
thread5 = threading.Thread(target=increment)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()

print("Final counter value:", counter)


"""
How to Fix above program
Use a Lock to make the critical section (read-modify-write) atomic:
This ensures that only one thread can execute the critical section at a time,
"""


counter = 0
lock = threading.Lock()


def increment():
    global counter
    for _ in range(100000):
        with lock:
            current = counter
            time.sleep(0.00001)
            counter = current + 1


threads = []
for _ in range(5):
    t = threading.Thread(target=increment)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Final counter value with lock:", counter)
# Final counter value with lock: 500000


"""
FINAL OUTPUT

(.env-312) pradip@machine:~/workspace/concurrency$  
cd /home/pradip/workspace/concurrency ; /usr/bin/env /home/pradip/
workspace/concurrency/.env-312/bin/python /home/pradip/.vscode/
extensions/ms-python.debugpy-2025.10.0-linux-x64/bundled/libs/
debugpy/adapter/../../debugpy/launcher 51783 -- /home/pradip/
workspace/concurrency/3_race_condition.py 

Final counter value: 200000
Final counter value: 100001
Final counter value with lock: 500000
"""

# Disclaimer: This code was generated with assistance from
# Chatgpt, an AI-powered assistant
