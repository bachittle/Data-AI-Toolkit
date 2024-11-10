# Data AI Toolkit

A collection of tools to seamlessly share your codebase with Claude. Perfect for reviewing large projects, getting code assistance across multiple files, or analyzing entire codebases with AI.

## Let's Use It On Itself!

We'll demonstrate how to use this toolkit by analyzing its own codebase. Follow along to see how it works.

### 1. Directory Scanning

First, let's scan the toolkit's directory structure:

```bash
python dir_scanner.py . ./data/this.json ./ignore.json
```

![data-ai-toolkit-1](https://github.com/user-attachments/assets/0b6a02d4-80af-4263-ae6c-9203e49599b1)

Note how we're using `ignore.json` to skip unnecessary files:
```json
{
    "files": [],
    "folders": ["__pycache__", ".git"],
    "extensions": [".pyc"]
}
```

### 2. Preparing for Claude

Now let's convert our scanned structure into Claude-friendly format:

```bash
python claude_concat.py ./data/this.json ./data/claude_ready/
```

![data-ai-toolkit-2](https://github.com/user-attachments/assets/e8b1aba0-5fd4-4e4a-8a75-3fd7765583df)

### 3. Uploading to Claude

![data-ai-toolkit-3](https://github.com/user-attachments/assets/f18b589d-cce2-49a7-9c0e-799b131c9c17)

Now you can ask Claude about any aspect of the toolkit's codebase! Try questions like:
- "How does dir_scanner.py handle ignore patterns?"
- "What's the relationship between the three main Python scripts?"
- "Can you suggest improvements to the error handling?"

### Alternative: Single File Output

If you prefer having everything in one file:

```bash
python single_file_concat.py ./data/this.json ./data/combined.txt
```

![data-ai-toolkit-4](https://github.com/user-attachments/assets/b66b42a0-c56b-49d7-bd44-f4519d8af06c)


## How It Works

1. `dir_scanner.py`: Maps your project structure
   - Scans directories recursively
   - Follows ignore patterns (like `.gitignore`)
   - Creates a JSON representation

2. `claude_concat.py`: Prepares for Claude Projects
   - Flattens directory structure
   - Preserves path info in filenames
   - Creates upload-ready files

3. `single_file_concat.py`: (Alternative approach)
   - Combines all files into one
   - Adds clear START/END markers
   - Preserves original paths

## Best Practices

- Always use an `ignore.json` file:
  ```json
  {
      "files": [],
      "folders": ["__pycache__", ".git"],
      "extensions": [".pyc"]
  }
  ```
- Keep processed files in `data/` (it's gitignored)
- Review files before upload to protect sensitive data
- For large projects, upload in logical segments
