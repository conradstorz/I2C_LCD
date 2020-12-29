# -*- coding: utf-8 -*-
"""Compiled, mashed and generally mutilated 2014-2015 by Denis Pleic.
	Made available under GNU GENERAL PUBLIC LICENSE

	# Modified Python I2C library for Raspberry Pi
	# as found on http://www.recantha.co.uk/blog/?p=4849
	# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
	# added bits and pieces from various sources
	# By DenisFromHR (Denis Pleic)
	# 2015-02-10, ver 0.1
"""

import smbus
from time import *

# LCD Address
ADDRESS = 0x27

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00
LIGHT_STATE = [LCD_NOBACKLIGHT, LCD_BACKLIGHT]

En = 0b00000100  # Enable bit
Rw = 0b00000010  # Read/Write bit
Rs = 0b00000001  # Register select bit


class i2c_device:
    def __init__(self, addr, port=1):
        self.addr = addr
        self.bus = smbus.SMBus(port)

    def write_cmd(self, cmd):  # Write a single command
        self.bus.write_byte(self.addr, cmd)
        sleep(0.0001)

    def write_cmd_arg(self, cmd, data):  # Write a command and argument
        self.bus.write_byte_data(self.addr, cmd, data)
        sleep(0.0001)

    def write_block_data(self, cmd, data):  # Write a block of data
        self.bus.write_block_data(self.addr, cmd, data)
        sleep(0.0001)

    def read(self):  # Read a single byte
        return self.bus.read_byte(self.addr)

    def read_data(self, cmd):  # Read
        return self.bus.read_byte_data(self.addr, cmd)

    def read_block_data(self, cmd):  # Read a block of data
        return self.bus.read_block_data(self.addr, cmd)


class lcd:
    def __init__(self):  # initializes objects and lcd
        self.lcd_device = i2c_device(ADDRESS)
        # send required startup codes...
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)
        # set startup conditions of device...
        self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        sleep(0.2)

    def lcd_strobe(self, data):  # clocks EN to latch command
        self.lcd_device.write_cmd(data | En | LCD_BACKLIGHT)
        sleep(0.0005)
        self.lcd_device.write_cmd(((data & ~En) | LCD_BACKLIGHT))
        sleep(0.0001)

    def lcd_write_four_bits(self, data):
        self.lcd_device.write_cmd(data | LCD_BACKLIGHT)
        self.lcd_strobe(data)

    def lcd_write(self, cmd, mode=0):  # write a command to lcd
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def lcd_write_char(self, charvalue, mode=1):  
        # write a character to lcd (or character rom) 0x09: backlight | RS=DR<
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))
        # works!

    def lcd_display_string(self, string, line):  # put string function
        # index position zero in line_addr is a dummy never used
        line_addr = [0x00, 0x80, 0xC0, 0x94, 0xD4]
        self.lcd_write(line_addr[line])
        for char in string:
            self.lcd_write(ord(char), Rs)

    def lcd_clear(self):  # clear lcd and set to home
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_RETURNHOME)

    def backlight(self, state):  # for state, 1 = on, 0 = off
        self.lcd_device.write_cmd(LIGHT_STATE[state])

    def lcd_load_custom_chars(self, fontdata):  # add custom characters (0 - 7)
        self.lcd_write(0x40)
        for char in fontdata:
            for line in char:
                self.lcd_write_char(line)

    def lcd_display_string_pos(self, string, line, pos):
        # define precise positioning (addition from the forum discussion)
        position_offset = [0x00, 0x00, 0x40, 0x14, 0x54]
        self.lcd_write(0x80 + pos + position_offset[line])
        for char in string:
            self.lcd_write(ord(char), Rs)
