#!/usr/bin/env python3
"""
Setup GitHub repository for PyGenius AI
"""

import subprocess
import sys
import os
import json
import urllib.request
import urllib.error

import os

# Get credentials from environment variables
# Set these before running:
#   export GITHUB_USERNAME="your-username"
#   export GITHUB_TOKEN="your-token"
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "kicicema-web")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_NAME = "pygenius"

if not GITHUB_TOKEN:
    print("ERROR: GITHUB_TOKEN environment variable not set!")
    print("Set it with: export GITHUB_TOKEN='your-github-token'")
    sys.exit(1)

def create_github_repo():
    """Create GitHub repository using API"""
    
    print(f"Creating GitHub repository: {GITHUB_USERNAME}/{REPO_NAME}")
    
    url = "https://api.github.com/user/repos"
    data = json.dumps({
        "name": REPO_NAME,
        "description": "PyGenius AI - Python coding assistant with AI-powered features",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True,
        "auto_init": False
    }).encode()
    
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
            print(f"✓ Repository created: {result['html_url']}")
            return result['clone_url']
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print("⚠ Repository may already exist. Continuing...")
            return f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
        else:
            print(f"✗ Error creating repository: {e}")
            return None

def init_local_repo(repo_url):
    """Initialize local git repository and push to GitHub"""
    
    print("\nInitializing local repository...")
    
    # Check if git is initialized
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
        print("✓ Git initialized")
    
    # Configure git
    subprocess.run(["git", "config", "user.email", "kicicema.web@gmail.com"], check=False)
    subprocess.run(["git", "config", "user.name", "Kicicema Web"], check=False)
    
    # Add remote
    subprocess.run(["git", "remote", "remove", "origin"], check=False)
    result = subprocess.run(
        ["git", "remote", "add", "origin", repo_url],
        capture_output=True,
        text=True
    )
    if result.returncode != 0 and "already exists" not in result.stderr:
        # Try with HTTPS including token
        auth_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
        subprocess.run(["git", "remote", "add", "origin", auth_url], check=False)
    
    print(f"✓ Remote added: {repo_url}")
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build artifacts
release/
tools/
*.AppImage
*.deb
*.exe
*.zip

# Keep flathub manifest
!flathub/
"""
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✓ .gitignore created")
    
    # Add all files
    subprocess.run(["git", "add", "-A"], check=True)
    print("✓ Files staged")
    
    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", "Initial release: PyGenius AI Desktop v1.0.0"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✓ Initial commit created")
    else:
        print("⚠ Nothing to commit or commit already exists")
    
    # Push
    print("\nPushing to GitHub...")
    auth_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    result = subprocess.run(
        ["git", "push", "-u", auth_url, "main"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        # Try master branch
        result = subprocess.run(
            ["git", "push", "-u", auth_url, "master"],
            capture_output=True,
            text=True
        )
    
    if result.returncode == 0:
        print("✓ Pushed to GitHub")
    else:
        print(f"⚠ Push result: {result.stderr}")
    
    return True

def create_initial_release():
    """Create initial GitHub release"""
    
    print("\nCreating initial release tag...")
    
    # Create tag
    subprocess.run(["git", "tag", "-a", "v1.0.0", "-m", "PyGenius AI v1.0.0 - Initial Release"], check=False)
    
    # Push tag
    auth_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    subprocess.run(["git", "push", auth_url, "v1.0.0"], check=False)
    
    print("✓ Release tag v1.0.0 created")
    
    return True

def main():
    """Main function"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║          PyGenius AI - GitHub Repository Setup               ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Create GitHub repository
    repo_url = create_github_repo()
    if not repo_url:
        print("Failed to create repository")
        return False
    
    # Initialize local repo
    if not init_local_repo(repo_url):
        print("Failed to initialize local repository")
        return False
    
    # Create initial release
    create_initial_release()
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print(f"\nRepository URL: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
    print(f"Clone URL: {repo_url}")
    print("\nNext steps:")
    print("  1. Visit the repository on GitHub")
    print("  2. Go to Actions tab to enable GitHub Actions")
    print("  3. Run the release workflow to build packages")
    print("  4. Submit to Flathub using flathub/submit.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
