import time

import RPi.GPIO as GPIO
import chess
from Adafruit_SSD1306 import SSD1306_128_32
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from constants import *

""" Represent current reed switches states:
    0 - Reed switch is open -> Square is empty
    1 - Reed switch is close -> Some piece on the square """
mask = [0] * 64

mask_stable = mask.copy()  # Store last legal mask

display = SSD1306_128_32(rst=None)
font = ImageFont.load_default()


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Setup MUX
    GPIO.setup(PIN_MUX_OUT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for pin in PINS_MUX_ADDR:
        GPIO.setup(pin, GPIO.OUT)

    # Setup buttons
    GPIO.setup(PIN_START_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_MOVE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_SELECT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_LEFT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(PIN_RIGHT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Setup display
    display.begin()
    display.clear()
    print_to_display(["Game Start!"])


def print_to_display(text: list[str]):
    image = Image.new("1", (display.width, display.height))
    draw = ImageDraw.Draw(image)
    for i, line in enumerate(text):
        draw.text((5, 5 + i * 10), line, font=font, fill=255)
    display.image(image)
    display.display()


def print_mask():
    for r in range(7, -1, -1):
        for f in range(8):
            i = r * 8 + f
            print(f"{mask[i]}", end=" ")
        print()


def update_mask():
    """ Read all board square states from MUX """
    for addr in range(TOTAL_SQUARES):
        addr_str = f'{addr:06b}'[::-1]
        for i in range(len(PINS_MUX_ADDR)):
            GPIO.output(PINS_MUX_ADDR[i], int(addr_str[i]))
        time.sleep(0)
        mask[addr] = GPIO.input(PIN_MUX_OUT)


def update_mask_stable():
    """ Copy mask into mask_stable """
    global mask_stable
    mask_stable = mask.copy()


def get_changed_squares() -> list[chess.Square]:
    """ Return list of squares which changed its state between current mask and mask_stable """
    return [chess.Square(i) for i in range(TOTAL_SQUARES) if mask[i] != mask_stable[i]]


def is_start_button_pressed() -> bool:
    return GPIO.input(PIN_START_BUTTON)


def is_move_button_pressed() -> bool:
    return GPIO.input(PIN_MOVE_BUTTON)


def is_left_button_pressed() -> bool:
    return GPIO.input(PIN_LEFT_BUTTON)


def is_right_button_pressed() -> bool:
    return GPIO.input(PIN_RIGHT_BUTTON)


def is_select_button_pressed() -> bool:
    return GPIO.input(PIN_SELECT_BUTTON)
