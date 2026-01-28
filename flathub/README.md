# Flathub Submission for PyGenius AI

This directory contains the Flatpak manifest and metadata for submitting PyGenius AI to Flathub.

## How to Submit to Flathub

### 1. Fork the Flathub Repository

```bash
git clone https://github.com/flathub/flathub.git
cd flathub
git checkout new-pr
```

### 2. Create the App Repository

Create a new repository for your app:

```bash
# The repository name should match the app-id
# For PyGenius AI: ai.pygenius.desktop
git checkout -b ai.pygenius.desktop
```

### 3. Add the Manifest Files

Copy these files to the flathub repository:
- `ai.pygenius.yml` - Main manifest
- `ai.pygenius.desktop` - Desktop entry
- `ai.pygenius.appdata.xml` - AppStream metadata

### 4. Submit a Pull Request

```bash
git add .
git commit -m "Add PyGenius AI"
git push origin ai.pygenius.desktop
```

Then create a pull request on GitHub.

### 5. Wait for Review

The Flathub maintainers will review your submission. They may ask for changes.

### 6. Automated Builds

Once merged, Flathub will automatically build and publish your app.

## Requirements Checklist

- [ ] App has a unique app ID (`ai.pygenius.desktop`)
- [ ] Desktop file is valid
- [ ] AppStream metadata is valid
- [ ] Icon is included (optional for CLI apps)
- [ ] Screenshot URLs are provided (in AppStream)
- [ ] License is specified
- [ ] OARS rating is included

## Testing Locally

Before submitting, test the Flatpak locally:

```bash
# Install Flatpak builder
sudo apt install flatpak-builder

# Build the app
flatpak-builder --force-clean build-dir ai.pygenius.yml

# Test the app
flatpak-builder --run build-dir ai.pygenius.yml pygenius

# Build a bundle
flatpak-builder --repo=repo --force-clean build-dir ai.pygenius.yml
flatpak build-bundle repo pygenius.flatpak ai.pygenius.desktop

# Install the bundle
flatpak install pygenius.flatpak
```

## References

- [Flathub App Submission](https://github.com/flathub/flathub/wiki/App-Submission)
- [Flatpak Manifest Documentation](https://docs.flatpak.org/en/latest/manifests.html)
- [AppStream Metadata](https://www.freedesktop.org/software/appstream/docs/)
