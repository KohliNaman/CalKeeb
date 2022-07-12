import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1106
import time
from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import usb_hid

uart = busio.UART(board.GP0, board.GP1, baudrate=9600)
displayio.release_displays()
oled_reset = board.GP7
oled_cs = board.GP11
oled_dc = board.GP6
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3)
display_bus = displayio.FourWire(spi,
                                 command=oled_dc,
                                 chip_select=oled_cs,
                                 reset=oled_reset,
                                 baudrate=1000000)
WIDTH = 132
HEIGHT = 64  # Change to 64 if needed
BORDER = 5
display = adafruit_displayio_sh1106.SH1106(display_bus,
                                           width=WIDTH,
                                           height=HEIGHT)
splash = displayio.Group()
display.show(splash)
lol = 0

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

d17 = DigitalInOut(board.GP17)
d17.direction = Direction.INPUT
d17.pull = Pull.UP


def open_app(app):
    kbd.send(Keycode.LEFT_ALT, Keycode.SPACE)
    time.sleep(0.2)
    layout.write(app)
    time.sleep(0.2)
    kbd.send(Keycode.ENTER)


while True:
    if not d17.value:
        kbd.send(Keycode.GUI, Keycode.D)
    #time.sleep(0.5)  # debounce delay

    data = uart.readline()
    if data is not None:
        data_string = ''.join([chr(b) for b in data])
        #print(data_string,end = "")
        text = data_string
        slot3 = data_string[-8:-1]
        slot2 = data_string[-14:-9]
        slot1 = data_string[:-15]

        text_area = label.Label(terminalio.FONT,
                                text=slot1,
                                color=0xFFFF00,
                                x=4,
                                y=4)
        if lol > 0:
            del splash[0]
        splash.append(text_area)
        text_area = label.Label(terminalio.FONT,
                                text=slot2,
                                color=0xFFFF00,
                                x=4,
                                y=16)
        if lol > 0:
            del splash[0]
        splash.append(text_area)
        text_area = label.Label(terminalio.FONT,
                                text=slot3,
                                color=0xFFFF00,
                                x=4,
                                y=28)
        if lol > 0:
            del splash[0]
        splash.append(text_area)
        lol = 1
