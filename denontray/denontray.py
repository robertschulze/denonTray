#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""System tray remote-control tool for Denon AVR receivers."""
import os

import denonavr
import yaml
from infi.systray import SysTrayIcon

CONFIG_NAME = "config.yml"

if os.path.exists(CONFIG_NAME):
    WORK_DIR = "."
elif os.path.exists(os.path.join("denontray", CONFIG_NAME)):
    WORK_DIR = "denontray"
else:
    raise Exception("Configuration file %s not found." % CONFIG_NAME)

CONFIG = yaml.safe_load(open(os.path.join(WORK_DIR, CONFIG_NAME)))

RECEIVER_ADDRESS = CONFIG.get("receiver_address")
DB_OFFSET = CONFIG.get("receiver_address", 80)

if RECEIVER_ADDRESS is None:
    raise Exception("You need to set a receiver_address in config.yml")


def power_on(tray):
    """Power On."""
    d.power_on()
    print("Turned On.")


def power_off(tray):
    """Power Off."""
    d.power_off()
    print("Turned Off.")


def volume_up(tray):
    """Volume Up by 5dB."""
    d.update()
    volume_before = d.volume
    d.set_volume(volume_before + 5)
    d.update()
    volume_after = d.volume
    print("Volume turned up from %i to %i."
          % (volume_before + DB_OFFSET, volume_after + DB_OFFSET))


def volume_down(tray):
    """Volume Down by 5dB."""
    d.update()
    volume_before = d.volume
    d.set_volume(volume_before - 5)
    d.update()
    volume_after = d.volume
    print("Volume turned down from %i to %i."
          % (volume_before + DB_OFFSET, volume_after + DB_OFFSET))


# initialize connection
d = denonavr.DenonAVR(RECEIVER_ADDRESS)

# create source selection menu options
SOURCE_SELECTORS = []
for source in d.input_func_list:
    source_short = ''.join(x for x in source if x.isalpha())
    exec("def select_%s(systray): d.input_func = '%s'"
         % (source_short, source))
    SOURCE_SELECTORS += \
        [("Select %s" % source, None, eval("select_%s" % source_short))]

# build up full set of tray icon menu options
MENU_OPTIONS = [("Power On", None, power_on),
                ("Power Off", None, power_off),
                ("Volume Up", None, volume_up),
                ("Volume Down", None, volume_down),
                ] + SOURCE_SELECTORS

# create tray icon and start main loop
SYSTRAY = SysTrayIcon(os.path.join(WORK_DIR, "denon.ico"),
                      "denontray", tuple(MENU_OPTIONS))
SYSTRAY.start()
