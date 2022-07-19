# Munchkin

## About

Munchkin is a simple python application to automatically lock your screen when you are away.

## How it works

The application looks for a list of bluetooth devices (specified with the --devices arg) 
and will lock the screen as soon as the link quality between your PC and any of those devices drops.

The metric for accessing the link quality is the standard RSSI value where 0 is considered optimal and 
any value above is considered as a degradation of some kind. For this reason, the application works bests in a noisy 
environment where the signal would quickly degrade as soon your connected device is at some small
distance from your PC.

The application lives in your system tray. It will show a red icon when encountering a true connection loss.
To prevent locking the user out, the application enters standby mode when failing to reach your bluetooth devices.

## Building

**Binaries are distributed on the project repository; you can download them directly from there:**

https://github.com/Mathieu-Beliveau/munchkin/releases

If you wish to build against your operating system, some python knowledge is assumed:

Install the following dependencies preferably in a ``venv``:

- pybluez
- PyQt5

Install ``pyinstaller`` through your favorite package manager.

Then generate a standalone executable with, at the projet's root: 

``pyinstaller -p ./.venv/lib/python3.8/site-packages/ --name munchkin --onefile ./cli.py``

(where we specify the venv site-packages to avoid conflicts against system libraries.)

Pyinstaller will generate the final binary in the ``dist`` folder.

### Note: 

The application's icons are bundled as a Qt resource using:

``pyrcc5 ./icons.qrc -o ./munchkin/icons_resource.py``

(On Ubuntu, ``pyrcc5`` is part of the ``pyqt5-dev-tools`` package)

This is required such that the tray icons will show up once the application has been bundled by ``pyinstaller``.

## Runtime Arguments

``--devices`` A comma separated list of bluetooth addresses to scan for (in the XX:XX:XX:XX:XX:XX format).

``--min-sensitivity`` The integer RSSI value above which Munchkin will lock the screen (defaults to 1). This can be increased if you experience unwanted locking.

``--min-consecutives`` The minimal (integer) number of consecutive RSSI values above ``min-sensitivity`` after which the screen will be locked (defaults to 1). Like the above setting, this can also be increased to prevent unwanted screen locking.

``--calibration-mode`` Either true or false, sets the application in calibration mode where scanned RSSI values will be displayed and screen locking will be prevented.

``--theme`` Icon theme to be used, either ``dark`` or ``white``. Use ``dark`` if your desktop theme is dark.

