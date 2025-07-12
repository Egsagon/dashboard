# Script to get battery percentage of the Keychron M34K

import time
import pywinusb.hid as hid

TIMEOUT = 1.5 # 1.5 seconds timeout 

PATH = '\\\\?\\hid#vid_3434&pid_d038&mi_03#7&3b030a9f&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}'

BUFFER = [0] * 65
BUFFER[1] = 65
BUFFER[3] = 129
BUFFER[4] = 1
BUFFER[64] = 222

device = hid.HidDevice(PATH)
device.open()

response = None
report = device.find_output_reports()

def handler(data: list) -> None:
    global response
    response = data

report[0].set_raw_data(BUFFER)
device.set_raw_data_handler(handler)
report[0].send()

start = time.time()
while not response:
    time.sleep(.05)

    if time.time() - start > TIMEOUT:
        print(0)
        exit(1)

print(response[7])

# EOF