import sys
import time
import traceback

from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSignal, QObject, pyqtSlot, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QStyle, QAction, QPushButton, \
    QHBoxLayout, QVBoxLayout, QWidget

from ScreenLocker import ScreenLocker
from argparser import parser


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tray = QSystemTrayIcon()
        self.context = parser.parse_args()
        self.setup_ui()
        self.threads = []

    def monitor(self):
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
        thread.started.connect(worker.monitor_and_lock)
        return thread

    def setup_ui(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.tray.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        # Tray menu
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray.setContextMenu(tray_menu)
        self.tray.show()
        self.button = QPushButton("start")
        self.button.clicked.connect(self.monitor)
        self.meh = QPushButton("meh")
        self.meh.clicked.connect(self.queef)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.meh)
        self.centralWidget.setLayout(layout)

    def queef(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

