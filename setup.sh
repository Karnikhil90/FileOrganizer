#!/bin/bash

# Define the target directory and source directory
SOURCE_DIR="exe"
TARGET_DIR="/usr/local/myapp"  # Update this path as needed
TARGET_ENV_VAR="MYAPP_HOME"

# Create target directory
if [ ! -d "$TARGET_DIR" ]; then
    if mkdir -p "$TARGET_DIR"; then
        echo "Target directory created."
    else
        echo "Error creating target directory" >&2
        exit 1
    fi
else
    echo "Target directory already exists."
fi

# Copy files from source directory to target directory
if cp -r "$SOURCE_DIR/"* "$TARGET_DIR/"; then
    echo "Files copied to $TARGET_DIR"
else
    echo "Error copying files" >&2
    exit 1
fi

# Set environment variable
echo "export $TARGET_ENV_VAR=$TARGET_DIR" >> ~/.bashrc
echo "Environment variable $TARGET_ENV_VAR set to $TARGET_DIR in ~/.bashrc"

# Notify user to reload .bashrc or restart the terminal
echo "Please reload your shell or restart the terminal for the environment variable to take effect."
