"""Useful functions for the i2c bus devices.
"""

import smbus

bus = smbus.SMBus(1) # older RaspberryPi devices use '0'

def find_attached_i2c_devices():
    devices = []
    for device in range(128):
        try:
            bus.read_byte(device)
            devices.append(hex(device))
        except OSError as e:
            pass
    return devices
