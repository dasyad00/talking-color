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
GPIO.setup(GPIO_POWER, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # assume power switch is on
GPIO.setup(GPIO_TRIGGER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # assume trigger is normally open


def on_click_power():
    say("Shutting down TACO")
    subprocess.call(['shutdown', '-h', 'now'], shell=False)


def on_click_trigger():
    run()


GPIO.add_event_detect(GPIO_POWER, GPIO.FALLING, callback=on_click_power)  # catch switching off event
GPIO.add_event_detect(GPIO_TRIGGER, GPIO.RISING, callback=on_click_trigger)  # catch pressing in event
