# tools/show_qr_tool.py
import subprocess
import os

def show_qr_fun():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "qr_launcher.py"))
    subprocess.Popen(["python", path])
    return "📲 QR code is now visible."
