import os
import sys
import json

def create_directory_lookup_table(directory):
    # gets every file and folder in the directory and creates a lookup table
    directory_dict = {}
    for root, dirs, files in os.walk(directory):
        print(f"Processing directory: {root}")

        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]
        directory_dict[root] = {'dirs': dirs, 'files': files}
    return directory_dict

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <directory_path> [output_file]")
        return

    dir = sys.argv[1]

    if not os.path.isdir(dir):
        print(f"{dir} is not a directory.")
        return

    dir_dict = create_directory_lookup_table(dir)

    if len(sys.argv) == 3:
        output_file = sys.argv[2]
        with open(output_file, 'w') as f:
            json.dump(dir_dict, f, indent=4)
    else:
        print(json.dumps(dir_dict, indent=4))

if __name__ == "__main__":
    main()
