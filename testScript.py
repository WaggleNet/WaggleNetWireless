import digitalio
import board

led = digitalio.DigitalInOut(board.D26)
led.direction = digitalio.Direction.INPUT

print(led)