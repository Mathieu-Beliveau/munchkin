import sys

from PyQt5.QtWidgets import QApplication

from munchkin.Munchkin import Munchkin


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Munchkin")
    window = Munchkin(app)
    sys.exit(app.exec())
