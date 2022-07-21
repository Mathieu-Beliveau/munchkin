from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QAction

from munchkin.ScreenLocker import ScreenLocker
from munchkin.Status import Status
from munchkin.argparser import parser
import munchkin.icons_resource


class Munchkin(QMainWindow):
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.tray = QSystemTrayIcon()
        self.start_action = QAction("Start", self)
        self.pause_action = QAction("Pause", self)
        self.quit_action = QAction("Exit", self)
        self.context = parser.parse_args()
        self.setup_ui()
        self.status = Status.RUNNING
        self.threads = []
        self.workers = []
        self.create_threads()

    def create_threads(self):
        self.threads.clear()
        self.threads = [
            self.create_thread(device_address)
            for device_address in self.context.devices
        ]
        for thread in self.threads:
            thread.start()

    def create_thread(self, device_address):
        thread = QThread()
        worker = ScreenLocker(self.context, device_address=device_address)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.connection_status_signal.connect(self.report_connection_status)
        self.start_action.triggered.connect(worker.polling_start)
        self.pause_action.triggered.connect(worker.polling_stop)
        self.workers.append(worker)
        return thread

    def setup_ui(self):
        self.tray.setIcon(self.get_standard_icon())
        tray_menu = QMenu()
        tray_menu.addAction(self.start_action)
        self.start_action.triggered.connect(self.set_running)
        tray_menu.addAction(self.pause_action)
        self.pause_action.triggered.connect(self.set_paused)
        tray_menu.addAction(self.quit_action)
        self.quit_action.triggered.connect(self.exit)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()

    def set_running(self):
        self.status = Status.RUNNING
        self.update_icon()

    def set_paused(self):
        self.status = Status.PAUSED
        self.update_icon()

    def report_connection_status(self, is_connected):
        if not is_connected:
            if self.status != Status.CONNECTION_LOST:
                self.status = Status.CONNECTION_LOST
                self.update_icon()
        elif self.status != Status.RUNNING and self.status != Status.PAUSED:
            self.status = Status.RUNNING
            self.update_icon()

    def update_icon(self):
        if self.status == Status.RUNNING:
            self.tray.setIcon(self.get_standard_icon())
        elif self.status == Status.PAUSED:
            self.tray.setIcon(self.get_paused_icon())
        elif self.status == Status.CONNECTION_LOST:
            self.tray.setIcon(self.get_connection_loss_icon())

    def get_standard_icon(self):
        return QIcon(":icons/{}/standard.svg".format(self.context.theme))

    def get_paused_icon(self):
        return QIcon(":icons/{}/paused.svg".format(self.context.theme))

    def get_connection_loss_icon(self):
        return QIcon(":icons/{}/connection_lost.svg".format(self.context.theme))

    def exit(self):
        self.application.quit()

