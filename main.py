# #!/usr/bin/python

import time

# For MUX connection
import RPi.GPIO as GPIO

# For display connection
from Adafruit_SSD1306 import SSD1306_128_32
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

MUX_OUT = 23
MUX_ADDR = [17, 27, 22, 5, 6, 13]

MOVE_BUTTON = 14
SHUTDOWN_BUTTON = 15

def move_button_callback(channel):
    chess_board = [""] * 8
    for addr in range(8):    
        addr_str = f'{addr:06b}'[::-1]
        for i in range(6):
            GPIO.output(MUX_ADDR[i], int(addr_str[i]))
        value = GPIO.input(MUX_OUT)
        chess_board[addr] = str(value)
        
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    print("".join(chess_board))
    draw.text((10, 10), "".join(chess_board), font=font, fill=255)
    display.image(image)
    display.display()

def shutdown_button_callback(channel):
    GPIO.cleanup()
    exit(0)

def init():
    GPIO.setwarnings(False)
    
    GPIO.setmode(GPIO.BCM)
    
    # Setup MUX
    GPIO.setup(MUX_OUT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(MUX_ADDR[0], GPIO.OUT)
    GPIO.setup(MUX_ADDR[1], GPIO.OUT)
    GPIO.setup(MUX_ADDR[2], GPIO.OUT)
    GPIO.setup(MUX_ADDR[3], GPIO.OUT)
    GPIO.setup(MUX_ADDR[4], GPIO.OUT)
    GPIO.setup(MUX_ADDR[5], GPIO.OUT)
    
    # Setup buttons
    GPIO.setup(MOVE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(MOVE_BUTTON, GPIO.RISING, callback=move_button_callback)
    GPIO.setup(SHUTDOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(SHUTDOWN_BUTTON, GPIO.RISING, callback=shutdown_button_callback)
    
    # Setup display
    global display
    display = SSD1306_128_32(rst=None)
    display.begin()
    display.clear()
    display.display()

    global width
    width = display.width
    global height
    height = display.height
    image = Image.new("1", (width, height))

    draw = ImageDraw.Draw(image)

    global font
    font = ImageFont.load_default()
    draw.text((10, 10), "Game Start", font=font, fill=255)

    display.image(image)
    display.display()

def main():
    init()

if __name__ == "__main__":
    main()
   
