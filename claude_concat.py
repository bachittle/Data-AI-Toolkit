# claude_concat.py
# ---
# takes in a directory structure generated by dir_scanner.py
# and concatenates all the files into one folder with transformed filenames

import sys
import json
import os
import argparse
from typing import Tuple, List, Optional, Any

def transform_path(parent_dir: str, filepath: str) -> str:
    # If it's the root directory file, just return the filename
    if '/' not in filepath and '\\' not in filepath:
        return filepath
        
    # Replace .\\ with nothing and \\ with \@
    filepath = filepath.replace('.\\', '')
    filepath = filepath.replace('\\', '@')
        
    # Otherwise, replace slashes with @ but skip the parent dir
    return filepath.replace('/', '@')

def validate_json(dir_data: dict) -> bool:
    if not isinstance(dir_data, dict):
        print("Error: Invalid JSON format. Expected a dictionary.")
        return False
    
    for k, v in dir_data.items():
        if not isinstance(v, dict):
            print(f"Error: Invalid JSON format for directory: {k}")
            return False
        
        if not ("dirs" in v and "files" in v):
            print(f"Error: Missing 'dirs' or 'files' keys in directory: {k}")
            return False
    
    return True

def is_visual_file(filepath: str) -> bool:
    visual_extensions = ('.png', '.jpg', '.jpeg', '.pdf')
    return filepath.lower().endswith(visual_extensions)

def setup_anthropic_counter(count_tokens: bool, model_name: str) -> Tuple[bool, Optional[Any]]:
    """Initialize Anthropic token counting if enabled."""
    if not count_tokens:
        return False, None
    
    try:
        from anthropic import Anthropic
    except ImportError:
        print("Warning: Anthropic token counting requested but anthropic package not installed.")
        print("Install with: pip install anthropic")
        return False, None
    
    try:
        client = Anthropic()
        # Test the client with a simple count
        client.beta.messages.count_tokens(
            model=model_name,
            messages=[{"role": "user", "content": "test"}]
        )
        print(f"Using Anthropic API tokenizer with {model_name}")
        return True, client
    except Exception as e:
        print(f"Warning: Anthropic token counting initialization failed: {e}")
        print("Token counting will be disabled.")
        return False, None

def setup_tiktoken_counter(count_tokens: bool) -> Tuple[bool, Optional[Any]]:
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

def count_anthropic_tokens(client: Optional[Any], model_name: str, content: str) -> Optional[int]:
    """Count tokens using Anthropic API if enabled."""
    if not client:
        return None
    
    try:
        count = client.beta.messages.count_tokens(
            model=model_name,
            messages=[{"role": "user", "content": content}]
        )
        return count.input_tokens
    except Exception as e:
        print(f"Warning: Token counting failed: {e}")
        return None

def count_tiktoken_tokens(encoder: Optional[Any], content: str) -> Optional[int]:
    """Count tokens using tiktoken if enabled."""
    if not encoder:
        return None
    
    try:
        num_tokens = len(encoder.encode(content))
        return num_tokens
    except Exception as e:
        print(f"Warning: Token counting failed: {e}")
        return None

def setup_token_counter(count_tokens: bool, tokenizer: str, model_name: str = None) -> Tuple[bool, Optional[Any], str]:
    """Setup the appropriate token counter based on tokenizer choice."""
    if not count_tokens:
        return False, None, tokenizer
    
    if tokenizer == 'anthropic':
        is_enabled, counter = setup_anthropic_counter(count_tokens, model_name)
        if not is_enabled and count_tokens:
            print("Falling back to tiktoken...")
            is_enabled, counter = setup_tiktoken_counter(count_tokens)
            if is_enabled:
                tokenizer = 'tiktoken'
    else:  # tiktoken
        is_enabled, counter = setup_tiktoken_counter(count_tokens)
        
    return is_enabled, counter, tokenizer

def count_file_tokens(tokenizer: str, counter: Any, model_name: str, content: str) -> Optional[int]:
    """Count tokens using the selected tokenizer."""
    if tokenizer == 'anthropic':
        return count_anthropic_tokens(counter, model_name, content)
    else:  # tiktoken
        return count_tiktoken_tokens(counter, content)

def concat_dir_data(dir_data: dict, output_dir: str, count_tokens: bool = False, 
                   tokenizer: str = 'anthropic',
                   model_name: str = "claude-3-5-sonnet-latest") -> Tuple[List[str], List[str]]:
    created_files = []
    visual_files = []
    total_tokens = 0
    
    # Initialize token counting
    token_counting_enabled, counter, active_tokenizer = setup_token_counter(
        count_tokens, tokenizer, model_name
    )
    
    visual_dir = None
    parent_dir = next(iter(dir_data.keys()))
    
    for base_dir, content in dir_data.items():
        for filepath in content["files"]:
            full_path = os.path.join(base_dir, filepath)
            relative_path = os.path.relpath(full_path, parent_dir)
            transformed_name = transform_path(parent_dir, relative_path)
            
            if is_visual_file(transformed_name):
                if visual_dir is None:
                    visual_dir = os.path.join(output_dir, "visual")
                    os.makedirs(visual_dir, exist_ok=True)
                output_path = os.path.join(visual_dir, transformed_name)
                visual_files.append(transformed_name)
            else:
                output_path = os.path.join(output_dir, transformed_name)
                created_files.append(transformed_name)
            
            print(f"\nProcessing: {full_path} -> {transformed_name}")
            
            try:
                # Read file content
                with open(full_path, "rb") as f:
                    file_content = f.read()
                
                # Count tokens if enabled and not a visual file
                if token_counting_enabled and not is_visual_file(transformed_name):
                    try:
                        # Decode content for token counting
                        decoded_content = file_content.decode('utf-8')
                        token_count = count_file_tokens(active_tokenizer, counter, model_name, decoded_content)
                        if token_count is not None:
                            total_tokens += token_count
                            print(f"Tokens: {token_count:,}")
                    except UnicodeDecodeError:
                        print("Warning: File appears to be binary. Skipping token count.")
                
                # Write the file
                with open(output_path, "wb") as out_f:
                    out_f.write(file_content)
                    
            except Exception as e:
                print(f"Error processing {full_path}: {e}")
                continue
    
    if token_counting_enabled and total_tokens > 0:
        tokenizer_name = "Anthropic API" if active_tokenizer == 'anthropic' else "tiktoken"
        print(f"\nTotal tokens processed ({tokenizer_name}): {total_tokens:,}")
        
        if total_tokens > 80000:
            print("\nWARNING: Total tokens exceed 80,000. This may be too large for some models.")
    
    return created_files, visual_files

def main():
    parser = argparse.ArgumentParser(description='Process directory structure into Claude-friendly format.')
    parser.add_argument('json_file', help='Input JSON file containing directory structure')
    parser.add_argument('output_dir', help='Output directory for processed files')
    parser.add_argument('--count-tokens', action='store_true', help='Enable token counting')
    parser.add_argument('--model', default="claude-3-5-sonnet-latest", 
                      help='Model name for token counting (default: claude-3-5-sonnet-latest)')
    parser.add_argument('--tokenizer', choices=['anthropic', 'tiktoken'], default='anthropic',
                      help='Choose tokenizer for counting (default: anthropic)')
    
    args = parser.parse_args()

    # Confirm output directory with user
    if os.path.exists(args.output_dir):
        confirm = input(f"Output directory '{args.output_dir}' already exists. Delete and continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
        
        # Remove existing output directory
        try:
            import shutil
            shutil.rmtree(args.output_dir)
        except Exception as e:
            print(f"Error removing directory {args.output_dir}: {e}")
            sys.exit(1)

    # Create fresh output directory
    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.json_file, 'r') as json_file:
        dir_data = json.load(json_file)
        if not validate_json(dir_data):
            sys.exit(1)
        
        print("JSON is valid. Processing files...")
        created_files, visual_files = concat_dir_data(
            dir_data, 
            args.output_dir,
            count_tokens=args.count_tokens,
            tokenizer=args.tokenizer,
            model_name=args.model
        )
        
        # don't print these for now, just look in the folder to see what was made
        # print("\nCreated files:")
        # for f in created_files:
        #     print(f"- {f}")
            
        # if visual_files:
        #     print("\nVisual files (in 'visual' subdirectory):")
        #     for f in visual_files:
        #         print(f"- {f}")

if __name__ == "__main__":
    main()