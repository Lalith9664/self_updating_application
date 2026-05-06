import json
import os
import shutil
import zipfile
import datetime

LOCAL_VERSION_FILE = "version.json"
UPDATES_DIR = "updates"
MODULES_DIR = "app/modules"


def get_local_versions():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return {}
    with open(LOCAL_VERSION_FILE) as f:
        return json.load(f)


def get_remote_versions():
    """Read version info from the local updates/ directory (simulates a remote server)."""
    remote_version_file = os.path.join(UPDATES_DIR, "version.json")
    if not os.path.exists(remote_version_file):
        return {}
    try:
        with open(remote_version_file) as f:
            return json.load(f)
    except Exception:
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
    """Install a module from the local updates/ directory."""
    # Try zip file first
    zip_path = os.path.join(UPDATES_DIR, f"{module}.zip")
    module_dir = os.path.join(UPDATES_DIR, module)
    extract_path = os.path.join(MODULES_DIR, module)
    os.makedirs(extract_path, exist_ok=True)

    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
        return True

    # Fall back to copying the directory if no zip
    if os.path.isdir(module_dir):
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        shutil.copytree(module_dir, extract_path)
        return True

    return False


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
            ok = install_module(module)
            module_results.append({
                "name": module,
                "status": "success" if ok else "failed",
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

    return {
        "success": all_success,
        "status": "Updated successfully" if all_success else "Completed with errors",
        "modules": module_results,
        "timestamp": datetime.datetime.now().isoformat(),
        "current_version": get_current_version(),
    }