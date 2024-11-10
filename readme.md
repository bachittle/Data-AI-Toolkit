# Data AI Toolkit

A collection of Python scripts designed to help prepare and organize files for AI interactions. Makes it easy to share multiple files and directory structures with AI systems like Claude.

For detailed information about the motivation and design behind this toolkit, see [docs/index.md](docs/index.md).

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
Creates a Claude-friendly version of your files by flattening them into a single directory with path information preserved in filenames.
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

## Quick Start
1. Scan your directory:
```bash
python dir_scanner.py ./my_project ./data/output.json ./ignore.json
```

2. Prepare for Claude:
```bash
python claude_concat.py ./data/output.json ./data/claude_ready/
```

3. Drag all files from `claude_ready/` into Claude Projects.

## Documentation

- [Introduction and Motivation](docs/index.md) - Learn about why this toolkit exists and how it works
- More documentation coming soon

**Note**: The `data/` directory is git-ignored. This is the recommended place to store your JSON files and processed outputs.