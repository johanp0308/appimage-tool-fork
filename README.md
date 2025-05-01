# AppImage Tool

**AppImage Tool** is a simple CLI utility to help you install `.AppImage` applications system-wide for your user. It handles permissions, copying, and menu integration for a seamless experience.

## ✨ Features

- Copies your AppImage file to `~/Applications`
- Makes it executable
- Optionally installs an icon (`.png` or `.svg`)
- Creates a `.desktop` entry in your application menu
- Automatically refreshes the application database

## 📦 Installation

You can install this tool via the provided install script:

```bash
curl -L https://raw.githubusercontent.com/Dabrox02/appimage-tool/main/install.sh | bash
