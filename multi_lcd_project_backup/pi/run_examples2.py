from time import sleep
import RPi_I2C_driver
import examples2
from i2c_utils import find_attached_i2c_devices
from random import choice

tests = [examples2.test_1, examples2.test_2, examples2.test_3, examples2.flash_LCD]

while True:
    devices = find_attached_i2c_devices()
    device_list = []
    print(f'{len(devices)} devices found.')

    for device in devices:
        try:
            # instantiate an object of the LCD class.
            device_int = int(device, 16)
            lcd = RPi_I2C_driver.lcd(device_int)        
            device_list.append(lcd)
        except:
            print(f'An error occurred instantiating device {device}.')
            sleep(1)



    for lcd in device_list:
        test = choice(tests)
        test(lcd)


