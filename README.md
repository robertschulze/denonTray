# denonTray
This is a simple tool to remote control your Denon or compatible (e.g. Marantz) receiver 
from Windows by placing an icon in the system tray. The options are accessible from the
icon's context menu. Double-clicking the tray icon turns on the receiver.

![Screenshot](screenshot.png?raw=True)

The tool is based on the [denonavr](https://github.com/scarface-4711/denonavr)
and [info.systray](https://github.com/Infinidat/infi.systray) packages.

#### Configuration
The configuration is maintained in ```config.yml``` file. 
There is one only one configuration option that needs to be set specifically for your
home network, namely the hostname or IP address of you receiver:

```receiver_address: 192.168.3.46```

#### Installation
* install Python
* install dependencies
``` pip install denonavr infi.systray ```
* clone this repository