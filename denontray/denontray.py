#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""System tray remote-control tool for Denon AVR receivers."""
# c:\Portable\Anaconda37\Scripts\black.exe denontray --line-length=79
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
DB_OFFSET = CONFIG.get("db_offset", 80)

if RECEIVER_ADDRESS is None:
    raise Exception("You need to set a receiver_address in config.yml")


def power_on(tray):
    """Power On."""
    AVR.power_on()
    print("Turned On.")
    return tray


def power_off(tray):
    """Power Off."""
    AVR.power_off()
    print("Turned Off.")
    return tray


def volume_up(tray):
    """Volume Up by 5dB."""
    AVR.update()
    volume_before = AVR.volume
    AVR.set_volume(volume_before + 5)
    AVR.update()
    volume_after = AVR.volume
    print(
        "Volume turned up from %i to %i."
        % (volume_before + DB_OFFSET, volume_after + DB_OFFSET)
    )
    return tray


def volume_down(tray):
    """Volume Down by 5dB."""
    AVR.update()
    volume_before = AVR.volume
    AVR.set_volume(volume_before - 5)
    AVR.update()
    volume_after = AVR.volume
    print(
        "Volume turned down from %i to %i."
        % (volume_before + DB_OFFSET, volume_after + DB_OFFSET)
    )
    return tray


# initialize connection
AVR = denonavr.DenonAVR(RECEIVER_ADDRESS)

# create source selection menu options
SOURCE_SELECTORS = []
for source in AVR.input_func_list:
    source_short = "".join(x for x in source if x.isalpha())
    exec("def select_%s(systray): AVR.input_func = '%s'"
         % (source_short, source))
    SOURCE_SELECTORS += [
        ("Select %s" % source, None, eval("select_%s" % source_short))
    ]

# build up full set of tray icon menu options
MENU_OPTIONS = [
    ("Power On", None, power_on),
    ("Power Off", None, power_off),
    ("Volume Up", None, volume_up),
    ("Volume Down", None, volume_down),
] + SOURCE_SELECTORS

# create tray icon and start main loop
SYSTRAY = SysTrayIcon(
    os.path.join(WORK_DIR, "denon.ico"), "denontray", tuple(MENU_OPTIONS)
)
SYSTRAY.start()
