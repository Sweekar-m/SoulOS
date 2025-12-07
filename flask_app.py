import socket
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from frontend.screen_stream import screen_stream_blueprint

import pyautogui
from frontend import code_store
from LLM_clusters.parallel_router import run_all_llms
# === Flask App Setup ===
app = Flask(__name__, template_folder="templates")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


# Register screen stream
app.register_blueprint(screen_stream_blueprint, url_prefix="/stream")

# === Flask Routes ===
@app.route("/")
def index():
    print("[Flask] Serving index.html")
    return render_template("index.html")

# === SocketIO Events ===
@socketio.on("connect")
def handle_connect():
    ip = request.remote_addr or "Unknown IP"
    print(f"[SocketIO] Connect Request from: {ip} (SID: {request.sid})")
    socketio.emit("show_connect_prompt", {"ip": ip}, to=request.sid)

@socketio.on("confirm_connection")
def handle_confirm_connection():
    print(f"[SocketIO] Connection confirmed by user {request.sid}")
    socketio.emit("agent_status", {"status": "✅ Connected to Soul OS"}, to=request.sid)
@socketio.on("move_cursor")
def move_cursor(data):
    dx = data.get("dx", 0)
    dy = data.get("dy", 0)
    try:
        pyautogui.moveRel(dx, dy)
    except Exception as e:
        print(f"[Cursor] Error moving: {e}")

@socketio.on("mouse_click")
def handle_mouse_click(data):
    button = data.get("button", "left")
    try:
        pyautogui.click(button=button)
        print(f"[WebClick] {button} click performed")
    except Exception as e:
        print(f"[WebClick] Failed: {e}")

@socketio.on("verify_pin")
def handle_pin(data):
    with open("access_code.txt", "r") as f:
        code = f.read().strip()
    pin = data.get("pin")
    if pin == code:  # You can dynamically generate this too
        print("[✔️] Correct PIN entered.")
        socketio.emit("pin_verified", to=request.sid)
    else:
        print("[❌] Wrong PIN attempt.")
        socketio.emit("pin_failed", to=request.sid)

@socketio.on("chat_message")
def handle_chat_message(data):
    print(f"[SocketIO] Raw message received: {data}")
    prompt = data.get("message", "").strip()
    prompt="web prompt "+prompt
    print(f"💬 User Prompt: {prompt}")
    results = run_all_llms(prompt)
    print(results)
# === Flask Server Runner ===
def run_flask():
    ip = socket.gethostbyname(socket.gethostname())
    print(f"\n🟢 Visit: http://{ip}:5500\n")
    socketio.run(app, host='0.0.0.0', port=5500, allow_unsafe_werkzeug=True, debug=False, use_reloader=False)
