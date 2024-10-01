import os
import shutil
import sys
import platform

def is_windows():
    """Check if the current operating system is Windows."""
    return platform.system() == 'Windows'

def create_directory_structure():
    """Create the main directory and bin directory for the application."""
    main_dir = r'C:\FileOrganizer_v2'
    bin_dir = os.path.join(main_dir, 'bin')

    # Create the main directory if it doesn't exist
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
        print(f"Created directory: {main_dir}")

    # Create the bin directory if it doesn't exist
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
        print(f"Created directory: {bin_dir}")

    return main_dir, bin_dir  # Return both directories

def move_executable(bin_dir):
    """Move the FO.exe file from the ./app/ directory to the bin directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory where the script is located
    source_path = os.path.join(current_dir, 'app', 'FO.exe')  # Locate FO.exe in ./app/ folder
    destination_path = os.path.join(bin_dir, 'FO.exe')

    try:
        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"Moved FO.exe to {destination_path}")
        else:
            print(f"FO.exe not found at {source_path}. Please ensure it is in the 'app' directory.")
    except Exception as e:
        print(f"Error moving FO.exe: {e}")

def add_bin_to_system_path(bin_dir):
    """Add the bin directory to the system's Path variable permanently."""
    try:
        # Use 'setx' to append bin_dir to the system Path variable
        os.system(f'setx /M Path "%Path%;{bin_dir}"')  # /M ensures it's for the system, not user
        print(f"Added {bin_dir} to the system Path variable")
    except Exception as e:
        print(f"Error adding {bin_dir} to the system Path variable: {e}")

def prompt_for_reboot():
    """Prompt the user to reboot the system."""
    response = input("Setup completed successfully. Would you like to reboot the system now? (y/n): ").strip().lower()
    if response == 'y':
        print("Rebooting the system...")
        os.system("shutdown /r /t 0")  # Reboot immediately
    else:
        print("You can reboot later to apply changes.")

def main():
    """Main function to run the setup."""
    if not is_windows():
        print("This script is intended for Windows operating systems only.")
        sys.exit(1)

    main_dir, bin_dir = create_directory_structure()  # Capture both return values
    move_executable(bin_dir)
    add_bin_to_system_path(bin_dir)  # Add the bin directory to system Path
    prompt_for_reboot()

main()