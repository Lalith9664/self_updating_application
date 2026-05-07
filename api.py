import json
import os
import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from updater import check_updates, update_modules, get_current_version

app = FastAPI()

if getattr(sys, 'frozen', False):
    APP_ROOT = sys._MEIPASS
else:
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = os.path.join(APP_ROOT, "app", "templates")
INDEX_HTML = os.path.join(TEMPLATES_DIR, "index.html")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

CONFIG_FILE = os.path.join(APP_ROOT, "config.json")
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
def home(request: Request):
    current_ver = get_current_version()
    return templates.TemplateResponse(request=request, name="index.html", context={"version": current_ver})


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