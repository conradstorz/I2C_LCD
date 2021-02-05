"""
The following instructions were copied from:
https://rplcd.readthedocs.io/en/stable/index.html
"""

# First, import the RPLCD library from your Python script.

from RPLCD.i2c import CharLCD

"""
Then create a new instance of the CharLCD class. 
For that, you need to know the address of your LCD. 
You can find it on the command line using the sudo i2cdetect 1 command 
(or sudo i2cdetect 0 on the original Raspberry Pi). 
In my case the address of the display was 0x27. 
You also need to provide the name of the I²C port expander that your board uses. 
It should be written on the microchip that’s soldered on to your board. 
Supported port expanders are the PCF8574, the MCP23008 and the MCP23017.
"""

lcd = CharLCD('PCF8574', 0x27)

"""
If you want to customize the way the LCD is instantiated 
(e.g. by changing the number of columns and rows on your display or the I²C port), 
you can change the corresponding parameters. 
Example:

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=20, rows=4, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)

"""

# Now you can write a string to the LCD:

lcd.write_string('Hello world')

# To clean the display, use the clear() method:

lcd.clear()

# You can control line breaks with the newline (\n, moves down 1 line) and carriage return (\r, moves to beginning of line) characters.

lcd.write_string('Hello\r\n  World!')

# And you can also set the cursor position directly:

lcd.cursor_pos = (2, 0)

"""
Regular text can be written to the CharLCD instance using the write_string() method. 
It accepts unicode strings (str in Python 3, unicode in Python 2).

The cursor position can be set by assigning a (row, col) tuple to cursor_pos. 
It can be reset to the starting position with home().

Line feed characters (\n) move down one line and carriage returns 
(\r) move to the beginning of the current line.
"""

lcd.write_string('Raspberry Pi HD44780')
lcd.cursor_pos = (2, 0)
lcd.write_string('https://github.com/\n\rdbrgn/RPLCD')

"""
You can also use the convenience functions cr(), lf() 
and crlf() to write line feed (\n) or carriage return (\r) characters to the display.
"""
lcd.write_string('Hello')
lcd.crlf()
lcd.write_string('world!')

"""
After your script has finished, you may want to close the connection 
and optionally clear the screen with the close() method.
"""

lcd.close(clear=True)

