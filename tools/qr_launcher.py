# tools/qr_launcher.py
import sys
from PyQt5.QtWidgets import QApplication
from qr import QRWidget


def run_qr():
    app = QApplication(sys.argv)
    w = QRWidget()
    w.setWindowTitle("SoulOS QR")
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_qr()
