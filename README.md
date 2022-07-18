#Munchkin
##About
Munchkin is a simple python application to automatically lock your screen when you are away.
##How it works
The application looks for a list of bluetooth devices (specified with the --devices arg.) 
and will lock the screen as soon as the link quality between your PC and any of those devices drops.

The metric for accessing the link quality is the standard RSSI value where 0 is considered optimal and 
any value above is a mark of a degradation of some kind. For this reason, the application works bests in a noisy 
environment where the signal would quickly degrade as soon your connected device is at some small
distance from your PC.

The application lives in your system tray. It will show a red icon when encountering a true connection loss.
To prevent locking the user out, the application enters standby mode when failing to reach your bluetooth devices.

##Runtime Arguments

``--devices`` A comma separated list of bluetooth addresses to scan for (in the XX:XX:XX:XX:XX:XX format).

``--min-sensitivity`` The integer RSSI value above which Munchkin will lock the screen (defaults to 1). This can be increased if you experience unwanted locking.

``--min-consecutives`` The minimal (integer) number of consecutive RSSI values above ``min-sensitivity`` after which the screen will be locked (defaults to 1). Like the above setting, this can also be increased to prevent unwanted locks.

``--calibration-mode`` Either true or false, sets the application in calibration mode where scanned RSSI values will be displayed and screen locking will be prevented.

``--theme`` Icon theme to be used, either ``dark`` or ``white``. Use ``dark`` if your desktop theme is dark.

