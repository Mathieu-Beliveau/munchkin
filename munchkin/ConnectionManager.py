import bluetooth


class ConnectionManager:
    def __init__(self, device_address):
        super().__init__()
        self.bt_sock = None
        self.device_address = device_address

    def is_connection_active(self):
        try:
            self.bt_sock.getpeername()
            return True
        except:
            return False

    def connect(self):
        if self.bt_sock is not None:
            self.bt_sock.close()
        self.bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        self.bt_sock.connect_ex((self.device_address, 1))  # PSM 1 - Service Discovery
