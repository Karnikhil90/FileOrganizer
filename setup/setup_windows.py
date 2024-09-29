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
    """Move the FO.exe file to the bin directory."""
    source_path = 'FO.exe'  # Ensure this script is in the same directory as FO.exe
    destination_path = os.path.join(bin_dir, 'FO.exe')

    try:
        shutil.move(source_path, destination_path)
        print(f"Moved FO.exe to {destination_path}")
    except FileNotFoundError:
        print("FO.exe not found. Please ensure it is in the same directory as this script.")
    except Exception as e:
        print(f"Error moving FO.exe: {e}")

def set_global_environment_variable():
    """Set a global environment variable for the application."""
    variable_name = 'FILE_ORGANIZER_PATH'
    variable_value = r'C:\FileOrganizer_v2\bin'

    try:
        os.environ[variable_name] = variable_value
        # Use 'setx' command to set the variable globally
        os.system(f'setx {variable_name} "{variable_value}"')
        print(f"Set global environment variable: {variable_name} = {variable_value}")
    except Exception as e:
        print(f"Error setting environment variable: {e}")

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
    set_global_environment_variable()
    prompt_for_reboot()

if __name__ == "__main__":
    main()
