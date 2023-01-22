# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *
import string
from random import randrange, choice

from os import path
RUNTIME_NAME = path.basename(__file__)

from loguru import logger
# logger.remove()  # stop any default logger
logger.add(f"{RUNTIME_NAME}_{time()}.log") # add a logging file.
LOGGING_LEVEL = "INFO"


@logger.catch
def test_1(device):
    """Display address of device on device.
    """
    logger.info('Function Test_1 start.')
    # display it's address on it's own screen 
    device.lcd_display_string('Test 1', 1)   


@logger.catch
def test_2(device):
    """Original test routines from Denis Pleic
    """
    logger.info('Function Test_2 start.')

    device.lcd_display_string("RPi I2C test #2", 1)
    device.lcd_display_string(" Custom chars", 2)

    sleep(2)  # 2 sec delay

    device.lcd_clear()

    # let's define a custom icon, consisting of 6 individual characters
    # 3 chars in the first row and 3 chars in the second row
    fontdata1 = [
        # Char 0 - Upper-left
        [0x00, 0x00, 0x03, 0x04, 0x08, 0x19, 0x11, 0x10],
        # Char 1 - Upper-middle
        [0x00, 0x1F, 0x00, 0x00, 0x00, 0x11, 0x11, 0x00],
        # Char 2 - Upper-right
        [0x00, 0x00, 0x18, 0x04, 0x02, 0x13, 0x11, 0x01],
        # Char 3 - Lower-left
        [0x12, 0x13, 0x1B, 0x09, 0x04, 0x03, 0x00, 0x00],
        # Char 4 - Lower-middle
        [0x00, 0x11, 0x1F, 0x1F, 0x0E, 0x00, 0x1F, 0x00],
        # Char 5 - Lower-right
        [0x09, 0x19, 0x1B, 0x12, 0x04, 0x18, 0x00, 0x00],
        # Char 6 - my test
        [0x1F, 0x0, 0x4, 0xE, 0x0, 0x1F, 0x1F, 0x1F],
    ]

    # Load logo chars (fontdata1)
    device.lcd_load_custom_chars(fontdata1)


    # Write first three chars to row 1 directly
    device.lcd_write(0x80)
    device.lcd_write_char(0)
    device.lcd_write_char(1)
    device.lcd_write_char(2)
    # Write next three chars to row 2 directly
    device.lcd_write(0xC0)
    device.lcd_write_char(3)
    device.lcd_write_char(4)
    device.lcd_write_char(5)
    sleep(2)

    device.lcd_clear()

    device.lcd_display_string_pos("Testing", 1, 1)  # row 1, column 1
    sleep(1)
    device.lcd_display_string_pos("Testing", 2, 3)  # row 2, column 3
    sleep(1)
    device.lcd_display_string_pos("Testing", 3, 5)  # row 3, column 5
    sleep(1)
    device.lcd_display_string_pos("Testing", 4, 4)  # row 4, column 4
    sleep(1)

    device.lcd_clear()

    # Now let's define some more custom characters
    fontdata2 = [
        # Char 0 - left arrow
        [0x1, 0x3, 0x7, 0xF, 0xF, 0x7, 0x3, 0x1],
        # Char 1 - left one bar
        [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10],
        # Char 2 - left two bars
        [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18],
        # Char 3 - left 3 bars
        [0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C],
        # Char 4 - left 4 bars
        [0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E],
        # Char 5 - left start
        [0x0, 0x1, 0x3, 0x7, 0xF, 0x1F, 0x1F, 0x1F],
        # Char 6 -
        # [ ],
    ]

    # Load logo chars from the second set
    device.lcd_load_custom_chars(fontdata2)

    block = chr(255)  # block character, built-in

    # display two blocks in columns 5 and 6 (i.e. AFTER pos. 4) in row 1
    # first draw two blocks on 5th column (cols 5 and 6), starts from 0
    device.lcd_display_string_pos(block * 2, 1, 4)

    #
    pauza = 0.2  # define duration of sleep(x)
    #
    # now draw cust. chars starting from col. 7 (pos. 6)

    pos = 6
    device.lcd_display_string_pos(chr(1), 1, 6)
    sleep(pauza)

    device.lcd_display_string_pos(chr(2), 1, pos)
    sleep(pauza)

    device.lcd_display_string_pos(chr(3), 1, pos)
    sleep(pauza)

    device.lcd_display_string_pos(chr(4), 1, pos)
    sleep(pauza)

    device.lcd_display_string_pos(block, 1, pos)
    sleep(pauza)

    # and another one, same as above, 1 char-space to the right
    pos = pos + 1  # increase column by one

    device.lcd_display_string_pos(chr(1), 1, pos)
    sleep(pauza)
    device.lcd_display_string_pos(chr(2), 1, pos)
    sleep(pauza)
    device.lcd_display_string_pos(chr(3), 1, pos)
    sleep(pauza)
    device.lcd_display_string_pos(chr(4), 1, pos)
    sleep(pauza)
    device.lcd_display_string_pos(block, 1, pos)
    sleep(pauza)


    #
    # now again load first set of custom chars - smiley
    device.lcd_load_custom_chars(fontdata1)

    device.lcd_display_string_pos(chr(0), 1, 9)
    device.lcd_display_string_pos(chr(1), 1, 10)
    device.lcd_display_string_pos(chr(2), 1, 11)
    device.lcd_display_string_pos(chr(3), 2, 9)
    device.lcd_display_string_pos(chr(4), 2, 10)
    device.lcd_display_string_pos(chr(5), 2, 11)

    sleep(2)
    device.lcd_clear()
    sleep(1)
    device.backlight(0)
    sleep(1)
    return # end of test2 routines


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
