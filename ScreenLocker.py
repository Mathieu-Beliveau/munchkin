import datetime
import subprocess
import threading
import time

from PyQt5.QtCore import QObject, QTimer

from BlueToothRSSI import BluetoothRSSI


class ScreenLocker(QObject):
    SLEEP = 1

    def __init__(self, context, device_address):
        super().__init__()
        self.context = context
        self.device_address = device_address
        self.poller = QTimer(self)
        self.poller.timeout.connect(self.monitor_and_lock)
        self.brssi = BluetoothRSSI(addr=self.device_address)

    def monitor_and_lock(self):
        reads_above_threshold = 0
        if self.brssi .is_connection_active():
            rssi = self.brssi.get_rssi()
            if self.context.calibration_mode:
                print("Time: {}, Address: {}, rssi: {}".format(datetime.datetime.now(), self.device_address, rssi))
            if rssi >= self.context.min_sensitivity:
                reads_above_threshold += 1
                if reads_above_threshold >= self.context.min_consecutives:
                    subprocess.run("loginctl lock-session ", shell=True)
                    reads_above_threshold = 0
        else:
            self.brssi.connect()

    def polling_start(self):
        # slot to call upon when timer should start the routine.
        self.poller.start(1000)
        # the argument specifies the milliseconds the timer waits in between
        # calls of the polling routine. If you want to emulate the polling
        # routine in a while loop, you could pass 0 ms...

    def polling_stop(self):
        # This simply stops the timer. The timer is still "alive" after.
        self.poller.stop()