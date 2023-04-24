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

chess_board_prev = [""] * 8
chess_board_cur = [""] * 8


def move_button_callback(channel):
    global chess_board_prev
    global chess_board_cur
    for addr in range(8):
        addr_str = f'{addr:06b}'[::-1]
        for i in range(6):
            GPIO.output(MUX_ADDR[i], int(addr_str[i]))
        value = GPIO.input(MUX_OUT)
        chess_board_cur[addr] = str(value)

    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    # for i in range(8):
    #    for j in range(1):
    #        print(f"{chess_board_cur[i]} ", end="")
    # print("")
    # for square in range(8):
    #    if chess_board_prev[square] != chess_board_cur[square]:
    #        print(f"square={square} was {chess_board_prev[square]} now {chess_board_cur[square]}")
    # chess_board_prev = chess_board_cur
    print(" ".join(chess_board_cur))
    draw.text((10, 10), " ".join(chess_board_cur), font=font, fill=255)
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
