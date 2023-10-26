from importlib import reload
import time
# from a import get_a
a = __import__("a")

# a = reload(a)

while True:
    print(a.get_a())
    a = reload(a)
    time.sleep(3)
    