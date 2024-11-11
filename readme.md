# Data AI Toolkit

A collection of tools to seamlessly share your codebase with Claude and other AI assistants. Perfect for reviewing large projects, getting code assistance across multiple files, or analyzing entire codebases with AI.

## Why We Need This

When working with AI assistants like Claude, direct folder uploads aren't supported. Trying to maintain project structure through manual uploads quickly becomes messy and error-prone.

[GIF: Claude Folder Limitations]
*This GIF will demonstrate how Claude struggles with direct folder uploads, showing error messages and confused responses when trying to reference files in subdirectories. This limitation is why we need a more structured approach.*


## Directory Structure Analysis

First, scan your project structure to create a JSON representation:

```bash
python dir_scanner.py . ./data/this.json ./ignore.json
```

![data-ai-toolkit-1](https://github.com/user-attachments/assets/0b6a02d4-80af-4263-ae6c-9203e49599b1)

We use `ignore.json` to skip unnecessary files:
```json
{
    "files": [],
    "folders": ["__pycache__", ".git"],
    "extensions": [".pyc"]
}
```

## Claude Projects Approach

Using `claude_concat.py`, transform your project into a Claude-friendly format where all files are flattened with path information encoded in the filenames:

```bash
python claude_concat.py ./data/this.json ./data/claude_ready/
```

![data-ai-toolkit-2](https://github.com/user-attachments/assets/e8b1aba0-5fd4-4e4a-8a75-3fd7765583df)

Once processed, the files can be dragged directly into Claude while maintaining their structural context:

![data-ai-toolkit-3](https://github.com/user-attachments/assets/f18b589d-cce2-49a7-9c0e-799b131c9c17)

### Key Benefits
- Interactive file exploration in Claude
- Files remain individually addressable
- Path information preserved in filenames
- Great for exploratory code analysis

## Single File Approach

While the Claude Projects approach works well in Claude, other AI platforms like Google AI Studio handle multiple files differently. 

[GIF: Google AI Studio File Handling]
*This GIF will demonstrate:
1. Attempting to use the Claude-style @ files in Google AI Studio
2. Showing how this approach doesn't work well
3. Switching to the single file format
4. Successfully analyzing the codebase with proper context*

Using `single_file_concat.py`, combine all files into a single document with clear START/END markers:

```bash
python single_file_concat.py ./data/this.json ./data/combined.txt
```

![data-ai-toolkit-4](https://github.com/user-attachments/assets/b66b42a0-c56b-49d7-bd44-f4519d8af06c)

### Key Benefits
- Works consistently across different AI platforms
- Clear file boundaries with START/END markers
- Excellent for maintaining file context
- Better for focused, project-wide analysis

## How The Tools Work

**dir_scanner.py**
- Scans directories recursively
- Follows ignore patterns
- Creates a JSON representation of your project

**claude_concat.py**
- Flattens directory structure
- Preserves path info in filenames
- Creates individual upload-ready files
- Optimized for Claude Projects

**single_file_concat.py**
- Combines all files into one document
- Adds clear START/END markers
- Preserves original paths
- Works across multiple AI platforms

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
- Choose your approach based on your needs:
  - Use claude_concat.py for interactive file exploration
  - Use single_file_concat.py for cross-platform compatibility
- Test with a small subset of files first