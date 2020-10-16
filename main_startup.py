#!/usr/bin/env python3

import RPi.GPIO as GPIO
import subprocess

from main import run
from audio_output import say

say("TACO is on")

# define GPIO pins to use
GPIO_POWER = 3
GPIO_TRIGGER = None

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_POWER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_TRIGGER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_power = GPIO.input(GPIO_POWER)
button_trigger = GPIO.input(GPIO_TRIGGER)

while True:
    if button_power:
        break
    elif button_trigger:
        run()

say("Shutting down TACO")
subprocess.call(['shutdown', '-h', 'now'], shell=False)
