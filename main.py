import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QStyle, QAction, QPushButton, \
    QVBoxLayout, QWidget

from ScreenLocker import ScreenLocker
from argparser import parser


class MainWindow(QMainWindow):
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.tray = QSystemTrayIcon()
        self.start_action = QAction("Start", self)
        self.pause_action = QAction("Pause", self)
        self.quit_action = QAction("Exit", self)
        self.context = parser.parse_args()
        self.setup_ui()
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
        thread.started.connect(worker.polling_start)
        worker.connection_status_signal.connect(self.report_connection_status)
        self.start_action.triggered.connect(worker.polling_start)
        self.pause_action.triggered.connect(worker.polling_stop)
        self.workers.append(worker)
        return thread

    def setup_ui(self):
        self.tray.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        tray_menu = QMenu()
        tray_menu.addAction(self.start_action)
        tray_menu.addAction(self.pause_action)
        tray_menu.addAction(self.quit_action)
        self.quit_action.triggered.connect(self.exit)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()

    def report_connection_status(self, status):
        if not status:
            self.tray.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        else:
            self.tray.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray.show()

    def exit(self):
        self.application.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    sys.exit(app.exec())

