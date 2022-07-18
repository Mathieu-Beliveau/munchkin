import datetime
import subprocess
import threading
import time

from BlueToothRSSI import BluetoothRSSI


class ScreenLocker:
    SLEEP = 1

    def __init__(self, bt_address):
        self.bt_address = bt_address

    def monitor_and_lock(self):
        b = BluetoothRSSI(addr=self.bt_address)
        while True:
            if b.is_connection_active():
                rssi = b.get_rssi()
                print("Time: {}, Pixel 2 addr: {}, rssi: {}".format(datetime.datetime.now(), self.bt_address, rssi))
                if rssi != 0:
                    subprocess.run("loginctl lock-session ", shell=True)
            else:
                b.connect()
            time.sleep(1)

    def start_monitoring_thread(self):
        thread = threading.Thread(
            target=self.monitor_and_lock,
            args=()
        )
        thread.daemon = True
        thread.start()
        return thread

