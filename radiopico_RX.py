import digitalio as dio
import board
import busio
import adafruit_rfm9x
import time

import os

RADIO_FREQ_MHZ = 915.0
CS = dio.DigitalInOut(board.D11)
RESET = dio.DigitalInOut(board.D5)
spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)

rfm9x.coding_rate = 5
rfm9x.spreading_factor = 8
rfm9x.tx_power = 23
rfm9x.enable_crc = False
rfm9x.node = 201
rfm9x.destination = 200

msg = ""
while True:
    msg = rfm9x.receive(keep_listening = True, with_header=True, with_ack=True)
    if(msg is not None):
        print(msg)
    else:
        print(f"nothing yet... Rssi: {rfm9x.last_rssi}")
        
    print(f"Rssi: {rfm9x.last_rssi}")	