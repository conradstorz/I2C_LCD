#!/usr/bin/env python

import smbus
from time import sleep
import examples

bus = smbus.SMBus(1) # 1 indicates /dev/i2c-1

while True:
    devices = []
    for device in range(128):
        try:
            bus.read_byte(device)
            print(hex(device))
            devices.append(device)
        except OSError as e:
            pass
    print(f'{len(devices)} devices found.')

    for device in devices:
        try:
            examples.test_1(device)
            # examples.test_2(device)
        except OSError as e:
            print(e)

        try:
            pass
            # examples.test_3(device)
        except OSError as e:
            print(e)

    sleep(1)