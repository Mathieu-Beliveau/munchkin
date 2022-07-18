import argparse

parser = argparse.ArgumentParser(description='Lock screen upon loss of bluetooth signal quality for given devices.')
parser.add_argument('--devices', nargs='+', default=[], required=True,
                    help='List of devices addresses to monitor')
parser.add_argument('--min-sensitivity', metavar='min_sensitivity', type=int, default=1, required=False,
                    help='min RSSI value at which screen lock will occur')
parser.add_argument('--calibration-mode', metavar='calibration_mode', type=bool, default=False, required=False,
                    help='Whether to run the application in calibration mode')
parser.add_argument('--theme', metavar='theme', type=str, default='dark', required=False,
                    help='Icon theme to use.', choices=['dark', 'white'])
parser.add_argument('--min-consecutives', metavar='min_consecutives', type=int, default=1, required=False,
                    help='Minimal number of consecutive RSSI reads above min-sensitivity required to lock screen.')
