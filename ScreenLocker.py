import datetime
import subprocess
import threading
import time

from PyQt5.QtCore import QObject

from BlueToothRSSI import BluetoothRSSI


class ScreenLocker(QObject):
    SLEEP = 1

    def __init__(self, context, device_address):
        super().__init__()
        self.context = context
        self.device_address = device_address

    def monitor_and_lock(self):
        b = BluetoothRSSI(addr=self.device_address)
        reads_above_threshold = 0
        while True:
            if b.is_connection_active():
                rssi = b.get_rssi()
                if self.context.calibration_mode:
                    print("Time: {}, Address: {}, rssi: {}".format(datetime.datetime.now(), self.device_address, rssi))
                if rssi >= self.context.min_sensitivity:
                    reads_above_threshold += 1
                    if reads_above_threshold >= self.context.min_consecutives:
                        subprocess.run("loginctl lock-session ", shell=True)
                        reads_above_threshold = 0
            else:
                b.connect()
            time.sleep(1)

