import os , sys
from shutil import move
import argparse ,csv
from FileAccess import FileAccess
from datetime import datetime

# Global file types dictionary as falback
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
======================================================
             {0}
        Developed by Nikhil Karmakar
======================================================

FileOrganizer is a command-line tool designed to help you manage and organize your files efficiently. 
Whether you need to sort files by type, move them to different directories, or clean up your file system, 
FileOrganizer provides a simple yet powerful set of commands to streamline these tasks.
""".format(CURRENT_VERSION)

fallback_file_path_of_FileType = "FILE_TYPES.json"
config_file_path= "config.json"


file = FileAccess(config_file_path,True)
config_:dict = file.read_json()[0]
# print(config_)
config_filepath = config_.get("filepath",{})
file_path_of_FileType = config_filepath.get("DEFAULT_FILE_TYPES", fallback_file_path_of_FileType)


class FileOrganised:
    def __init__(self, file_types: str =None):
        self.file_types = file_types if file_types is not None else FILE_TYPES
    def setFileType(self,file_type:dict[str, list[str]]):
        self.file_types = file_type

    def getFileType(self)-> dict[str, list[str]]:
        return self.file_types
    
    def add_value_FileType(self, new_value: dict[str, list[str]]) -> bool:
        added = False

        for category, extensions in new_value.items():
            if category in self.file_type:
                for ext in extensions:
                    if ext not in self.file_type[category]:
                        self.file_type[category].append(ext)
                        added = True
            else:
                self.file_type[category] = extensions.copy()
                added = True

        return added



    def organize_files(self, directory: str = './', selected_extensions: list = None, all_extensions: bool = False):
        """
        Organizes files from the given directory into specific folders based on the file extensions.
        """

        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)

            # Skip hidden files and directories
            if filename.startswith('.') or os.path.isdir(full_path):
                continue

            # Safely extract file extension
            file_extension = os.path.splitext(filename)[1][1:].lower()  # Removes the dot

            if all_extensions:
                # Folder name = extension
                self.move_file_to_folder(filename, file_extension, directory)
            elif selected_extensions:
                if file_extension in selected_extensions:
                    self.move_file_to_folder(filename, file_extension, directory)
            else:
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

# utility funtion 
def map_directory_to_extensions(user_input : str) -> dict[str:list[str]] | bool:
    if ':' not in user_input : return False
    directory, file_types = user_input.split(':')
    return {directory: file_types.split(',')}


# It cheaks that @param file_type:dict is not emplty
def cheak_FileType_json(file_type:dict={})-> bool:
    size_of_keys = len(file_type.keys())
    if size_of_keys > 0 and file_type: 
        return True
    return False
    

def log_command_entry(command: str):
    # print('log_command_entry')
    log_file = config_filepath.get("MAPPING_HISTORY", "mapping_log.csv")
    
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    log_exists = os.path.isfile(log_file)

    with open(log_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not log_exists:
            writer.writerow(['time', 'command'])
        writer.writerow([datetime.now().isoformat(), command])


# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description=f"{CURRENT_VERSION}")

    parser.add_argument('-l', '--location', type=str, default='./', help="Specify directory to organize")
    parser.add_argument('-s', '--select', type=str, help="Move only these extensions (e.g. -s 'png,jpg')")
    parser.add_argument('-a', '--all', action='store_true', help="Create folder for each file extension")
    parser.add_argument('-v', '--version', action='store_true', help="Show version info and exit")
    parser.add_argument('-t', '--add-type', type=str, help="Add new mappings to user file types (e.g. 'my_space:exe,json,png')")
    parser.add_argument('-m', '--map', type=str, help="Custom mapping (e.g. 'images:jpg,png')")
    parser.add_argument('-sk', '--show-keys', action='store_true', help="Show all category keys currently defined in FILE_TYPES")
    parser.add_argument('--reset-types', action='store_true', help='Reset all user-added file type mappings (clears USER_MODIFIED_FILE_TYPES.json)')
    parser.add_argument('--show-log', action='store_true', help='Display the CLI command log history from mapping_log.csv')

    args = parser.parse_args()
    selected_extensions = [ext.strip() for ext in args.select.split(',')] if args.select else []

    # Load file types from DEFAULT and USER files
    default_path = config_filepath.get("DEFAULT_FILE_TYPES", fallback_file_path_of_FileType)
    user_path = config_filepath.get("USER_MODIFIED_FILE_TYPES", "USER_MODIFIED_FILE_TYPES.json")
    default_types:dict = FileAccess(default_path, True).read_json()
    user_types:dict = FileAccess(user_path, True).read_json()
    user_types = user_types if isinstance(user_types, dict) else {}

    # Merge defaults + user-added types
    merged_types = default_types.copy()
    if user_types:
        for k, v in user_types.items():
            merged_types.setdefault(k, [])
            for ext in v:
                if ext not in merged_types[k]:
                    merged_types[k].append(ext)

    organizer = FileOrganised(merged_types)

    if args.version:
        print(VERSION_INFO)
    elif args.show_keys:
        print("Categories:", list(merged_types.keys()))
        print(f"Total: {len(merged_types)}")
    elif args.add_type:
        try:
            # Parse input like: 'images:webp,avif'
            new_map = map_directory_to_extensions(args.add_type)

            if not new_map:
                raise ValueError("Invalid format. Use 'category:ext1,ext2'")

            user_file = FileAccess(user_path, True)
            current = user_file.read_json()
            current = current if isinstance(current, dict) else {}

            for k, v in new_map.items():
                current.setdefault(k, [])
                for ext in v:
                    if ext not in current[k]:
                        current[k].append(ext)

            user_file.write_json(current)
            print("✅ New types added to user file.")
        except Exception as e:
            print(f"❌ Invalid --add-type input: {e}")
    elif args.map:
        try:
            mapping = map_directory_to_extensions(args.map)
            FileOrganised(mapping).organize_files(args.location, selected_extensions, args.all)
        except:
            print("❌ Error parsing mapping input.")

    # --reset-types
    elif args.reset_types:
        user_file = FileAccess(user_path, True)
        user_file.write_json({})
        print("🗑️  Cleared all user-added FILE_TYPE mappings.")

    # --show-log
    elif args.show_log:
        log_file = config_filepath.get("MAPPING_HISTORY", "mapping_log.csv")
        if not os.path.exists(log_file):
            print("📂 No log file found.")
        else:
            with open(log_file, mode='r', encoding='utf-8') as csvfile:
                print("\n📝 Command Log History:")
                for line in csvfile:
                    print("  " + line.strip())

    else:
        organizer.organize_files(args.location, selected_extensions, args.all)

    # Log the full command string
    log_command_entry(" ".join(sys.argv))

try:
    main()
except Exception as e:
    print(f"Error(main): {e}")

