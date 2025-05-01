#!/bin/bash
REPO_URL="https://raw.githubusercontent.com/Dabrox02/appimage-tool/main/appimage-tool.py"
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_NAME="appimage-tool"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "The directory $INSTALL_DIR does not exist. Creating it..."
    mkdir -p "$INSTALL_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create $INSTALL_DIR. Check your permissions."
        exit 1
    fi
fi

echo "Downloading the script from GitHub..."
curl -L "$REPO_URL" -o "$INSTALL_DIR/$SCRIPT_NAME"

if [ $? -ne 0 ]; then
    echo "Error downloading the script from GitHub."
    exit 1
fi

chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo "The ~/.local/bin directory is not in your PATH."
    echo "To add it, run the following command:"
    echo 'echo "export PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc && source ~/.bashrc'
    echo "Then restart your terminal."
    exit 1
fi

echo "✅ The script has been successfully installed as a CLI tool."
echo "You can now run it using the command: appimage-tool"
