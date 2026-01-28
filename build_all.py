#!/usr/bin/env python3
"""
Master build script - builds all packages
"""

import subprocess
import sys
import os
import shutil

def run_build(script_name):
    """Run a build script"""
    print(f"\n{'='*60}")
    print(f"Running {script_name}...")
    print('='*60)
    result = subprocess.run([sys.executable, script_name])
    return result.returncode == 0

def main():
    """Build all packages"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                PyGenius AI - Build All                       ║
║                                                              ║
║  Building packages for:                                      ║
║    • Windows (.exe)                                          ║
║    • Linux (.deb package)                                    ║
║    • Linux (AppImage)                                        ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Clean release directory
    if os.path.exists("release"):
        shutil.rmtree("release")
    os.makedirs("release", exist_ok=True)
    
    results = {}
    
    # Build Windows executable (only on Windows or with Wine)
    if sys.platform == "win32" or os.environ.get("BUILD_WINDOWS"):
        results["Windows .exe"] = run_build("build_windows.py")
    else:
        print("\n[SKIP] Windows executable - requires Windows or BUILD_WINDOWS env var")
        results["Windows .exe"] = None
    
    # Build Debian package
    if sys.platform.startswith("linux"):
        results["Linux .deb"] = run_build("build_deb.py")
    else:
        print("\n[SKIP] Debian package - requires Linux")
        results["Linux .deb"] = None
    
    # Build AppImage
    if sys.platform.startswith("linux"):
        results["Linux AppImage"] = run_build("build_appimage.py")
    else:
        print("\n[SKIP] AppImage - requires Linux")
        results["Linux AppImage"] = None
    
    # Print summary
    print("\n" + "="*60)
    print("BUILD SUMMARY")
    print("="*60)
    
    for name, result in results.items():
        if result is True:
            status = "✓ SUCCESS"
        elif result is False:
            status = "✗ FAILED"
        else:
            status = "⊘ SKIPPED"
        print(f"  {name:25} {status}")
    
    print("\n" + "="*60)
    print("RELEASE FILES")
    print("="*60)
    
    release_dir = "release"
    if os.path.exists(release_dir):
        for root, dirs, files in os.walk(release_dir):
            level = root.replace(release_dir, '').count(os.sep)
            indent = '  ' * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = '  ' * (level + 1)
            for file in files:
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                size_str = f"{size/1024/1024:.1f} MB" if size > 1024*1024 else f"{size/1024:.1f} KB"
                print(f'{subindent}{file} ({size_str})')
    
    print("\n" + "="*60)
    print("Build complete!")
    print("="*60)
    
    # Return success if at least one build succeeded
    return any(r for r in results.values() if r is not None)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
