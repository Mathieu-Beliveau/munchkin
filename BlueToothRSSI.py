import bluetooth
import bluetooth._bluetooth as bt
import struct
import array
import fcntl

from bluetooth import get_byte


class BluetoothRSSI(object):
    def __init__(self, addr):
        self.addr = addr
        self.hci_sock = bt.hci_open_dev()
        self.hci_fd = self.hci_sock.fileno()
        self.bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.bt_sock.settimeout(10)
        self.connected = False
        self.cmd_pkt = None

    def prep_cmd_pkt(self):
        reqstr = struct.pack(
            "6sB17s", bt.str2ba(self.addr), bt.ACL_LINK, b'\0' * 17)
        request = array.array("b", reqstr)
        handle = fcntl.ioctl(self.hci_fd, bt.HCIGETCONNINFO, request, 1)
        handle = struct.unpack("8xH14x", request.tostring())[0]
        self.cmd_pkt = struct.pack('H', handle)

    def is_connection_active(self):
        try:
            self.bt_sock.getpeername()
            return True
        except:
            return False

    def connect(self):
        self.bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        response = self.bt_sock.connect_ex((self.addr, 1))  # PSM 1 - Service Discovery
        return response == 0

    def get_rssi(self):
        try:
            if self.cmd_pkt is None:
                self.prep_cmd_pkt()
            rssi = bt.hci_send_req(
                self.hci_sock, bt.OGF_STATUS_PARAM,
                bt.OCF_READ_RSSI, bt.EVT_CMD_COMPLETE, 4, self.cmd_pkt)
            rssi = get_byte(rssi[3])
            return rssi
        except IOError:
            return None
