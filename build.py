import os
import subprocess
import shutil
from pathlib import Path

def build():
    print("🚀 Starting Build Process (PyInstaller)...")
    
    # Paths
    base_dir = Path(__file__).parent
    main_script = base_dir / "src" / "main.py"
    icon_path = base_dir / "data" / "app-icon" / "icon.ico"
    dist_dir = base_dir / "dist"
    build_dir = base_dir / "build"
    
    # Clean previous builds
    if dist_dir.exists(): shutil.rmtree(dist_dir)
    if build_dir.exists(): shutil.rmtree(build_dir)
    
    # PyInstaller command
    # Using venv python -m PyInstaller ensures we use the correct env
    python_exe = base_dir / "venv" / "Scripts" / "python.exe"
    
    cmd = [
        str(python_exe), "-m", "PyInstaller",
        "--noconsole",
        "--onedir",  # Folder mode (AV friendly)
        "--clean",
        f"--icon={icon_path}",
        "--add-data=data;data",  # Copy data folder
        "--name=MusicDiscTracker",
        str(main_script)
    ]
    
    print(f"🔨 Running PyInstaller...")
    print(" ".join(cmd))
    
    try:
        process = subprocess.run(cmd, check=True)
        print("\n✅ Build completed successfully!")
        print(f"📂 Output is in: {dist_dir / 'MusicDiscTracker'}")
        print("👉 You can zip this folder and share it!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error code {e.returncode}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    build()
