import digitalio
import board
import busio
import adafruit_rfm9x
import time

import os

RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.GP5)
RESET = digitalio.DigitalInOut(board.GP6)
spi = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)

rfm9x.coding_rate = 5
rfm9x.spreading_factor = 8
rfm9x.tx_power = 23
rfm9x.enable_crc = False
rfm9x.node = 200
rfm9x.destination = 201

print("hello. Transmitting")
msg = "Hello from the other pico"
while True:
    print("Transmitting")
    if not rfm9x.send_with_ack(bytearray(msg)):
        print("send timeout")
    time.sleep(0.1)
