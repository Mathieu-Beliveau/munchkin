import datetime
import subprocess

from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from munchkin.BlueToothRSSI import BluetoothRSSI


class ScreenLocker(QObject):
    REFRESH_RATE_IN_MS = 1000
    connection_status_signal = pyqtSignal(bool)

    def __init__(self, context, device_address):
        super().__init__()
        self.context = context
        self.device_address = device_address
        self.poller = QTimer(self)
        self.poller.timeout.connect(self.monitor_and_lock)
        self.brssi = BluetoothRSSI(addr=self.device_address)
        self.reads_above_threshold = 0

    def monitor_and_lock(self):
        if self.brssi .is_connection_active():
            self.report_connection_active()
            rssi = self.brssi.get_rssi()
            if self.context.calibration_mode:
                print("Time: {}, Address: {}, rssi: {}".format(datetime.datetime.now(), self.device_address, rssi))
            if rssi >= self.context.min_sensitivity:
                self.reads_above_threshold += 1
                if self.reads_above_threshold >= self.context.min_consecutives:
                    if not self.context.calibration_mode:
                        subprocess.run("loginctl lock-session ", shell=True)
                    else:
                        print("Screen locking would have occurred!")
                    self.reads_above_threshold = 0
        else:
            self.report_connection_loss()
            self.brssi.connect()

    def report_connection_active(self):
        self.connection_status_signal.emit(True)

    def report_connection_loss(self):
        self.connection_status_signal.emit(False)

    def polling_start(self):
        self.poller.start(self.REFRESH_RATE_IN_MS)

    def polling_stop(self):
        self.poller.stop()