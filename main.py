import sys
import threading
from PyQt5.QtWidgets import QApplication

import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Import the updated UI (your floating window UI)
from frontend.softwareUI import create_ui  

from flask_app import run_flask
from frontend import code_store

# === Access Code ===
user_code = code_store.get_code()
print("Access code is:", user_code)

# === PyQt GUI ===
def run_gui():
    qt_app = QApplication(sys.argv)
    ui = create_ui()   # <-- updated class name
    ui.show()
    sys.exit(qt_app.exec_())

# === Run Both ===
if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    run_gui()   # GUI must run on the main thread
