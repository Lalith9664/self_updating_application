import webview
import time
import signal
import sys
import subprocess
from updater import update_modules

backend_process = None

def start_server():
    global backend_process
    backend_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "api:app", "--port", "8000", "--reload"])

def run_desktop_app():
    # Optional: auto update on startup
    print("Checking updates...")
    update_modules()

    # Start FastAPI server in subprocess with reload
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

    if backend_process:
        backend_process.terminate()

if __name__ == "__main__":
    # Suppress ugly KeyboardInterrupt traceback on Ctrl+C
    def cleanup(*args):
        if backend_process:
            backend_process.terminate()
        sys.exit(0)
    signal.signal(signal.SIGINT, cleanup)
    run_desktop_app()