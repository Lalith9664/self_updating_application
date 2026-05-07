import os
import subprocess
import sys

def build_app():
    print("🚀 Starting build process for Windows Application...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller.__main__
    except ImportError:
        print("PyInstaller not found. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        import PyInstaller.__main__

    # Define PyInstaller arguments
    # --noconsole: Hides the command prompt window
    # --onedir: Packages into a folder (so our updater batch script can replace files safely)
    # --add-data: Includes required folders and files
    
    separator = ';' if os.name == 'nt' else ':'
    
    pyinstaller_args = [
        "run.py",
        "--name=SelfUpdatingApp",
        "--noconsole",
        "--onedir", 
        f"--add-data=app{separator}app",
        f"--add-data=version.json{separator}.",
        "--clean",
        "-y" # Automatically overwrite old builds
    ]

    print("\nRunning PyInstaller...")
    PyInstaller.__main__.run(pyinstaller_args)
    
    print("\n✅ Build complete!")
    print("Your 'Real App' is located in the 'dist/SelfUpdatingApp' folder.")
    print("You can zip this folder and send it to your Windows users.")

if __name__ == "__main__":
    build_app()
