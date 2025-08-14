"""Instruction reordering is extremely unlikely to occur in the code 
you've written because of Python's GIL and memory model - especially 
when using CPython, the standard Python interpreter.

In CPython, instruction reordering will not happen for:
self.x += 1
self.y += 1
self.z += 1
self.w += 1

because of:
The GIL preventing concurrent bytecode execution,
Python's higher-level memory model, and
"""

import threading


class NumberStore:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0

    def increment(self):
        self.x += 1
        self.y += 1
        self.z += 1
        self.w += 1

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_w(self):
        return self.w


number_store = NumberStore()
# Running the thread multiple times
for _ in range(1000000):
    t = threading.Thread(target=number_store.increment)
    current = number_store.get_w()
    t.start()
    # while current == number_store.get_w():
    #     pass
    # Inlined content of check_order()
    if not (
        number_store.get_w() == number_store.get_z()
        or number_store.get_z() == number_store.get_y()
        or number_store.get_y() == number_store.get_x()
    ):
        print(
            f"Reordering detected: \
              x={number_store.get_x()}, \
              y={number_store.get_y}, \
              z={number_store.get_z}, \
              w={number_store.get_w}"
        )

    t.join()

# If your Python program were translated into Java and run under similar
# conditions, you could observe memory reordering issues, output below.
"""
public class NumberStore {
    int x = 0;
    int y = 0;
    int z = 0;
    int w = 0;

    public void increment() {
        x += 1;
        y += 1;
        z += 1;
        w += 1;
    }

    public int getX() { return x; }
    public int getY() { return y; }
    public int getZ() { return z; }
    public int getW() { return w; }

    public static void main(String[] args) throws Exception {
        NumberStore store = new NumberStore();

        for (int i = 0; i < 1000000; i++) {
            Thread t = new Thread(() -> store.increment());

            int currentW = store.getW();
            t.start();

            while (store.getW() == currentW) {
                // busy-wait until increment happens
            }

            int x = store.getX();
            int y = store.getY();
            int z = store.getZ();
            int w = store.getW();

            if (w > z || z > y || y > x) {
                System.out.printf("Reordering detected: 
                x=%d, y=%d, z=%d, w=%d%n", x, y, z, w);
            }

            t.join();
        }
    }
}

Output: 
Reordering detected: x=1, y=1, z=1, w=0
Reordering detected: x=2, y=2, z=1, w=1
Reordering detected: x=4, y=3, z=3, w=3

# Solution to the reordering is synchronized keyword
# Modified increment function as below

public void increment() {
       synchronized {
          x += 1;
          y += 1;
          z += 1;
          w += 1;
      }
    }

"""

# Disclaimer: This code was generated with assistance from GitHub Copilot
# and chatgpt, an AI-powered coding assistant
