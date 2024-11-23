import os
from shutil import move
import argparse

# Global file types dictionary
FILE_TYPES = {
    "images": ["png", "jpg", "jpeg", "gif", "bmp", "svg", "tiff", "ico" ,"webp"],
    "music": ["mp3", "wav", "flac", "aac", "ogg", "m4a"],
    "videos": ["mp4", "mkv", "mov", "avi", "flv", "wmv", "webm"],
    "documents": ["txt", "pdf", "doc", "docx", "odt", "rtf", "md", "epub"],
    "archives": ["zip", "rar", "tar", "gz", "7z", "bz2"],
    "executables": ["exe", "bat", "sh", "msi", "bin", "apk"],
    "spreadsheets": ["xls", "xlsx", "csv", "ods"],
    "presentations": ["ppt", "pptx", "odp"],
    "code": ["py", "js", "html", "css", "java", "c", "cpp", "h", "rb", "php", "go", "ts"],
    "databases": ["sql", "db", "sqlite", "mdb", "accdb"],
    "fonts": ["ttf", "otf", "woff", "woff2"],
    "scripts": ["js", "php","sh", "bat", "rb"],
    "others": ["iso", "dmg", "torrent"]
}
CURRENT_VERSION :str = 'FileOrganizer v2.2'

VERSION_INFO = """
        ===========================
             {0}
        Developed by Nikhil Karmakar
        ===========================

FileOrganizer is a command-line tool designed to help you manage and organize your files efficiently. 
Whether you need to sort files by type, move them to different directories, or clean up your file system, 
FileOrganizer provides a simple yet powerful set of commands to streamline these tasks.
""".format(CURRENT_VERSION)

class FileOrganised:
    def __init__(self, file_types=None):
        """
        Initializes the class with the provided file types or the default ones.
        """
        self.file_types = file_types if file_types is not None else FILE_TYPES

    def organize_files(self, directory: str = './', selected_extensions: list = None, all_extensions: bool = False):
        """
        Organizes files from the given directory into specific folders based on the file extensions.
        """
        for filename in os.listdir(directory):
            # Get the file extension (ignore hidden files starting with '.')
            if filename.startswith('.'):
                continue
            file_extension = filename.split('.')[-1].lower()

            if all_extensions:
                # Create a folder for each unique file extension
                self.move_file_to_folder(filename, file_extension, directory)
            elif selected_extensions:
                # If specific extensions are provided, only organize those
                if file_extension in selected_extensions:
                    self.move_file_to_folder(filename, file_extension, directory)
            else:
                # Default handling based on the predefined file types
                for folder, extensions in self.file_types.items():
                    if file_extension in extensions:
                        self.move_file_to_folder(filename, folder, directory)
                        break

    def move_file_to_folder(self, filename, folder, directory):
        """
        Move the file to the appropriate folder, creating the folder if necessary.
        """
        folder_path = os.path.join(directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        source = os.path.join(directory, filename)
        destination = os.path.join(folder_path, filename)

        try:
            move(source, destination)
            print(f"Moved {filename} to {folder}/")
        except Exception as e:
            print(f"Error moving {filename}: {e}")


"""
The function `map_directory_to_extensions` converts a string input into a dictionary, 
mapping a directory name to a list of file extensions.

* in simple , From str to dictionary. key is the directory's name and value is file types
Example:
    user_input: "mydoc:txt,pdf" 
    
    Output: {'mydoc': ['txt', 'pdf']}
"""


def map_directory_to_extensions(user_input : str) -> dict[str:list[str]] | bool:
    if ':' not in user_input : return False
    directory, file_types = user_input.split(':')
    return {directory: file_types.split(',')}
print(map_directory_to_extensions("mydoc:txt,pdf"))


# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description=f"{CURRENT_VERSION}")

    # Location option
    parser.add_argument('-l', '--location', type=str, default='./', help="Specify directory to organize")
    # Selected extensions option
    parser.add_argument('-s', '--select', type=str, help="Specify extensions to move only those files, e.g., -s 'png,jpg'")
    # All extensions option to create folders for each file extension
    parser.add_argument('-a', '--all', action='store_true', help="Create a new directory for each file extension")
   # Custom directory-extension mapping input
    parser.add_argument('-m', '--map', type=str, help="Custom directory to extension mapping (e.g., 'images:jpg,png,gif')")
    # Version option
    parser.add_argument('-v', '--version', action='store_true', help="Show version information and exit")

    args = parser.parse_args()

    # Parse selected extensions if provided
    selected_extensions = []
    if args.select:
        selected_extensions = [ext.strip() for ext in args.select.split(',')]

    # If custom directory-extension mapping is provided, map it
    if args.map:
        try:        
            mapping = map_directory_to_extensions(args.map)
        except:
            print("ErrorType : Invalid Syntax for mapping input.")
        if mapping:
            # Create the FileOrganised object with the mapped extensions
            organizer = FileOrganised(mapping)
            organizer.organize_files(args.location, selected_extensions, args.all)
        else:
            print("ErrorType : Invalid Syntax for mapping input.")
    else:
        # If no mapping is provided, use the default file types
        organizer = FileOrganised(FILE_TYPES)
        organizer.organize_files(args.location, selected_extensions, args.all)

try:
    main()
except Exception as e:
    print(f"Error: {e}")
