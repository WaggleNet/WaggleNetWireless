import digitalio as dio
import board
import busio
import adafruit_rfm9x
import time
import os
from datetime import datetime
import boto3

RADIO_FREQ_MHZ = 915.0
CS = dio.DigitalInOut(board.D6)
RESET = dio.DigitalInOut(board.D5)
spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
# rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)

rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000)

rfm9x.coding_rate = 5
rfm9x.spreading_factor = 8
rfm9x.tx_power = 23
rfm9x.enable_crc = False
rfm9x.node = 201
rfm9x.destination = 200

msg = ""
msg_list = ""
HTML_start = "<!DOCTYPE HTML>\n<html><body>"
HTML_end = "</body></html>"
file = open("received.html", "w")
keyfile = open('key.txt')

access_key = keyfile.readline()
secret_key = keyfile.readline()

bucket_name = 'beehive-data-1.0'

last_upload = time.time()

def upload(filepath, stamp):
    s3 = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key=secret_key)
    s3.upload_file(filepath, bucket_name, f'{datetime.now()}-{stamp}')

num_upload = 0

while True:
    msg = rfm9x.receive(keep_listening = True, with_header=True, with_ack=True)
    if(msg is not None):
        print(msg, time.time())
        file.truncate(0)

        now = datetime.now()

        newline = str(now) + ": " + msg.decode(errors='ignore') + "<br>"
        msg_list = newline + msg_list
        file.write(HTML_start + msg_list[0:1000] + HTML_end)
        file.flush()
    else:
        print(f"nothing yet... Rssi: {rfm9x.last_rssi}")
        
    print(f"Rssi: {rfm9x.last_rssi}")	

    if time.time() - last_upload > 20:
        upload("received.html", num_upload)

        num_upload += 1
        last_upload = time.time()
    