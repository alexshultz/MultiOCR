
# File Input Handler

The `file_input_handler.py` script is responsible for handling input files and directories, filtering by supported file types, and controlling directory traversal depth. It is part of the **MultiOCR** project and serves as a modular tool for managing file inputs before they are processed by the OCR systems.

## Features

- Accepts files or directories as input.
- Filters files based on supported extensions (e.g., PDFs, PNGs, JPGs).
- Limits directory traversal using the `--depth` argument.
- Provides a diagnostics mode (`--diagnostics`) to output detailed information about file and directory checks.

## Class: `FileInputHandler`

### Overview

The `FileInputHandler` class is designed to manage input files and directories, allowing for file type filtering and directory depth control. It can be used as part of the larger OCR system or independently to handle file input operations.

### Methods

- `__init__(self, input_path, filetype_file, depth=None, diagnostics=False)`: Initializes the handler with a directory or file path, file type filters, depth control, and optional diagnostics mode.
  
  - `input_path` (str): Path to the input directory or file.
  - `filetype_file` (str): Path to the file that lists supported file types (e.g., `filetypes.txt`).
  - `depth` (int, optional): Limits how deep the directory traversal should go.
  - `diagnostics` (bool, optional): If `True`, enables detailed logging.
  
- `get_supported_files(self)`: Returns a list of files that match the supported file types and depth limits.
  
  - **Returns**: A list of file paths that match the specified criteria.
  
- `_load_supported_filetypes(self, filetype_file)`: Loads supported file types from a `.txt` or `.json` file. (Private method)

- `_is_supported_file(self, file_path)`: Checks if a file has a valid extension. (Private method)

- `_find_files_in_directory(self, directory_path)`: Traverses directories to find supported files based on depth and file type filtering. (Private method)

### Example Usage in Python

You can import and use the `FileInputHandler` class in your own scripts:

```python
from file_input_handler import FileInputHandler

# Initialize the file handler with a directory, file type filter, and depth
handler = FileInputHandler(input_path="/path/to/input", filetype_file="filetypes.txt", depth=2, diagnostics=True)

# Get the list of supported files
files = handler.get_supported_files()

# Process the files
for file in files:
    print(f"Processing file: {file}")
```

## Installation

Ensure you have Python 3.x installed and any dependencies for the project (e.g., `os` and `argparse`).

## Usage

To use the `file_input_handler.py` script from the command line:

```bash
python file_input_handler.py [input_path] [--depth N] [--diagnostics]
```

### Command-Line Arguments

- `input_path`: Path to the input file or directory (defaults to the current directory if not provided).
- `--depth`: Limit how deep the script will traverse directories. For example, `--depth 2` will limit traversal to two levels.
- `--diagnostics`: Enables detailed output for debugging, showing what files are being processed and why certain files are included or excluded.

### Examples

#### Process all files in the current directory with diagnostics:

```bash
python file_input_handler.py --diagnostics
```

#### Process a specific directory with a depth limit of 2:

```bash
python file_input_handler.py /path/to/directory --depth 2
```

#### Process a specific file:

```bash
python file_input_handler.py /path/to/file.pdf
```

## Integration

`file_input_handler.py` can be used as a standalone script or integrated into larger Python projects where directory traversal and file filtering are required.
