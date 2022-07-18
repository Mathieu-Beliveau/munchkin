import time
from ScreenLocker import ScreenLocker
from argparser import parser


def main():
    context = parser.parse_args()
    threads = []
    for device_address in context.devices:
        screen_locker = ScreenLocker(context, device_address)
        th = screen_locker.start_monitoring_thread()
        threads.append(th)
    while True:
        time.sleep(1)


main()
