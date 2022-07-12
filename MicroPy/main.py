from machine import Pin, SPI, UART
from sh1106 import SSD1306_SPI
import framebuf
from time import sleep
from utime import sleep_ms
import struct

uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
spi = SPI(0, 10485760, mosi=Pin(3), sck=Pin(2))
lol=1
oled = SSD1306_SPI(128, 64, spi, Pin(6),Pin(7),Pin(11))
#oled = SSD1306_SPI(WIDTH, HEIGHT, spi, dc,rst, cs) use GPIO PIN NUMBERS
while True:
    try:
#                 oled.fill(0)
                oled.show()
                rxData=bytes()
                lol=bytes()
                
                while uart0.any() > 0:
                    lol = uart0.read(1)
                    
                   
                    rxData += lol
                    
                if len(rxData):
                    oled.fill(0)
                    print(rxData.decode('utf-8'), end='')
                    oled.text(rxData.decode('utf-8'),0,32)
                    
                #sleep(1)
                oled.text("Naman is hero",0,0)
                oled.text("Madhvi is paddu",0,8)
                oled.text("yahi satya hai",0,16)

                oled.show()
                sleep_ms(1000)
    except KeyboardInterrupt:
        break
