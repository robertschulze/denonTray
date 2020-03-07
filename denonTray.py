import denonavr
from infi.systray import SysTrayIcon

d = denonavr.DenonAVR("192.168.3.46")

dB_add = 80


def powerOn(systray):
    d.power_on()
    print("Turned On.")


def powerOff(systray):
    d.power_off()
    print("Turned Off.")


def volUp(systray):
    d.update()
    v1 = d.volume
    d.set_volume(v1 + 5)
    d.update()
    v2 = d.volume
    print("Volume turned up from %i to %i." % (v1 + dB_add, v2 + dB_add))


def volDown(systray):
    d.update()
    v1 = d.volume
    d.set_volume(v1 - 5)
    d.update()
    v2 = d.volume
    print("Volume turned down from %i to %i." % (v1 + dB_add, v2 + dB_add))


selectors = []
for source in d.input_func_list:
    source_short = ''.join(x for x in source if x.isalpha())
    exec("def select_%s(systray): d.input_func = '%s'" % (source_short, source))
    selectors += [("Select %s" % source, None, eval("select_%s" % source_short))]

menu_options = [("Power On", None, powerOn),
                ("Power Off", None, powerOff),
                ("Volume Up", None, volUp),
                ("Volume Down", None, volDown),
                ] + selectors

systray = SysTrayIcon(r"c:\dokumente\Private\Coding\DenonGui\denon.ico", "DenonAvr GUI", tuple(menu_options))
systray.start()
