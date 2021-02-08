
from time import sleep
import RPi_I2C_driver
from i2c_utils import find_attached_i2c_devices
import string
from random import randrange, choice
from loguru import logger

import ray

ray.init()

@ray.remote
@logger.catch
def test_3(device):
    """
    """
    logger.info('Function Test_3 start.')

    device.lcd_display_string("RPi I2C test #3", 1)
    sleep(2)
    chars = string.printable
    count = 500
    while count:
        # display some random text
        x = randrange(20)
        y = randrange(4) + 1
        c = choice(chars)
        device.lcd_display_string_pos(c, y, x)
        count -= 1

    device.lcd_clear()
    sleep(1)
    device.backlight(0)    
    sleep(1)
    return

@ray.remote
@logger.catch
def flash_LCD(device):
    """Flash the backlight 3 times.
    """
    logger.info('Function Flash LCD start.')
    count = 3
    while count:
        device.backlight(0)    
        sleep(.1)
        device.backlight(1)    
        sleep(.1)        
        count -= 1


tests = [flash_LCD, test_3]



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

    ray.get([tests[1].remote(device_list[0]), tests[0].remote(device_list[1])])






