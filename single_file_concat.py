# takes in a directory structure generated by dir_scanner.py
# and concatenates all the files in the directory into one file

import sys
import json
import os
import argparse
from typing import Optional, Tuple

FILE_HEADER = """
--- {} START ---
"""

FILE_FOOTER = """
--- {} END ---
"""

def setup_tiktoken_counter(count_tokens: bool) -> Tuple[bool, Optional[object]]:
    """Initialize tiktoken counter if enabled."""
    if not count_tokens:
        return False, None
    
    try:
        import tiktoken
        model_name = "gpt-4o"
        encoder = tiktoken.encoding_for_model(model_name)
        print(f"Using tiktoken tokenizer with {model_name} encoder")
        return True, encoder
    except ImportError:
        print("Warning: Token counting requested but tiktoken package not installed.")
        print("Install with: pip install tiktoken")
        return False, None
    except Exception as e:
        print(f"Warning: Token counting initialization failed: {e}")
        print("Token counting will be disabled.")
        return False, None

def validate_json(dir_data):
    # check if json file was made using format that dir_scanner.py uses
    # format:
    # is a dictionary with each key being the directory path (ex: C:\Users\... on windows, /Users/... on linux, etc.)
    # value of each key contains two keys: "dirs" and "files". "dirs" is a list of directories inside the base directory, 
    # and "files" is a list of files inside the base directory. 

    if not isinstance(dir_data, dict):
        print("Error: Invalid JSON format. Expected a dictionary.")
        return False
    
    for k, v in dir_data.items():
        if not os.path.isdir(k):
            print(f"Error: Invalid directory path: {k}")
            return False

        if not isinstance(v, dict):
            print(f"Error: Invalid JSON format for directory: {k}")
            return False
        
        if not isinstance(v["dirs"], list):
            print(f"Error: Invalid JSON format for directory: {k}")
            return False
        
        if not isinstance(v["files"], list):
            print(f"Error: Invalid JSON format for directory: {k}")
            return False
    
    return True

def count_file_tokens(encoder, content: str) -> Optional[int]:
    """Count tokens in file content if token counting is enabled."""
    if not encoder:
        return None
    
    try:
        num_tokens = len(encoder.encode(content))
        return num_tokens
    except Exception as e:
        print(f"Warning: Token counting failed: {e}")
        return None

def concat_dir_data(dir_data, token_counting_enabled=False):
    concat_data = ""
    total_tokens = 0
    
    # Initialize token counting if enabled
    token_counting_enabled, encoder = setup_tiktoken_counter(token_counting_enabled)
    
    for k, v in dir_data.items():
        for f in v["files"]:
            filepath = os.path.join(k, f)
            print(f"\nProcessing: {filepath}")

            try:
                # Read file content
                with open(filepath, "r") as f:
                    file_content = f.read()
                    
                    # Format the complete content including headers and footers
                    formatted_content = (
                        f"{FILE_HEADER.format(filepath)}\n"
                        f"{file_content}\n"
                        f"{FILE_FOOTER.format(filepath)}\n"
                    )
                    
                    # Add to concatenated data
                    concat_data += formatted_content
                    
                    # Count tokens if enabled for the complete formatted content
                    if token_counting_enabled:
                        try:
                            token_count = count_file_tokens(encoder, formatted_content)
                            if token_count is not None:
                                total_tokens += token_count
                                print(f"Tokens: {token_count:,}")
                        except Exception as e:
                            print(f"Warning: Token counting failed for {filepath}: {e}")
                            
            except Exception as e:
                print(f"Error: {e}")
                print(f"skipping file {filepath}")
                pass
    
    if token_counting_enabled and total_tokens > 0:
        print(f"\nTotal tokens processed: {total_tokens:,}")
        
        if total_tokens > 80000:
            print("\nWARNING: Total tokens exceed 80,000. This may be too large for some models.")
    
    return concat_data

def main():
    parser = argparse.ArgumentParser(description='Concatenate directory files into a single file.')
    parser.add_argument('json_file', help='Input JSON file containing directory structure')
    parser.add_argument('output_file', nargs='?', help='Output file (optional)')
    parser.add_argument('-c', '--count-tokens', action='store_true', help='Enable token counting using tiktoken')
    parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation prompts')
    
    args = parser.parse_args()

    # Check if output file exists and handle confirmation
    if args.output_file and os.path.exists(args.output_file):
        if not args.yes:
            confirm = input(f"Output file '{args.output_file}' already exists. Overwrite? (y/N): ")
            if confirm.lower() != 'y':
                print("Operation cancelled.")
                sys.exit(0)

    with open(args.json_file, 'r') as json_file:
        dir_data = json.load(json_file)
        if not validate_json(dir_data):
            sys.exit(1)
        
        print("JSON is valid. Concatenating...")
        concat_data = concat_dir_data(dir_data, args.count_tokens)

    if args.output_file:
        with open(args.output_file, 'w') as output_file:
            output_file.write(concat_data)
            print("\nSuccessfully wrote to file.")
            sys.exit(0)
    else:
        print(concat_data)

if __name__ == "__main__":
    main()