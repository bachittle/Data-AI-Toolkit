import os
import sys
import json

DEFAULT_IGNORE = {
    "files": [],
    "folders": [], 
    "extensions": []
}

def should_ignore(name, ignore_patterns):
    # Check if the name matches any ignore pattern
    if os.path.splitext(name)[1] in ignore_patterns["extensions"]:
        return True
    if name in ignore_patterns["files"]:
        return True
    if name in ignore_patterns["folders"]:
        return True
    if ignore_patterns.get("ignore_hidden", False) and name.startswith('.'):
        return True
    return False

def create_directory_lookup_table(directory, ignore_patterns=DEFAULT_IGNORE):
    directory_dict = {}
    for root, dirs, files in os.walk(directory):
        print(f"Processing directory: {root}")

        # Filter out hidden files/folders and ignored patterns
        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]
        files = [f for f in files if not should_ignore(f, ignore_patterns)]
        
        directory_dict[root] = {'dirs': dirs, 'files': files}
    return directory_dict

def main():
    if not (2 <= len(sys.argv) <= 4):
        print("Usage: python script.py <directory_path> [output_file] [ignore_patterns_file]")
        return

    dir = sys.argv[1]
    if not os.path.isdir(dir):
        print(f"{dir} is not a directory.")
        return

    # Initialize empty ignore patterns (ignore nothing by default)
    ignore_patterns = {
        "files": [],
        "folders": [],
        "extensions": []
    }

    # Check if ignore patterns file is provided
    if len(sys.argv) >= 4:
        ignore_file = sys.argv[3]
        try:
            with open(ignore_file, 'r') as f:
                ignore_patterns = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Ignore patterns file '{ignore_file}' not found. Using empty patterns.")
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in '{ignore_file}'. Using empty patterns.")

    dir_dict = create_directory_lookup_table(dir, ignore_patterns)

    # Handle output
    if len(sys.argv) >= 3:  
        output_file = sys.argv[2]
        with open(output_file, 'w') as f:
            json.dump(dir_dict, f, indent=4)
    else:  
        print(json.dumps(dir_dict, indent=4))

if __name__ == "__main__":
    main()
