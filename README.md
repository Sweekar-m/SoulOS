# soulOS

soulOS is a hybrid desktop and web application that provides both a PyQt5-based GUI and a Flask web interface with real-time communication using Flask-SocketIO. It also supports screen streaming and QR code-based web access.

## Features
- PyQt5 GUI (`softwareUI.py`) for local interaction
- Flask web server with SocketIO for real-time chat and screen streaming
- QR code generation for easy web access
- Modular agent system for intent parsing and tool execution

## Requirements
Install dependencies with:

```
pip install -r requirements.txt
```

## Running the Application

1. Start the application (runs both GUI and web server):

```
python main.py
```

2. Access the web UI:
   - Scan the QR code in the GUI, or
   - Visit `http://<your-ip>:5500` in your browser (the IP is shown in the console and QR code)

3. Use the chat box in the web UI or the input in the GUI to interact with the agent.

## Project Structure

- `main.py` — Entry point, runs both GUI and Flask server
- `flask_app.py` — Flask app and SocketIO logic
- `frontend/softwareUI.py` — PyQt5 GUI
- `frontend/screen_stream.py` — Screen streaming logic
- `agent/` — LLM client, state manager, tool router
- `tools/` — Tool implementations
- `templates/index.html` — Web UI

## Notes
- For best results, run on the same network as your client devices.
- Requires Python 3.7+
- For development only: uses `eventlet` for WebSocket support.

---

Feel free to customize and extend!
# Soul-OS
