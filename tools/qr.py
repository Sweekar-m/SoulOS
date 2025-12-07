import sys
import random
import qrcode
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout,
    QWidget, QLineEdit, QHBoxLayout, QFrame
)
import os

# Always save to soulOS/access_code.txt, no matter where this script is run from
base_dir = os.path.dirname(os.path.abspath(__file__))  # tools/
project_root = os.path.abspath(os.path.join(base_dir, ".."))  # soulOS/
access_code_path = os.path.join(project_root, "access_code.txt")

class QRWidget(QWidget):
    def __init__(self, link=""):
        super().__init__()
        
            # Dynamically get local IP and set default link
        import socket
        ip = socket.gethostbyname(socket.gethostname())
        self.link = f"http://{ip}:5500"
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        # === Top Bar ===
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_frame = QFrame()
        top_frame.setStyleSheet("background-color: #222;")
        top_frame.setFixedHeight(30)
        minimize_btn = QPushButton("-")
        minimize_btn.clicked.connect(self.showMinimized)
        minimize_btn.setStyleSheet("background: #888; color: white; border: none; width: 30px;")
        close_btn = QPushButton("×")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("background: red; color: white; border: none; width: 30px;")
        top_bar.addStretch()
        top_bar.addWidget(minimize_btn)
        top_bar.addWidget(close_btn)
        top_frame.setLayout(top_bar)

        # === Greeting ===
        self.greet = QLabel("👋 Welcome to Soul OS", self)
        self.greet.setAlignment(Qt.AlignCenter)
        self.greet.setStyleSheet("""
            font-size: 24px;
            color: #ffffff;
            padding: 12px;
            font-weight: 600;
            background-color: #292c3e;
            border-radius: 8px;
            margin-top: 20px;   
        """)

        # === Generate and Save Code ===
        self.code = str(random.randint(1000, 9999))
        with open(access_code_path, "w") as f:
            f.write(self.code)

        # === QR Code ===
        qr_img = qrcode.make(self.link)
        qr_img = qr_img.resize((200, 200))
        img_data = qr_img.convert("RGB").tobytes("raw", "RGB")
        qimg = QImage(img_data, 200, 200, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.qr_label = QLabel(self)
        self.qr_label.setPixmap(pixmap)
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setStyleSheet("margin-top: 15px;")

        # === Code Label ===
        self.code_label = QLabel(f"🔐 Access Code: {self.code}", self)
        self.code_label.setAlignment(Qt.AlignCenter)
        self.code_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #00ffaa;
            margin-bottom: 10px;
            padding: 10px;
            background-color:#292c3e;
            border-radius: 8px;
        """)

        # === Close Button ===
        self.close_btn = QPushButton("Close QR", self)
        self.close_btn.clicked.connect(self.hideGreeting)
        self.close_btn.setStyleSheet("""
            background-color: #292c3e;
            color: white;
            padding: 8px 20px;
            border-radius: 8px;
            font-size: 14px;
        """)

       
        # self.text_input.returnPressed.connect(self.handle_enter)  # Optional: implement handle_enter

        # === Layout ===
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(top_frame)
        layout.addWidget(self.greet, alignment=Qt.AlignCenter)
        layout.addWidget(self.code_label)
        layout.addWidget(self.qr_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.close_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)

    def hideGreeting(self):
        self.greet.hide()
        self.qr_label.hide()
        self.code_label.hide()
        self.close_btn.hide()
        self.setFixedHeight(100)
        self.setGeometry(100, 800, 400, 100)
        self.close()  # Close the widget and exit the app



