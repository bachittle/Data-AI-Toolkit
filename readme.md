# Data AI Toolkit

A collection of tools to seamlessly share your codebase with Claude. Perfect for reviewing large projects, getting code assistance across multiple files, or analyzing entire codebases with AI.

## Let's Use It On Itself!

We'll demonstrate how to use this toolkit by analyzing its own codebase. Follow along to see how it works.

### 1. Directory Scanning

First, let's scan the toolkit's directory structure:

```bash
python dir_scanner.py . ./data/this.json ./ignore.json
```

[GIF 1: Self-Scanning Process]
*The GIF will show:
1. Running the command above
2. The resulting this.json being created in the data directory
3. Quick peek at the JSON showing the structure:*
```json
{
    ".": {
        "dirs": ["data", "docs"],
        "files": [
            ".gitignore",
            "claude_concat.py",
            "dir_scanner.py",
            "ignore.json",
            "readme.md",
            "single_file_concat.py"
        ]
    },
    ...
}
```

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

[GIF 2: Creating Claude-Ready Files]
*The GIF will show:
1. Running the command above
2. The claude_ready directory being created
3. The resulting files with transformed names:*
```
claude_ready/
  ├─ .gitignore
  ├─ claude_concat.py
  ├─ dir_scanner.py
  ├─ ignore.json
  ├─ readme.md
  ├─ single_file_concat.py
  ├─ data@.gitignore
  ├─ docs@readme.md
```

### 3. Uploading to Claude

[GIF 3: Claude Projects Upload]
*The GIF will show:
1. Opening Claude Projects
2. Dragging all files from claude_ready/
3. Claude acknowledging receipt of the files, showing them in the sidebar*

Now you can ask Claude about any aspect of the toolkit's codebase! Try questions like:
- "How does dir_scanner.py handle ignore patterns?"
- "What's the relationship between the three main Python scripts?"
- "Can you suggest improvements to the error handling?"

### Alternative: Single File Output

If you prefer having everything in one file:

```bash
python single_file_concat.py ./data/this.json ./data/combined.txt
```

[GIF 4: Creating Combined Output]
*The GIF will show:
1. Running the command above
2. The resulting combined.txt with START/END markers:*
```
--- dir_scanner.py START ---
import os
import sys
import json
...
--- dir_scanner.py END ---

--- claude_concat.py START ---
...
```

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
