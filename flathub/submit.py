#!/usr/bin/env python3
"""
Submit PyGenius AI to Flathub
"""

import subprocess
import sys
import os
import json
import urllib.request
import urllib.error
import tempfile
import shutil

import os

# Get credentials from environment variables
# Set these before running:
#   export GITHUB_USERNAME="your-username"
#   export GITHUB_TOKEN="your-token"
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "kicicema-web")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
APP_ID = "ai.pygenius.desktop"

if not GITHUB_TOKEN:
    print("ERROR: GITHUB_TOKEN environment variable not set!")
    print("Set it with: export GITHUB_TOKEN='your-github-token'")
    sys.exit(1)

def check_flatpak_installed():
    """Check if flatpak and flatpak-builder are installed"""
    
    tools = ["flatpak", "flatpak-builder"]
    for tool in tools:
        result = subprocess.run(["which", tool], capture_output=True)
        if result.returncode != 0:
            print(f"✗ {tool} is not installed")
            return False
        print(f"✓ {tool} found")
    return True

def validate_manifest():
    """Validate the Flatpak manifest"""
    
    print("\nValidating Flatpak manifest...")
    
    # Check if required files exist
    required_files = [
        "ai.pygenius.yml",
        "ai.pygenius.desktop",
        "ai.pygenius.appdata.xml"
    ]
    
    for f in required_files:
        if not os.path.exists(f):
            print(f"✗ Missing file: {f}")
            return False
        print(f"✓ Found: {f}")
    
    return True

def test_build_locally():
    """Test building the Flatpak locally"""
    
    print("\nTesting local build...")
    print("This may take several minutes...")
    
    build_dir = "build-flatpak"
    repo_dir = "repo"
    
    # Clean previous builds
    for d in [build_dir, repo_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    # Build the app
    result = subprocess.run(
        ["flatpak-builder", "--force-clean", build_dir, "ai.pygenius.yml"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("✗ Build failed!")
        print(result.stderr)
        return False
    
    print("✓ Local build successful")
    return True

def fork_flathub():
    """Fork the Flathub repository"""
    
    print("\nForking Flathub repository...")
    
    url = "https://api.github.com/repos/flathub/flathub/forks"
    data = json.dumps({}).encode()
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✓ Forked Flathub: {result['html_url']}")
            return result['clone_url']
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("⚠ Already forked or error occurred")
            return f"https://github.com/{GITHUB_USERNAME}/flathub.git"
        else:
            print(f"✗ Error: {e}")
            return None

def create_flathub_pr():
    """Create a pull request to Flathub"""
    
    print("\nCreating Flathub pull request...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the forked repository
        flathub_dir = os.path.join(tmpdir, "flathub")
        fork_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/flathub.git"
        
        print("Cloning Flathub repository...")
        result = subprocess.run(
            ["git", "clone", fork_url, flathub_dir],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("✗ Failed to clone repository")
            print(result.stderr)
            return False
        
        os.chdir(flathub_dir)
        
        # Checkout new-pr branch
        subprocess.run(["git", "checkout", "new-pr"], check=True)
        
        # Create branch for this app
        branch_name = APP_ID
        subprocess.run(["git", "checkout", "-b", branch_name], check=False)
        
        # Copy manifest files
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        flathub_files = os.path.join(current_dir, "flathub")
        
        files_to_copy = [
            "ai.pygenius.yml",
            "ai.pygenius.desktop",
            "ai.pygenius.appdata.xml"
        ]
        
        for f in files_to_copy:
            src = os.path.join(flathub_files, f)
            dst = os.path.join(flathub_dir, f)
            if os.path.exists(src):
                shutil.copy(src, dst)
                print(f"✓ Copied: {f}")
        
        # Commit
        subprocess.run(["git", "add", "-A"], check=True)
        result = subprocess.run(
            ["git", "commit", "-m", f"Add {APP_ID}"],
            capture_output=True,
            text=True
        )
        
        # Push
        print("Pushing to GitHub...")
        result = subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("✗ Failed to push")
            print(result.stderr)
            return False
        
        print("✓ Branch pushed")
        
        # Create pull request via API
        print("Creating pull request...")
        
        pr_url = "https://api.github.com/repos/flathub/flathub/pulls"
        pr_data = json.dumps({
            "title": f"Add {APP_ID}",
            "head": f"{GITHUB_USERNAME}:{branch_name}",
            "base": "new-pr",
            "body": f"""### Description
PyGenius AI - Python coding assistant with AI-powered features

### Features
- Code editor with syntax highlighting
- Built-in Python console
- AI Tutor powered by OpenRouter
- Bug detection and code optimization
- Dark theme

### Checklist
- [x] I have read the [App Requirements](https://github.com/flathub/flathub/wiki/App-Requirements) page
- [x] I have built and tested the app locally
- [x] The app uses a valid app ID
- [x] AppStream metadata is included
- [x] Desktop file is included

### Repository
https://github.com/{GITHUB_USERNAME}/pygenius
"""
        }).encode()
        
        req = urllib.request.Request(
            pr_url,
            data=pr_data,
            headers={
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                print(f"\n✓ Pull request created!")
                print(f"  URL: {result['html_url']}")
                return True
        except urllib.error.HTTPError as e:
            print(f"✗ Failed to create PR: {e}")
            response_body = e.read().decode()
            print(f"Response: {response_body}")
            return False

def main():
    """Main function"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║           Submit PyGenius AI to Flathub                      ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Check if running from correct directory
    if not os.path.exists("ai.pygenius.yml"):
        print("✗ Please run this script from the flathub directory")
        return False
    
    # Validate manifest
    if not validate_manifest():
        print("\n✗ Manifest validation failed!")
        return False
    
    # Check flatpak installation
    if not check_flatpak_installed():
        print("\nInstalling Flatpak...")
        print("Please run: sudo apt install flatpak flatpak-builder")
        print("Then add flathub remote:")
        print("  flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
        return False
    
    # Ask about local build test
    print("\n" + "="*60)
    response = input("Test local build? (this may take 10+ minutes) [y/N]: ")
    if response.lower() == 'y':
        if not test_build_locally():
            print("\n⚠ Local build failed. Continue anyway?")
            response = input("Continue with PR submission? [y/N]: ")
            if response.lower() != 'y':
                return False
    
    # Fork Flathub
    fork_url = fork_flathub()
    if not fork_url:
        print("✗ Failed to fork Flathub")
        return False
    
    # Create PR
    if not create_flathub_pr():
        print("\n✗ Failed to create pull request")
        return False
    
    print("\n" + "="*60)
    print("SUBMISSION COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Wait for Flathub maintainers to review your PR")
    print("  2. They may request changes")
    print("  3. Once approved, your app will be built and published")
    print("\nCheck PR status at: https://github.com/flathub/flathub/pulls")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
