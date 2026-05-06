import json
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from updater import check_updates, update_modules, get_current_version

app = FastAPI()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "app", "templates")
INDEX_HTML = os.path.join(TEMPLATES_DIR, "index.html")

CONFIG_FILE = "config.json"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "auto_update": {
                "enabled": True,
                "check_interval_seconds": 30,
                "auto_install": True,
                "show_notification": True,
            }
        }
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


@app.get("/", response_class=HTMLResponse)
def home():
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/check")
def check():
    return check_updates()


@app.get("/update")
def update():
    return update_modules()


@app.get("/version")
def version():
    return {"current_version": get_current_version()}


@app.get("/settings")
def get_settings():
    return load_config()


@app.post("/settings")
async def post_settings(request: Request):
    try:
        data = await request.json()
        save_config(data)
        return {"success": True, "message": "Settings saved"}
    except Exception as e:
        return {"success": False, "error": str(e)}