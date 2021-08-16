# SPDX-FileCopyrightText: 2021 Sandy Macdonald
#
# SPDX-License-Identifier: MIT

# This example displays a rainbow animation on Keybow 2040's keys.

# Drop the keybow2040.py file into your `lib` folder on your `CIRCUITPY` drive.

import math
import board
import time

from keybow2040 import Keybow2040, number_to_xy, hsv_to_rgb

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Set up consumer control (used to send media key presses)
consumer_control = ConsumerControl(usb_hid.devices)

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
keymap =    [Keycode.LEFT_GUI,                              #   0   Windows Key
             ConsumerControlCode.SCAN_PREVIOUS_TRACK,       #   1   Audio Previous Track
             Keycode.TWO,                                   #   2   Browser Left Tab Switch
             Keycode.THREE,                                 #   3   F13 / Zoom Video Toggle
             "[Keycode.LEFT_CONTROL, Keycode.C]",           #   4   Copy
             ConsumerControlCode.PLAY_PAUSE,                #   5   Audio Pause
             Keycode.SIX,                                   #   6   Browser Right Tab Switch
             Keycode.SEVEN,                                 #   7   F14 / Zoom Audio Toggle
             "[Keycode.LEFT_CONTROL, Keycode.V]",           #   8   Paste
             ConsumerControlCode.SCAN_NEXT_TRACK,           #   9   Audio Next Track
             Keycode.A,                                     #   10  Snipping Tool
             Keycode.B,                                     #   11  Move Window to the Left FancyZone
             Keycode.APPLICATION,                           #   12  Context Menu
             ConsumerControlCode.VOLUME_DECREMENT,          #   13  Audio Lower Volume
             ConsumerControlCode.VOLUME_INCREMENT,          #   14  Audio Increase Volume
             Keycode.F]                                     #   15  Move Window to the Right FancyZone

# Attach handler functions to all of the keys
for key in keys:
    # A press handler that sends the keycode and turns on the LED
    @keybow.on_press(key)
    def press_handler(key):
        if keys[2].pressed:
            keybow.keys[2].set_led(255, 255, 255)
            keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB)
        elif keys[3].pressed:
            keybow.keys[3].set_led(255, 255, 255)
            keyboard.send(Keycode.F13)
        elif keys[4].pressed:
            keybow.keys[4].set_led(255, 255, 255)
            keyboard.send(Keycode.CONTROL, Keycode.C)
        elif keys[6].pressed:
            keybow.keys[6].set_led(255, 255, 255)
            keyboard.send(Keycode.CONTROL, Keycode.TAB)
        elif keys[7].pressed:
            keybow.keys[7].set_led(255, 255, 255)
            keyboard.send(Keycode.F14)
        elif keys[8].pressed:
            keybow.keys[8].set_led(255, 255, 255)
            keyboard.send(Keycode.CONTROL, Keycode.V)
        elif keys[10].pressed:
            keybow.keys[10].set_led(255, 255, 255)
            keyboard.press(Keycode.WINDOWS)
            keyboard.press(Keycode.SHIFT)
            keyboard.press(Keycode.S)
            keyboard.release(Keycode.S)
            keyboard.release(Keycode.SHIFT)
            keyboard.release(Keycode.WINDOWS)
        elif keys[11].pressed:
            keybow.keys[11].set_led(255, 255, 255)
            keyboard.press(Keycode.WINDOWS)
            keyboard.press(Keycode.LEFT_ARROW)
            keyboard.release(Keycode.LEFT_ARROW)
            keyboard.release(Keycode.WINDOWS)
        elif keys[15].pressed:
            keybow.keys[15].set_led(255, 255, 255)
            keyboard.press(Keycode.WINDOWS)
            keyboard.press(Keycode.RIGHT_ARROW)
            keyboard.release(Keycode.RIGHT_ARROW)
            keyboard.release(Keycode.WINDOWS)
        else:
            key.set_led(255, 255, 255)
            key_press = keymap[key.number]
            keyboard.send(key_press)
            consumer_control.send(key_press)

    # A release handler that turns off the LED
    @keybow.on_release(key)
    def release_handler(key):
        keyboard.release_all()
        key.set_led(255, 255, 255)

# Increment step to shift animation across keys.
step = 0

while True:

    # Always remember to call keybow.update() on every iteration of your loop!
    keybow.update()

    step += 3

    for i in range(16):
        # Convert the key number to an x/y coordinate to calculate the hue
        # in a matrix style-y.
        x, y = number_to_xy(i)

        # Calculate the hue.
        hue = (x + y + (step / 20)) / 8
        hue = hue - int(hue)
        hue = hue - math.floor(hue)

        # Convert the hue to RGB values.
        r, g, b = hsv_to_rgb(hue, 1, 1)

        # Display it on the key!
        if keys[i].pressed:
            keys[i].set_led(255, 255, 255)
        else:
            keys[i].set_led(r, g, b)
