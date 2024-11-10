# Data AI Toolkit

## Motivation

Working with AI assistants like Claude often requires sharing multiple files and project structures. The traditional approach of copying and pasting files individually is tedious and error-prone. This toolkit solves that problem by automating the process of preparing files for AI interaction.

## Understanding Claude's File Handling

Claude Projects has some specific limitations when it comes to file uploads:

- You can't drag in folders or subfolders directly
- Each file must be at the root level
- Files must be dragged in all at once for a single conversation
- Nested directory structures aren't preserved naturally

This creates a challenge when you want to share a project that has files spread across multiple directories:

```
my_project/
├── src/
│   ├── core/
│   │   └── main.py
│   └── utils/
│       └── helpers.py
├── tests/
│   └── test_main.py
└── docs/
    └── api.md
```

## Our Solution

This toolkit solves these limitations by:

1. Flattening the directory structure into a single folder
2. Encoding path information in filenames using '@' symbols:
```
claude_ready/
├── src@core@main.py
├── src@utils@helpers.py
├── tests@test_main.py
└── docs@api.md
```

Now you can:
1. Drag all files at once into Claude
2. Maintain directory context through the encoded paths
3. Work with projects of any size or complexity

## Basic Usage

```bash
# 1. Scan your project
python dir_scanner.py ./my_project ./data/project.json

# 2. Prepare for Claude
python claude_concat.py ./data/project.json ./data/claude_ready/

# 3. Drag all files from claude_ready/ into Claude Projects
```

## Next Steps

Future documentation will cover:
- Detailed usage guides
- Real-world examples
- Advanced features
- Best practices