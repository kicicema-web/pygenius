#!/usr/bin/env python3
"""
Build script for Linux AppImage
"""

import subprocess
import sys
import os
import shutil
import urllib.request

def build_appimage():
    """Build AppImage package"""
    
    # Create AppDir structure
    appdir = "build/AppDir"
    if os.path.exists(appdir):
        shutil.rmtree(appdir)
    
    dirs = [
        f"{appdir}/usr/bin",
        f"{appdir}/usr/share/pygenius",
        f"{appdir}/usr/share/applications",
        f"{appdir}/usr/share/icons/hicolor/256x256/apps",
        f"{appdir}/usr/share/metainfo",
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # Copy application files
    shutil.copy("pygenius_desktop.py", f"{appdir}/usr/share/pygenius/")
    shutil.copy("pygenius", f"{appdir}/usr/share/pygenius/")
    
    # Create AppRun script (entry point)
    apprun = """#!/bin/bash
# AppRun script for PyGenius AI AppImage

# Get the directory where this script is located
HERE="$(dirname "$(readlink -f "${0}")")"

# Export Python path
export PYTHONPATH="${HERE}/usr/share/pygenius:${PYTHONPATH}"

# Run the application
exec python3 "${HERE}/usr/share/pygenius/pygenius_desktop.py" "$@"
"""
    with open(f"{appdir}/AppRun", "w") as f:
        f.write(apprun)
    os.chmod(f"{appdir}/AppRun", 0o755)
    
    # Create desktop entry
    desktop_entry = """[Desktop Entry]
Name=PyGenius AI
Exec=AppRun
Icon=pygenius
Type=Application
Categories=Development;IDE;Education;
Comment=Python coding assistant with AI-powered features
Terminal=false
StartupNotify=true
MimeType=text/x-python;
X-AppImage-Name=PyGenius AI
X-AppImage-Version=1.0.0
X-AppImage-Arch=x86_64
"""
    with open(f"{appdir}/pygenius.desktop", "w") as f:
        f.write(desktop_entry)
    shutil.copy(f"{appdir}/pygenius.desktop", f"{appdir}/usr/share/applications/")
    
    # Create a simple icon (we'll use Python logo as base)
    # For now, create a placeholder or copy if exists
    icon_created = False
    if os.path.exists("pygenius.png"):
        shutil.copy("pygenius.png", f"{appdir}/pygenius.png")
        shutil.copy("pygenius.png", f"{appdir}/usr/share/icons/hicolor/256x256/apps/")
        icon_created = True
    elif os.path.exists("pygenius.svg"):
        shutil.copy("pygenius.svg", f"{appdir}/pygenius.svg")
        icon_created = True
    
    if not icon_created:
        # Create a simple text icon placeholder
        print("Note: No icon found. Creating placeholder...")
        # We'll use ImageMagick or create a simple one with Python
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGBA', (256, 256), (30, 30, 30, 255))
            draw = ImageDraw.Draw(img)
            # Draw a simple Python-like logo
            draw.ellipse([40, 40, 120, 120], fill=(55, 118, 171, 255))  # Blue
            draw.ellipse([136, 136, 216, 216], fill=(255, 210, 63, 255))  # Yellow
            draw.text((80, 160), "Py", fill=(255, 255, 255, 255))
            img.save(f"{appdir}/pygenius.png")
            shutil.copy(f"{appdir}/pygenius.png", f"{appdir}/usr/share/icons/hicolor/256x256/apps/")
            icon_created = True
        except ImportError:
            # Just create an empty file as placeholder
            open(f"{appdir}/pygenius.png", "w").close()
    
    # Create AppStream metadata (required for Flathub)
    appdata = """<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
  <id>ai.pygenius.desktop</id>
  <metadata_license>MIT</metadata_license>
  <project_license>MIT</project_license>
  <name>PyGenius AI</name>
  <summary>Python coding assistant with AI-powered features</summary>
  <description>
    <p>
      PyGenius AI is a desktop application for Python coding with AI-powered features.
    </p>
    <p>Features include:</p>
    <ul>
      <li>Code editor with syntax highlighting and line numbers</li>
      <li>Built-in Python console for running code</li>
      <li>AI Tutor powered by OpenRouter API</li>
      <li>Bug detection and code analysis</li>
      <li>Code optimization suggestions</li>
      <li>Dark theme for comfortable coding</li>
    </ul>
  </description>
  <launchable type="desktop-id">pygenius.desktop</launchable>
  <url type="homepage">https://github.com/kicicema-web/pygenius</url>
  <developer_name>Kicicema Web</developer_name>
  <update_contact>kicicema.web@gmail.com</update_contact>
  <content_rating type="oars-1.1" />
  <releases>
    <release version="1.0.0" date="2024-01-28">
      <description>
        <p>Initial release of PyGenius AI Desktop</p>
      </description>
    </release>
  </releases>
</component>
"""
    with open(f"{appdir}/usr/share/metainfo/ai.pygenius.appdata.xml", "w") as f:
        f.write(appdata)
    
    # Download appimagetool if not present
    appimagetool = "tools/appimagetool-x86_64.AppImage"
    os.makedirs("tools", exist_ok=True)
    
    if not os.path.exists(appimagetool):
        print("Downloading appimagetool...")
        url = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
        try:
            urllib.request.urlretrieve(url, appimagetool)
            os.chmod(appimagetool, 0o755)
        except Exception as e:
            print(f"Failed to download appimagetool: {e}")
            print("Please install appimagetool manually")
            return False
    
    # Build the AppImage
    print("Building AppImage...")
    env = os.environ.copy()
    env["ARCH"] = "x86_64"
    
    result = subprocess.run(
        [appimagetool, appdir],
        capture_output=True,
        text=True,
        env=env
    )
    
    if result.returncode == 0:
        # Move to release directory
        os.makedirs("release/linux", exist_ok=True)
        appimage_file = "PyGeniusAI-x86_64.AppImage"
        if os.path.exists(appimage_file):
            shutil.move(appimage_file, f"release/linux/{appimage_file}")
        
        print("\n" + "="*50)
        print("AppImage built successfully!")
        print("="*50)
        print(f"AppImage: release/linux/{appimage_file}")
        print(f"\nTo run: chmod +x {appimage_file} && ./{appimage_file}")
        return True
    else:
        print("Build failed!")
        print(result.stdout)
        print(result.stderr)
        return False

if __name__ == "__main__":
    success = build_appimage()
    sys.exit(0 if success else 1)
