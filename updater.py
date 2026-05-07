import json
import os
import shutil
import zipfile
import datetime
import requests
import sys
import subprocess
import threading
import time

LOCAL_VERSION_FILE = "version.json"
UPDATES_DIR = "updates"
MODULES_DIR = "app/modules"
UPDATE_BASE_URL = "https://raw.githubusercontent.com/Lalith9664/self_updating_application/main/updates"


def get_local_versions():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return {}
    with open(LOCAL_VERSION_FILE) as f:
        return json.load(f)


def get_remote_versions():
    """Fetch version info from the remote CDN/S3 server."""
    try:
        response = requests.get(f"{UPDATE_BASE_URL}/version.json", timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching remote version: {e}")
        return {}


def get_current_version():
    """Return a simple combined version string from local versions."""
    local = get_local_versions()
    if not local:
        return "0.0.0"
    # Return the version of the first module, or a combined string
    versions = list(local.values())
    return versions[0] if len(versions) == 1 else ", ".join(versions)


def parse_version(v):
    try:
        return tuple(map(int, v.split(".")))
    except ValueError:
        return (0,)


def check_updates():
    """Check for available updates.
    Returns a dict matching the frontend's expected format:
      { updates_available, available_modules, current_version }
    """
    local = get_local_versions()
    remote = get_remote_versions()

    updates = {}
    for module, remote_version in remote.items():
        local_version = local.get(module, "0")
        if parse_version(remote_version) > parse_version(local_version):
            updates[module] = remote_version

    return {
        "updates_available": len(updates) > 0,
        "available_modules": list(updates.keys()),
        "current_version": get_current_version(),
        "local_versions": local,
        "remote_versions": remote,
    }


def install_module(module):
    """Download and install a module from the remote server."""
    zip_url = f"{UPDATE_BASE_URL}/{module}.zip"
    temp_zip_path = os.path.join(UPDATES_DIR, f"{module}.zip")
    
    os.makedirs(UPDATES_DIR, exist_ok=True)
    
    try:
        # Download the zip file from the internet
        print(f"Downloading {zip_url}...")
        response = requests.get(zip_url, stream=True, timeout=10)
        response.raise_for_status()
        
        with open(temp_zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        # Extract the zip file
        extract_path = "."
        
        # If on Windows, we extract to a temp folder and prepare a batch script
        if os.name == 'nt':
            temp_extract = os.path.join(UPDATES_DIR, f"temp_{module}")
            if os.path.exists(temp_extract):
                shutil.rmtree(temp_extract)
            os.makedirs(temp_extract, exist_ok=True)
            
            with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_extract)
                
            # We don't clean up the zip yet; the batch script will handle it
            return {"success": True, "method": "batch", "temp_extract": temp_extract, "temp_zip": temp_zip_path}
            
        else:
            # On Linux/Mac or during development without locks, extract directly
            with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_path)
            os.remove(temp_zip_path)
            return {"success": True, "method": "direct"}
            
    except Exception as e:
        print(f"Error installing module {module}: {e}")
        return {"success": False, "error": str(e)}


def update_modules():
    """Download & install all available updates.
    Returns a dict matching the frontend's expected format:
      { success, status, modules: [{name, status}], timestamp }
    """
    check_result = check_updates()
    available = check_result["available_modules"]

    if not available:
        return {
            "success": True,
            "status": "No updates available",
            "modules": [],
            "timestamp": datetime.datetime.now().isoformat(),
            "current_version": check_result["current_version"],
        }

    module_results = []
    all_success = True

    for module in available:
        try:
            result = install_module(module)
            ok = result.get("success", False)
            module_results.append({
                "name": module,
                "status": "success" if ok else "failed",
                "method": result.get("method"),
                "temp_extract": result.get("temp_extract"),
                "temp_zip": result.get("temp_zip")
            })
            if not ok:
                all_success = False
        except Exception as e:
            module_results.append({"name": module, "status": "failed", "error": str(e)})
            all_success = False

    # Update local version file with newly installed versions
    if all_success or any(r["status"] == "success" for r in module_results):
        local = get_local_versions()
        remote = get_remote_versions()
        for result in module_results:
            if result["status"] == "success" and result["name"] in remote:
                local[result["name"]] = remote[result["name"]]
        with open(LOCAL_VERSION_FILE, "w") as f:
            json.dump(local, f, indent=2)

    # Trigger Windows Batch Updater if needed
    needs_restart = False
    if os.name == 'nt' and all_success:
        for res in module_results:
            if res.get("method") == "batch":
                needs_restart = True
                temp_extract = res["temp_extract"]
                temp_zip = res["temp_zip"]
                
                bat_path = os.path.join(UPDATES_DIR, "update.bat")
                executable = sys.executable
                args = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
                
                bat_content = f"""@echo off
echo Updating App... Please wait.
timeout /t 2 /nobreak > NUL
xcopy /s /y /i "{temp_extract}\\*" "{os.path.abspath('.')}"
rmdir /s /q "{temp_extract}"
del /q "{temp_zip}"
echo Update complete. Restarting...
start "" "{executable}" {args}
del "%~f0"
"""
                with open(bat_path, "w") as f:
                    f.write(bat_content)
                
                print("Launching Windows updater batch script...")
                CREATE_NO_WINDOW = 0x08000000
                subprocess.Popen([bat_path], creationflags=CREATE_NO_WINDOW)
                
                # Shutdown the app gracefully after 1 second so the API can return Success
                def kill_app():
                    time.sleep(1)
                    os._exit(0)
                threading.Thread(target=kill_app).start()
                break

    return {
        "success": all_success,
        "status": "Updated successfully" if all_success else "Completed with errors",
        "modules": module_results,
        "timestamp": datetime.datetime.now().isoformat(),
        "current_version": get_current_version(),
    }