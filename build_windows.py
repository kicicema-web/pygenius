#!/usr/bin/env python3
"""
Build script for Windows executable
"""

import subprocess
import sys
import os
import shutil

def build_windows_exe():
    """Build Windows executable using PyInstaller"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Install requests
    print("Installing requests...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    
    # Clean previous builds
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "PyGeniusAI",
        "--add-data", "pygenius_desktop.py;.",
        "--clean",
        "--noconfirm",
        "pygenius_desktop.py"
    ]
    
    # Add icon if available
    if os.path.exists("pygenius.ico"):
        cmd.extend(["--icon", "pygenius.ico"])
    
    print("Building Windows executable...")
    print(f"Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "="*50)
        print("Build successful!")
        print("="*50)
        print(f"Executable: dist/PyGeniusAI.exe")
        
        # Create release package
        os.makedirs("release/windows", exist_ok=True)
        shutil.copy("dist/PyGeniusAI.exe", "release/windows/")
        
        # Create README for Windows
        with open("release/windows/README.txt", "w") as f:
            f.write("""PyGenius AI - Windows Edition
==============================

To run PyGenius AI:
1. Double-click on PyGeniusAI.exe

Requirements:
- Windows 10 or later
- Internet connection (for AI features)

Features:
- Code Editor with syntax highlighting
- Built-in Python console
- AI Tutor powered by OpenRouter
- Bug detection and code optimization

Keyboard Shortcuts:
- Ctrl+N: New file
- Ctrl+O: Open file
- Ctrl+S: Save file
- F5: Run code

Support: https://github.com/kicicema-web/pygenius
""")
        
        print(f"\nRelease package created in: release/windows/")
        return True
    else:
        print("Build failed!")
        return False

if __name__ == "__main__":
    success = build_windows_exe()
    sys.exit(0 if success else 1)
