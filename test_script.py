import digitalio
import board
import time

pin = digitalio.DigitalInOut(board.LED)
print(pin.value)
pin.direction = digitalio.Direction.OUTPUT

while(True):
    pin.value = not pin.value
    time.sleep(0.1)
    print(pin.value)