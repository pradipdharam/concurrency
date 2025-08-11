import threading
import time


def print_numbers():
    for i in range(1, 6):
        print(f"Numbers thread: {i}")
        time.sleep(1)


def print_letters():
    for letter in ["A", "B", "C", "D", "E"]:
        print(f"Letters thread: {letter}")
        time.sleep(1)


def main_calculation():
    for i in range(1, 6):
        result = i * i
        print(f"Main thread calculation: {i}^2 = {result}")
        time.sleep(1)


# Create threads
t1 = threading.Thread(target=print_numbers)
t2 = threading.Thread(target=print_letters)

# Start threads
t1.start()
t2.start()

# Main thread does its own calculation concurrently
main_calculation()

# Wait for both threads to finish
t1.join()
t2.join()

print("All threads have finished.")

# Disclaimer: This code was generated with assistance from GitHub Copilot,
# an AI-powered coding assistant
