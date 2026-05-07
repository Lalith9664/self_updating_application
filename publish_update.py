import json
import os
import zipfile

def publish():
    print("🚀 Establishing full update from local code...")
    
    # 1. Get current local version
    try:
        with open("version.json") as f:
            local_version = json.load(f)["module1"]
    except Exception as e:
        print("Error reading local version.json:", e)
        return
        
    # 2. Package the app directory into a zip for the updater
    print("📦 Packaging app/ directory into updates/module1.zip...")
    os.makedirs("updates", exist_ok=True)
    
    with zipfile.ZipFile("updates/module1.zip", "w") as z:
        for root, _, files in os.walk("app"):
            for file in files:
                file_path = os.path.join(root, file)
                z.write(file_path)
                
    # 3. Update remote version file
    print(f"🔄 Setting remote update version to {local_version}...")
    with open("updates/version.json", "w") as f:
        json.dump({"module1": local_version}, f, indent=2)
        
    print(f"\n✅ Full update established! Version {local_version} is now live in the updates/ folder.")

if __name__ == "__main__":
    publish()
