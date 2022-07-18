import sys
import time
from ScreenLocker import ScreenLocker

BT_ADDR_LIST = ['40:4E:36:B8:01:4B']


def main():
    if not BT_ADDR_LIST:
        print("Please edit this file and set BT_ADDR_LIST variable")
        sys.exit(1)
    threads = []
    for addr in BT_ADDR_LIST:
        screen_locker = ScreenLocker(bt_address=addr)
        th = screen_locker.start_monitoring_thread()
        threads.append(th)
    while True:
        # Keep main thread alive
        time.sleep(1)

main()
