#!/usr/bin/env python

import smbus
from random import choice
from time import sleep
import examples
from i2c_utils import find_attached_i2c_devices

tests = [examples.test_1, examples.test_2, examples.test_3]

while True:
    devices = find_attached_i2c_devices()

    print(f'{len(devices)} devices found.')

    for test in tests:
        try:
            c = choice(devices)
            c_int = int(c, 16)
            examples.flash_LCD(c_int)        
            test(c_int)
            sleep(1)
        except:
            print('An error occurred.')
            sleep(5)
