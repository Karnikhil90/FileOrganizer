"""
===========================
    setup -v2[for windows]
===========================
File Organizer Setup Script
===========================

Design Philosophy:
------------------
This script is designed for flexibility and minimal future code changes. By using constants like `CURRENT_VERSION`, 
the code adapts to new versions effortlessly. It also dynamically handles file additions in `SOFTWARE_DIR`, meaning 
new files can be added without modifying the script. This ensures easy updates and maintenance.

Overview:
---------
1. **Version Control:**
   - The `CURRENT_VERSION` constant defines the current software version.
   - Simply updating this constant allows seamless setup for future versions without changing the core code.

2. **Old Version Cleanup:**
   - The script checks and removes older versions specified in the `OLD_VERSIONS` list to ensure a clean setup.

3. **File Copying:**
   - All files and directories from `SOFTWARE_DIR` are copied to `C://{CURRENT_VERSION}/bin`.
   - No need to update the code when adding new files or folders; everything in `SOFTWARE_DIR` will be handled.

4. **System Path Update:**
   - The `bin` directory is added to the system PATH, allowing easy access to the software from the command line.

5. **Reboot Prompt:**
   - After setup, the user is prompted to reboot for changes (like the PATH update) to take effect.

In summary, this script ensures simple version updates and extensibility without requiring code modifications for each new release.
"""

import os
import sys
import shutil
import platform

# Current version of the software
CURRENT_VERSION: str = 'FileOrganizer_21'

# List of older versions to remove if found
OLD_VERSIONS: list[str] = [
    'FileOrganizer - v1.0',
    'FileOrganizer_v2',
]

# Main software directory where all files will be copied
SOFTWARE_DIR : str = 'bin'

def is_windows() -> bool:
    """Check if the current operating system is Windows."""
    return platform.system() == 'Windows'

def create_directory_structure(version: str) -> tuple[str, str]:
    """Create the main directory and bin directory for the application.

    Args:
        version (str): The current version of the software.

    Returns:
        tuple[str, str]: The main directory and bin directory paths.
    """
    main_dir = f'C:\\{version}'
    bin_dir = os.path.join(main_dir, 'bin')

    # Create the main directory if it doesn't exist
    os.makedirs(main_dir, exist_ok=True)
    print(f"Created directory: {main_dir}")

    # Create the bin directory if it doesn't exist
    os.makedirs(bin_dir, exist_ok=True)
    print(f"Created directory: {bin_dir}")

    return main_dir, bin_dir

def remove_old_versions(old_versions: list[str]) -> None:
    """Remove old version directories if found.

    Args:
        old_versions (list[str]): A list of old version directories to remove.
    """
    for version in old_versions:
        old_version_dir = f'C://{version}'
        if os.path.exists(old_version_dir):
            shutil.rmtree(old_version_dir)
            print(f"Removed old version directory: {old_version_dir}")

def copy_all_files(bin_dir: str) -> None:
    """Copy all files from the software directory to the bin directory.

    Args:
        bin_dir (str): The destination bin directory path.
    """
    try:
        # Ensure the software directory exists
        if os.path.exists(SOFTWARE_DIR):
            # Iterate through all files in SOFTWARE_DIR
            for item in os.listdir(SOFTWARE_DIR):
                source_path = os.path.join(SOFTWARE_DIR, item)
                destination_path = os.path.join(bin_dir, item)
                
                if os.path.isfile(source_path):
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied {source_path} to {destination_path}")
                elif os.path.isdir(source_path):
                    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                    print(f"Copied directory {source_path} to {destination_path}")
        else:
            print(f"{SOFTWARE_DIR} not found. Please ensure it is present.")
    except Exception as e:
        print(f"Error copying files: {e}")

def add_bin_to_system_path(bin_dir: str) -> None:
    """Add the bin directory to the system's Path variable permanently.

    Args:
        bin_dir (str): The bin directory path to add to system Path.
    """
    try:
        # Append bin_dir to the system Path variable
        os.system(f'setx /M Path "%Path%;{bin_dir}"')
        print(f"Added {bin_dir} to the system Path variable")
    except Exception as e:
        print(f"Error adding {bin_dir} to the system Path variable: {e}")

def prompt_for_reboot() -> None:
    """Prompt the user to reboot the system."""
    response = input("Setup completed successfully. Would you like to reboot the system now? (y/n): ").strip().lower()
    if response == 'y':
        print("Rebooting the system...")
        os.system("shutdown /r /t 0")  # Reboot immediately
    else:
        print("You can reboot later to apply changes.")

def main() -> None:
    """Main function to run the setup."""
    if not is_windows():
        print("This script is intended for Windows operating systems only.")
        sys.exit(1)

    # Remove any old versions
    remove_old_versions(OLD_VERSIONS)

    # Create new directory structure based on current version
    main_dir, bin_dir = create_directory_structure(CURRENT_VERSION)

    # Copy all files from the software directory to the bin directory
    copy_all_files(bin_dir)

    # Add bin directory to system path
    add_bin_to_system_path(bin_dir)

    # Prompt user for reboot
    prompt_for_reboot()

if __name__ == '__main__':
    main()
