# AutoDoc

AutoDoc is an intelligent documentation generation and querying system that uses LMStudio to create and interact with module documentation. It consists of two main components: a documentation generator and a RAG-based (Retrieval-Augmented Generation) query system.

## Features

- Automatic documentation generation from source code
- Support for modular code structure
- Intelligent chunking of large files
- RAG-based documentation querying system
- Progress tracking with visual progress bars
- Interactive Q&A interface

## Project Structure

```
AutoDoc/
├── Documentation/          # Generated documentation storage
│   └── {ModuleName}/      # Module-specific documentation
├── Modules/               # Source code modules
├── Doc.js                 # Documentation generation script
├── RAG.js                # Documentation querying system
└── GetFiles.py           # File path extraction utility
```

## Prerequisites

- Node.js
- Python 3.x
- LMStudio
- Required NPM packages:
  - @lmstudio/sdk
  - cli-progress
  - readline

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

## Usage

### Step 1: Get Module Files

First, run the GetFiles script to scan your module and prepare files for documentation:

```bash
python GetFiles.py
```

This will:
- Scan the specified module directory
- Generate a list of available scripts
- Convert code files to text format for processing

### Step 2: Generate Documentation

Run the documentation generator:

```bash
node Doc.js
```

The script will:
1. Prompt for the module name
2. Read files listed in submodules.txt
3. Process each file in chunks
4. Generate comprehensive documentation in Markdown format

### Step 3: Query Documentation

Use the RAG-based query system to interact with the documentation:

```bash
node RAG.js
```

Features:
- Interactive Q&A interface
- Intelligent retrieval of relevant documentation
- Context-aware responses using LLM
- Continuous query mode with exit option

## Documentation Structure

The generated documentation follows this format:

```markdown
# {ModuleName} Module Documentation
Generated on: {Date}

## {SubmodulePath}
### Part 1/N
{Documentation Content}
---
```

## Models Used

- Text Embedding: nomic-embed-text-v1.5
- LLM: Various options including:
  - llama-3.2-3b-qnn
  - mistral-7b-instruct-v0.3

## Configuration

- Documentation chunks are approximately 300 tokens
- Context window is configured to stop at limit
- Temperature settings:
  - Documentation generation: 0.03 (highly focused)
  - RAG responses: 0.7 (more creative)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Error Handling

The system includes comprehensive error handling:
- File access verification
- Model initialization checks
- Graceful failure recovery
- Interactive error resolution

## Notes

- Keep LMStudio running while using the system
- Large modules may take significant time to process
- Documentation is generated in chunks to handle memory efficiently
