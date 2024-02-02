import sys
import time
#import your module
import exampleModule
import digitalio
import board
import busio
import adafruit_rfm9x
import time
from importlib import reload
import boto3
import numpy as np
import pandas as pd

access_key = 'AKIAWZ7TTR42XDCSCD3V'
secret_key = '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'
bucket_name = 'beehive-data-1.0'
test_file = 'testfile'

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

#list will contain all data collection modules
modules = []

#append it to the list of modules
modules.append(exampleModule.exampleModule())

for module in modules:
    #always use try except when calling module functions to prevent one module
    # from crashing the whole program
    try:
        module.setup()
    except:
        print(f"an exception occurred while setting up {module.name}")

running = True
message_length = 64

def upload(filepath, stamp):
    s3 = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key=secret_key)
    s3.upload_file(filepath, bucket_name, f'testfile-{stamp}')

# for i in range(99):
#     random = np.random.randint(1000, size=1000)
#     print(random)
#     df = pd.DataFrame(random)
#     df.to_csv('./testfile', header=False, index=False)
#     upload('testfile', i)

last_upload = time.time()

to_upload = []
num_upload = 0

while(running):
    transmit = ""
    for module in modules:
        reload(module)
        try:
            poll_result = module.wrap_poll()
            if (poll_result is not None):
                # transmit += f"[\"{module.module_name}\",  \"{poll_result}\"]"
                to_upload.append(f"[\"{module.module_name}\",  \"{poll_result}\"]")
        except:
            e = sys.exception()
            # transmit += f"an exception occurred when polling module \"{module.module_name}\" \n{e}"
            to_upload.append(f"an exception occurred when polling module \"{module.module_name}\" \n{e}")

    
    # for i in range(len(transmit) // message_length + 1):
    #     message = transmit[i : min( (i + 1) * message_length, len(transmit) )]

    #     if message != "":
    #         rfm9x.send_with_ack(bytearray(message))
    #         print(f"sending: {message}")
    
    if time.time() - last_upload > 20:
        with open(f"./testfile_{time.time()}", "w") as f:
            f.write(", ".join(to_upload))
        
        upload(f"./testfile_{time.time()}", num_upload)

        num_upload += 1
        to_upload = []
        last_upload = time.time()