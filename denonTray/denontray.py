#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""System tray remote-control tool for Denon AVR receivers."""
import os

import denonavr
import yaml
from infi.systray import SysTrayIcon

CONFIG_NAME = "config.yml"

if os.path.exists(CONFIG_NAME):
    work_dir = "."
elif os.path.exists(os.path.join("denonTray", CONFIG_NAME)):
    work_dir = "denonTray"
else:
    raise Exception("Configuration file %s not found." % CONFIG_NAME)

config = yaml.safe_load(open(os.path.join(work_dir, CONFIG_NAME)))

RECEIVER_ADDRESS = config.get("receiver_address")
DB_OFFSET = config.get("receiver_address", 80)

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
    v1 = d.volume
    d.set_volume(v1 + 5)
    d.update()
    v2 = d.volume
    print("Volume turned up from %i to %i."
          % (v1 + DB_OFFSET, v2 + DB_OFFSET))


def volume_down(tray):
    """Volume Down by 5dB."""
    d.update()
    v1 = d.volume
    d.set_volume(v1 - 5)
    d.update()
    v2 = d.volume
    print("Volume turned down from %i to %i."
          % (v1 + DB_OFFSET, v2 + DB_OFFSET))


# initialize connection
d = denonavr.DenonAVR(RECEIVER_ADDRESS)

# create source selection menu options
source_selectors = []
for source in d.input_func_list:
    source_short = ''.join(x for x in source if x.isalpha())
    exec("def select_%s(systray): d.input_func = '%s'"
         % (source_short, source))
    source_selectors += \
        [("Select %s" % source, None, eval("select_%s" % source_short))]

# build up full set of tray icon menu options
menu_options = [("Power On", None, power_on),
                ("Power Off", None, power_off),
                ("Volume Up", None, volume_up),
                ("Volume Down", None, volume_down),
                ] + source_selectors

# create tray icon and start main loop
systray = SysTrayIcon(os.path.join(work_dir, "denon.ico"),
                      "denonTray", tuple(menu_options))
systray.start()
