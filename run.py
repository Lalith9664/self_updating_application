import webview
import time
import signal
import sys
import threading
import uvicorn
from api import app
from updater import update_modules

def start_server():
    def run():
        # Passing the app object directly avoids PyInstaller string-resolution issues
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
    t = threading.Thread(target=run, daemon=True)
    t.start()

def run_desktop_app():
    # Optional: auto update on startup
    print("Checking updates...")
    update_modules()

    # Start FastAPI server in a background thread
    start_server()

    # Wait for server to be ready
    time.sleep(2)

    # Launch desktop window — try GTK first, fall back to QT or default
    webview.create_window(
        "Self-Updating App",
        "http://127.0.0.1:8000",
        width=720,
        height=600,
        resizable=True,
    )

    try:
        webview.start(gui="gtk")
    except Exception:
        try:
            webview.start(gui="qt")
        except Exception:
            webview.start()

if __name__ == "__main__":
    # Suppress ugly KeyboardInterrupt traceback on Ctrl+C
    def cleanup(*args):
        sys.exit(0)
    signal.signal(signal.SIGINT, cleanup)
    run_desktop_app()