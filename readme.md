# Data AI Toolkit

A collection of tools to seamlessly share your codebase with Claude and other AI assistants. Perfect for reviewing large projects, getting code assistance across multiple files, or analyzing entire codebases with AI.

## Why We Need This

When working with AI assistants like Claude, direct folder uploads aren't supported. Trying to maintain project structure through manual uploads quickly becomes messy and error-prone.

![data-ai-toolkit-5](https://github.com/user-attachments/assets/7d51fece-3c49-42fc-a2a5-c61f0188bd8f)

## Directory Structure Analysis

First, scan your project structure to create a JSON representation:

```bash
python dir_scanner.py . ./data/this.json ./ignore.json

# Or use TOML for ignore patterns
python dir_scanner.py . ./data/this.json ./ignore.toml
```

![data-ai-toolkit-1](https://github.com/user-attachments/assets/0b6a02d4-80af-4263-ae6c-9203e49599b1)

We support both JSON and TOML formats for ignore patterns:

JSON format (`ignore.json`):
```json
{
    "files": [],
    "folders": ["__pycache__", ".git"],
    "extensions": [".pyc"]
}
```

TOML format (`ignore.toml`):
```toml
# Files to ignore
files = []

# Folders to skip during scanning
folders = [
    "__pycache__",
    ".git"
]

# File extensions to ignore
extensions = [
    ".pyc"
]

# Optional: ignore hidden files
ignore_hidden = false
```

## Claude Projects Approach

Using `claude_concat.py`, transform your project into a Claude-friendly format where all files are flattened with path information encoded in the filenames:

```bash
# Basic usage
python claude_concat.py ./data/this.json ./data/claude_ready/

# With token counting using Anthropic API (default)
python claude_concat.py ./data/this.json ./data/claude_ready/ --count-tokens

# With token counting using tiktoken (local)
python claude_concat.py ./data/this.json ./data/claude_ready/ --count-tokens --tokenizer tiktoken

# With specific model for Anthropic API token counting
python claude_concat.py ./data/this.json ./data/claude_ready/ --count-tokens --model claude-3-5-sonnet-latest
```

### Token Counting Feature
The tool includes token counting with two options:

1. Anthropic API (Default):
   - Requires Anthropic API key as environment variable (ANTHROPIC_API_KEY)
   - Uses claude-3-5-sonnet-latest model by default
   - Requires anthropic Python package: `pip install anthropic`

2. tiktoken (Local):
   - No API key required
   - Uses GPT-4o model by default
   - Requires tiktoken package: `pip install tiktoken`

Token counting output example:
```bash
$ python claude_concat.py ./data/this.json ./data/claude_ready/ --count-tokens

Using Anthropic API tokenizer with claude-3-5-sonnet-latest

Processing: src/main.py -> main.py
Tokens: 1,234

Processing: tests/test_main.py -> tests@test_main.py
Tokens: 567

Total tokens processed (Anthropic API): 1,801

# If total tokens exceed 80,000:
WARNING: Total tokens exceed 80,000. This may be too large for some models.
```

![data-ai-toolkit-2](https://github.com/user-attachments/assets/e8b1aba0-5fd4-4e4a-8a75-3fd7765583df)

Once processed, the files can be dragged directly into Claude while maintaining their structural context:

![data-ai-toolkit-3](https://github.com/user-attachments/assets/f18b589d-cce2-49a7-9c0e-799b131c9c17)

### Key Benefits
- Interactive file exploration in Claude
- Files remain individually addressable
- Path information preserved in filenames
- Great for exploratory code analysis
- Flexible token counting options
- Token count warnings for large files

## Single File Approach

While the Claude Projects approach works well in Claude, other AI platforms like Google AI Studio handle multiple files differently.

![data-ai-toolkit-6](https://github.com/user-attachments/assets/d2c0715d-4937-4a56-af03-dab58aaed82c)

Using `single_file_concat.py`, combine all files into a single document with clear START/END markers:

```bash
# Basic usage
python single_file_concat.py ./data/this.json ./data/combined.txt

# With token counting (uses tiktoken)
python single_file_concat.py ./data/this.json ./data/combined.txt --count-tokens
```

Token counting in single file mode:
- Uses tiktoken with GPT-4o encoder
- Includes tokens from file markers
- Warns when total tokens exceed 80,000
- Requires tiktoken package: `pip install tiktoken`

![data-ai-toolkit-4](https://github.com/user-attachments/assets/b66b42a0-c56b-49d7-bd44-f4519d8af06c)

We can now upload this file as context to any LLM.

![data-ai-toolkit-7](https://github.com/user-attachments/assets/0c634f15-40dc-48e6-b8e2-5631e6348c43)

### Key Benefits
- Works consistently across different AI platforms
- Clear file boundaries with START/END markers
- Excellent for maintaining file context
- Better for focused, project-wide analysis
- Built-in token counting

## How The Tools Work

**dir_scanner.py**
- Scans directories recursively
- Follows ignore patterns (JSON or TOML)
- Creates a JSON representation of your project

**claude_concat.py**
- Flattens directory structure
- Preserves path info in filenames
- Creates individual upload-ready files
- Optimized for Claude Projects
- Flexible token counting options (Anthropic API or tiktoken)
- Token count warnings for large files

**single_file_concat.py**
- Combines all files into one document
- Adds clear START/END markers
- Preserves original paths
- Works across multiple AI platforms
- Built-in token counting with tiktoken
- Includes marker tokens in count

## Best Practices

- Use an ignore file to skip unnecessary content:
  - TOML format (recommended):
    ```toml
    # Skip common non-essential files
    files = []
    folders = ["__pycache__", ".git"]
    extensions = [".pyc"]

    # Optional: ignore hidden files
    ignore_hidden = false
    ```
  - JSON format (alternative):
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
- Use token counting to stay within model context limits

## Token Counting Tips
- Enable token counting when preparing large codebases
- Use results to split files into appropriate batches
- Monitor token usage across different file types
- Pay attention to 80,000 token warnings
- Choose tokenizer based on your needs:
  - Anthropic API for exact Claude token counts
  - tiktoken for quick local counting
- Remember each tool handles token counting differently:
  - claude_concat.py: Counts individual file tokens
  - single_file_concat.py: Includes markers in count

## Advanced Usage & Examples

Looking to get the most out of Data AI Toolkit? Check out these additional guides:
- [Workflows](docs/workflows.md) - Best practices for AI-assisted development, including:
  - Voice input and keyboard workflows
  - PR-style development approach
  - GitHub integration patterns
- [Use Cases](docs/use_cases.md) - Real-world examples and insights:
  - Full-stack web applications (Flask/React)
  - Python and C++ project considerations
  - Token management strategies
  - Self-improvement case study