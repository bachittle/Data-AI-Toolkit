# Data AI Toolkit

A collection of Python scripts designed to help prepare and organize files for AI interactions. Makes it easy to share multiple files and directory structures with AI systems like Claude.

## Scripts

### dir_scanner.py
Scans a directory and creates a JSON file mapping its structure.
```bash
python dir_scanner.py <directory_path> [output_file] [ignore_patterns_file]
```

### single_file_concat.py
Combines all scanned files into one text file with START/END markers for each file.
```bash
python single_file_concat.py <json_file> [output_file]
```

### claude_concat.py
Flattens files into a single directory, using @ symbols in filenames to preserve path info.
```bash
python claude_concat.py <json_file> <output_directory>
```

## Ignore Patterns
Create a JSON file to specify what to ignore:
```json
{
    "files": [],
    "folders": ["__pycache__"],
    "extensions": [".pyc"]
}
```

## Basic Usage
1. Scan your directory to create a JSON file mapping its structure:
  - Scan everything: `python dir_scanner.py ./my_project ./data/output.json`
  - Scan and ignore what is in ignore file: `python dir_scanner.py ./my_project ./data/output.json ./ignore.json`
2. Then either:
  - Combine into one file: `python single_file_concat.py ./data/output.json ./data/combined.txt`
  - Or prepare for Claude: `python claude_concat.py ./data/output.json ./data/prepared_files/`

**Note**: The `data/` directory is git-ignored. This is the recommended place to store your JSON files and output.