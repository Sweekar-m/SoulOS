import sys
import qrcode
import random
import socket

from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout,
    QWidget, QLineEdit, QHBoxLayout, QFrame, QScrollArea
)

from tools.general import show_general_response
from LLM_clusters.chat_tool_router import sub_chat_router
from LLM_clusters.parallel_router import getprompt
from frontend import code_store
# ---------------------------------------------------
# GLOBALS
# ---------------------------------------------------
window = None
old_pos = QPoint()
resize_dir = None
EDGE = 8   # Resize border thickness

chat_layout = None
chat_scroll = None
text_input = None


# ---------------------------------------------------
# DETECT EDGE
# ---------------------------------------------------
def get_resize_region(pos, w, h):
    x, y = pos.x(), pos.y()

    left   = x < EDGE
    right  = x > w - EDGE
    top    = y < EDGE
    bottom = y > h - EDGE

    if left and top: return "topleft"
    if right and top: return "topright"
    if left and bottom: return "bottomleft"
    if right and bottom: return "bottomright"
    if left: return "left"
    if right: return "right"
    if top: return "top"
    if bottom: return "bottom"
    return None


# ---------------------------------------------------
# UPDATE CURSOR
# ---------------------------------------------------
def update_cursor(region):
    if region in ("left", "right"):
        window.setCursor(Qt.SizeHorCursor)
    elif region in ("top", "bottom"):
        window.setCursor(Qt.SizeVerCursor)
    elif region in ("topleft", "bottomright"):
        window.setCursor(Qt.SizeFDiagCursor)
    elif region in ("topright", "bottomleft"):
        window.setCursor(Qt.SizeBDiagCursor)
    else:
        window.setCursor(Qt.ArrowCursor)


# ---------------------------------------------------
# MOUSE PRESS
# ---------------------------------------------------
def mousePress(event):
    global old_pos, resize_dir
    if event.button() == Qt.LeftButton:
        old_pos = event.globalPos()
        resize_dir = get_resize_region(event.pos(), window.width(), window.height())


# ---------------------------------------------------
# MOUSE MOVE
# ---------------------------------------------------
def mouseMove(event):
    global old_pos, resize_dir

    w, h = window.width(), window.height()

    # hovering only
    if not event.buttons():
        update_cursor(get_resize_region(event.pos(), w, h))
        return

    # Left button dragging
    if resize_dir:
        geo = window.geometry()
        dx = event.globalX() - old_pos.x()
        dy = event.globalY() - old_pos.y()

        new_geo = QRect(geo)

        if "left" in resize_dir:   new_geo.setLeft(new_geo.left() + dx)
        if "right" in resize_dir:  new_geo.setRight(new_geo.right() + dx)
        if "top" in resize_dir:    new_geo.setTop(new_geo.top() + dy)
        if "bottom" in resize_dir: new_geo.setBottom(new_geo.bottom() + dy)

        if new_geo.width() >= 350: 
            geo.setLeft(new_geo.left())
            geo.setRight(new_geo.right())

        if new_geo.height() >= 450:
            geo.setTop(new_geo.top())
            geo.setBottom(new_geo.bottom())

        window.setGeometry(geo)
        old_pos = event.globalPos()
    else:
        # Drag window
        delta = event.globalPos() - old_pos
        window.move(window.x() + delta.x(), window.y() + delta.y())
        old_pos = event.globalPos()


# ---------------------------------------------------
# MOUSE RELEASE
# ---------------------------------------------------
def mouseRelease(event):
    global resize_dir
    resize_dir = None
    window.setCursor(Qt.ArrowCursor)


# ---------------------------------------------------
# CHAT MESSAGE
# ---------------------------------------------------
def add_chat_message(text, is_user=True):
    global chat_layout, chat_scroll

    bubble_frame = QFrame()
    bubble_layout = QHBoxLayout(bubble_frame)
    bubble_layout.setContentsMargins(5, 5, 5, 5)

    label = QLabel(text)
    label.setWordWrap(True)
    label.setStyleSheet("""
        padding: 10px 15px;
        border-radius: 14px;
        font-size: 18px;
    """)

    if is_user:
        label.setStyleSheet(label.styleSheet() + "background:#4dd0e1;color:black;")
        bubble_layout.addStretch()
        bubble_layout.addWidget(label)
    else:
        label.setStyleSheet(label.styleSheet() + "background:#292c3e;color:white;")
        bubble_layout.addWidget(label)
        bubble_layout.addStretch()

    chat_layout.addWidget(bubble_frame)
    chat_scroll.verticalScrollBar().setValue(chat_scroll.verticalScrollBar().maximum())


# ---------------------------------------------------
# ENTER PRESS
# ---------------------------------------------------
def handle_enter():
    text = text_input.text().strip()
    if not text:
        return
    add_chat_message(text, True)
    getprompt(text)
    reply = show_general_response(text)
    add_chat_message(reply, False)
    text_input.clear()


# ---------------------------------------------------
# CREATE UI
# ---------------------------------------------------
def create_ui():
    global window, chat_layout, chat_scroll, text_input
    global greet, qr_label, code_label, close_btn_qr

    window = QWidget()
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.resize(450, 650)
    window.mousePressEvent = mousePress
    window.mouseMoveEvent = mouseMove
    window.mouseReleaseEvent = mouseRelease

    window.setStyleSheet("background:#232526; border-radius:14px;")

    # ---------------- TOP BAR ----------------
    top_frame = QFrame()
    top_frame.setFixedHeight(34)
    top_frame.setStyleSheet("""
        background:#292c3e;
        border-top-left-radius:14px;
        border-top-right-radius:14px;
    """)

    top_bar = QHBoxLayout(top_frame)
    top_bar.setContentsMargins(10, 0, 10, 0)

    title = QLabel("SoulOS QR Connect")
    title.setStyleSheet("color:white;font-size:16px;font-weight:bold;")
    top_bar.addWidget(title)
    top_bar.addStretch()

    # Minimize
    btn_min = QPushButton("–")
    btn_min.setFixedSize(26, 26)
    btn_min.clicked.connect(window.showMinimized)
    btn_min.setStyleSheet("""
        QPushButton {background:#232526;color:white;border:none;border-radius:5px;}
        QPushButton:hover {background:#444;}
    """)

    # Close
    btn_close = QPushButton("×")
    btn_close.setFixedSize(26, 26)
    btn_close.clicked.connect(window.close)
    btn_close.setStyleSheet("""
        QPushButton {background:#232526;color:#ff4f5e;border:none;border-radius:5px;}
        QPushButton:hover {background:#ff4f5e;color:white;}
    """)

    top_bar.addWidget(btn_min)
    top_bar.addWidget(btn_close)

    # ---------------- QR AREA ----------------
    greet = QLabel("👋 Welcome to SoulOS")
    greet.setStyleSheet("font-size:22px;color:white;padding:10px;")
    greet.setAlignment(Qt.AlignCenter)

    code = str(random.randint(1000, 9999))
    open("access_code.txt", "w").write(code)

    code_label = QLabel(f"Access Code: {code}")
    code_label.setAlignment(Qt.AlignCenter)
    code_label.setStyleSheet("font-size:18px;color:#a020f0;")

    ip = socket.gethostbyname(socket.gethostname())
    link = f"http://{ip}:5500"

    qr_img = qrcode.make(link).resize((200, 200))
    img = qr_img.convert("RGB").tobytes("raw", "RGB")
    qr_pixmap = QPixmap.fromImage(QImage(img, 200, 200, QImage.Format_RGB888))

    qr_label = QLabel()
    qr_label.setPixmap(qr_pixmap)
    qr_label.setAlignment(Qt.AlignCenter)

    close_btn_qr = QPushButton("Close QR")
    close_btn_qr.clicked.connect(lambda: [greet.hide(), qr_label.hide(), code_label.hide(), close_btn_qr.hide()])
    close_btn_qr.setStyleSheet("background:#292c3e;color:white;padding:8px 15px;border-radius:8px;")

    # ---------------- CHAT AREA ----------------
    chat_scroll_area = QScrollArea()
    chat_scroll_area.setWidgetResizable(True)
    chat_scroll_area.setStyleSheet("background:#1a1c25;border:none;")

    chat_container = QWidget()
    chat_layout = QVBoxLayout(chat_container)
    chat_layout.setAlignment(Qt.AlignTop)

    chat_scroll_area.setWidget(chat_container)
    chat_scroll = chat_scroll_area

    # ---------------- INPUT ----------------
    text_input = QLineEdit()
    text_input.setPlaceholderText("Ask SoulOS something…")
    text_input.setStyleSheet("""
        padding:12px;
        font-size:18px;
        border:2px solid #4dd0e1;
        border-radius:10px;
        color:white;
        background:#1a1c25;
    """)
    text_input.returnPressed.connect(handle_enter)

    # ---------------- LAYOUT ----------------
    layout = QVBoxLayout(window)
    layout.setContentsMargins(16, 8, 16, 8)

    layout.addWidget(top_frame)
    layout.addWidget(greet)
    layout.addWidget(code_label)
    layout.addWidget(qr_label)
    layout.addWidget(close_btn_qr, alignment=Qt.AlignCenter)
    layout.addWidget(chat_scroll_area)
    layout.addWidget(text_input)

    return window


# ---------------------------------------------------
# RUN
# ---------------------------------------------------
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ui = create_ui()
#     ui.show()
#     sys.exit(app.exec_())
