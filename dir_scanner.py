import os
import sys
import json
from typing import Dict, Any

# Optional TOML support
try:
    import tomli
    HAS_TOML = True
except ImportError:
    HAS_TOML = False

DEFAULT_IGNORE = {
    "files": [],
    "folders": [], 
    "extensions": [],
    "ignore_hidden": False
}

def detect_file_format(filename: str) -> str:
    """
    Detect the format of the ignore file based on extension.
    Returns 'toml' or 'json' (default).
    """
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.toml':
        return 'toml'
    return 'json'

def load_ignore_file(filename: str) -> Dict[str, Any]:
    """
    Load and parse the ignore file, supporting both JSON and TOML formats.
    Returns the parsed ignore patterns or DEFAULT_IGNORE if loading fails.
    """
    if not os.path.exists(filename):
        print(f"Warning: Ignore file '{filename}' not found. Using default patterns.")
        return DEFAULT_IGNORE

    format_type = detect_file_format(filename)
    
    try:
        if format_type == 'toml':
            if not HAS_TOML:
                print("Warning: TOML file detected but tomli package not installed.")
                print("Install with: pip install tomli")
                return DEFAULT_IGNORE
                
            with open(filename, 'rb') as f:
                ignore_patterns = tomli.load(f)
        else:
            with open(filename, 'r') as f:
                ignore_patterns = json.load(f)
        
        # Validate structure
        required_keys = ['files', 'folders', 'extensions']
        for key in required_keys:
            if key not in ignore_patterns:
                print(f"Warning: Missing required key '{key}' in ignore file.")
                return DEFAULT_IGNORE
            if not isinstance(ignore_patterns[key], list):
                print(f"Warning: '{key}' must be a list in ignore file.")
                return DEFAULT_IGNORE
        
        # Ensure all entries are strings
        for key in required_keys:
            if not all(isinstance(item, str) for item in ignore_patterns[key]):
                print(f"Warning: All entries in '{key}' must be strings.")
                return DEFAULT_IGNORE
        
        # Set default for optional ignore_hidden flag
        ignore_patterns.setdefault('ignore_hidden', False)
        
        return ignore_patterns
        
    except (json.JSONDecodeError, tomli.TOMLDecodeError) as e:
        print(f"Warning: Invalid {format_type.upper()} in '{filename}': {e}")
        return DEFAULT_IGNORE
    except Exception as e:
        print(f"Warning: Error reading '{filename}': {e}")
        return DEFAULT_IGNORE

def should_ignore(name: str, ignore_patterns: Dict[str, Any]) -> bool:
    """Check if the name matches any ignore pattern."""
    if os.path.splitext(name)[1] in ignore_patterns["extensions"]:
        return True
    if name in ignore_patterns["files"]:
        return True
    if name in ignore_patterns["folders"]:
        return True
    if ignore_patterns.get("ignore_hidden", False) and name.startswith('.'):
        return True
    return False

def create_directory_lookup_table(directory: str, ignore_patterns: Dict[str, Any] = DEFAULT_IGNORE) -> Dict[str, Dict[str, list]]:
    """Create a lookup table of directories and their contents."""
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
    ignore_patterns = DEFAULT_IGNORE.copy()

    # Check if ignore patterns file is provided
    if len(sys.argv) >= 4:
        ignore_file = sys.argv[3]
        ignore_patterns = load_ignore_file(ignore_file)

    dir_dict = create_directory_lookup_table(dir, ignore_patterns)

    # Handle output
    if len(sys.argv) >= 3:  
        output_file = sys.argv[2]
        try:
            with open(output_file, 'w') as f:
                json.dump(dir_dict, f, indent=4)
            print(f"Successfully wrote directory structure to {output_file}")
        except Exception as e:
            print(f"Error writing to {output_file}: {e}")
            sys.exit(1)
    else:  
        print(json.dumps(dir_dict, indent=4))

if __name__ == "__main__":
    main()