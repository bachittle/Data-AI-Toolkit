# Data AI Toolkit

A collection of tools to seamlessly share your codebase with Claude and other AI assistants. Perfect for reviewing large projects, getting code assistance across multiple files, or analyzing entire codebases with AI.

## Why We Need This

When working with AI assistants like Claude, direct folder uploads aren't supported. Trying to maintain project structure through manual uploads quickly becomes messy and error-prone.

![data-ai-toolkit-5](https://github.com/user-attachments/assets/7d51fece-3c49-42fc-a2a5-c61f0188bd8f)

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
# Basic usage
python claude_concat.py ./data/this.json ./data/claude_ready/

# With token counting enabled
python claude_concat.py ./data/this.json ./data/claude_ready/ --count-tokens

# With specific model for token counting
python claude_concat.py ./data/this.json ./data/claude_ready/ --count-tokens --model claude-3-opus-20240229
```

### Token Counting Feature
The tool now includes an optional token counting feature that helps you understand the token usage of your files:

```bash
$ python claude_concat.py ./data/this.json ./data/claude_ready/ --count-tokens

Processing: src/main.py -> main.py
Tokens: 1,234

Processing: tests/test_main.py -> tests@test_main.py
Tokens: 567

Total tokens processed: 1,801
```

Requirements for token counting:
- Anthropic API key set as environment variable (ANTHROPIC_API_KEY)
- Anthropic Python package installed: `pip install anthropic`

Token counting options:
- `--count-tokens`: Enable token counting
- `--model`: Specify Claude model for counting (default: claude-3-sonnet-20240229)

Note: The tool works normally without token counting if these requirements aren't met.

![data-ai-toolkit-2](https://github.com/user-attachments/assets/e8b1aba0-5fd4-4e4a-8a75-3fd7765583df)

Once processed, the files can be dragged directly into Claude while maintaining their structural context:

![data-ai-toolkit-3](https://github.com/user-attachments/assets/f18b589d-cce2-49a7-9c0e-799b131c9c17)

### Key Benefits
- Interactive file exploration in Claude
- Files remain individually addressable
- Path information preserved in filenames
- Great for exploratory code analysis
- Optional token usage tracking

## Single File Approach

While the Claude Projects approach works well in Claude, other AI platforms like Google AI Studio handle multiple files differently. 

![data-ai-toolkit-6](https://github.com/user-attachments/assets/d2c0715d-4937-4a56-af03-dab58aaed82c)

Using `single_file_concat.py`, combine all files into a single document with clear START/END markers:

```bash
python single_file_concat.py ./data/this.json ./data/combined.txt
```

![data-ai-toolkit-4](https://github.com/user-attachments/assets/b66b42a0-c56b-49d7-bd44-f4519d8af06c)

We can now upload this file as context to any LLM.

![data-ai-toolkit-7](https://github.com/user-attachments/assets/0c634f15-40dc-48e6-b8e2-5631e6348c43)

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
- Optional token counting with `--count-tokens`

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
- Use token counting to stay within model context limits

## Token Counting Tips
- Enable token counting when preparing large codebases
- Use results to split files into appropriate batches
- Monitor token usage across different file types
- Consider model selection based on project size
- Remember token counting is optional - tool works without it