#!/usr/bin/env python3
"""
Build script for Debian (.deb) package
"""

import subprocess
import sys
import os
import shutil
import stat

def build_deb_package():
    """Build Debian package"""
    
    package_name = "pygenius-ai"
    version = "1.0.0"
    arch = "all"
    
    # Clean previous builds
    build_dir = "build/deb"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    
    # Create directory structure
    deb_root = f"{build_dir}/{package_name}_{version}_{arch}"
    dirs = [
        f"{deb_root}/DEBIAN",
        f"{deb_root}/usr/bin",
        f"{deb_root}/usr/share/pygenius",
        f"{deb_root}/usr/share/applications",
        f"{deb_root}/usr/share/icons/hicolor/256x256/apps",
        f"{deb_root}/usr/share/doc/pygenius",
        f"{deb_root}/usr/share/man/man1",
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # Copy main application
    shutil.copy("pygenius_desktop.py", f"{deb_root}/usr/share/pygenius/")
    shutil.copy("pygenius", f"{deb_root}/usr/share/pygenius/")
    
    # Create wrapper script in /usr/bin
    wrapper = f"""#!/bin/bash
# PyGenius AI wrapper script
exec python3 /usr/share/pygenius/pygenius_desktop.py "$@"
"""
    with open(f"{deb_root}/usr/bin/pygenius", "w") as f:
        f.write(wrapper)
    os.chmod(f"{deb_root}/usr/bin/pygenius", stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    # Create desktop entry
    desktop_entry = f"""[Desktop Entry]
Name=PyGenius AI
Comment=Python coding assistant with AI-powered features
Exec=pygenius
Type=Application
Icon=pygenius
Categories=Development;IDE;Education;
Terminal=false
StartupNotify=true
MimeType=text/x-python;
"""
    with open(f"{deb_root}/usr/share/applications/pygenius.desktop", "w") as f:
        f.write(desktop_entry)
    
    # Create control file
    control = f"""Package: pygenius-ai
Version: {version}
Section: devel
Priority: optional
Architecture: {arch}
Depends: python3 (>= 3.8), python3-requests, python3-tk
Maintainer: Kicicema Web <kicicema.web@gmail.com>
Description: PyGenius AI - Python coding assistant
 PyGenius AI is a desktop application for Python coding with AI-powered features.
 Features include:
  - Code editor with syntax highlighting
  - Built-in Python console
  - AI Tutor powered by OpenRouter
  - Bug detection and code optimization
Homepage: https://github.com/kicicema-web/pygenius
"""
    with open(f"{deb_root}/DEBIAN/control", "w") as f:
        f.write(control)
    
    # Create postinst script
    postinst = """#!/bin/bash
set -e

# Create icon symlink if needed
if [ ! -f /usr/share/icons/hicolor/256x256/apps/pygenius.png ]; then
    ln -sf /usr/share/icons/hicolor/scalable/apps/applications-python.svg /usr/share/icons/hicolor/256x256/apps/pygenius.png 2>/dev/null || true
fi

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true
fi

echo "PyGenius AI has been installed!"
echo "Run 'pygenius' from terminal or find it in your applications menu."
exit 0
"""
    with open(f"{deb_root}/DEBIAN/postinst", "w") as f:
        f.write(postinst)
    os.chmod(f"{deb_root}/DEBIAN/postinst", stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    # Create prerm script
    prerm = """#!/bin/bash
set -e
exit 0
"""
    with open(f"{deb_root}/DEBIAN/prerm", "w") as f:
        f.write(prerm)
    os.chmod(f"{deb_root}/DEBIAN/prerm", stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    
    # Create copyright file
    copyright = """Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: PyGenius AI
Source: https://github.com/kicicema-web/pygenius

Files: *
Copyright: 2024 Kicicema Web
License: MIT
"""
    with open(f"{deb_root}/usr/share/doc/pygenius/copyright", "w") as f:
        f.write(copyright)
    
    # Build the package
    print("Building Debian package...")
    result = subprocess.run(
        ["dpkg-deb", "--build", deb_root],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        # Move to release directory
        os.makedirs("release/linux", exist_ok=True)
        deb_file = f"{package_name}_{version}_{arch}.deb"
        shutil.move(f"build/deb/{deb_file}", f"release/linux/{deb_file}")
        
        print("\n" + "="*50)
        print("Debian package built successfully!")
        print("="*50)
        print(f"Package: release/linux/{deb_file}")
        print(f"\nTo install: sudo dpkg -i {deb_file}")
        print("If dependencies are missing: sudo apt-get install -f")
        return True
    else:
        print("Build failed!")
        print(result.stderr)
        return False

if __name__ == "__main__":
    success = build_deb_package()
    sys.exit(0 if success else 1)
