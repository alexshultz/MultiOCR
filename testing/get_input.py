import os
import json
import argparse

def load_supported_filetypes(filetype_file, diagnostics=False):
    """Load supported file types from a file (txt or json)."""
    if filetype_file.endswith('.txt'):
        with open(filetype_file, 'r') as f:
            if diagnostics:
                print(f"Loading file types from: {filetype_file}")
            return [line.strip() for line in f if line.strip()]  # Handles plain text format
    elif filetype_file.endswith('.json'):
        with open(filetype_file, 'r') as f:
            if diagnostics:
                print(f"Loading file types from: {filetype_file}")
            return json.load(f)  # Handles JSON format
    else:
        raise ValueError("Unsupported file type definition. Use .txt or .json.")

def is_supported_file(file_path, supported_extensions, diagnostics=False):
    """Check if the file has a valid extension for OCR."""
    _, ext = os.path.splitext(file_path)
    if diagnostics:
        print(f"Checking file: {file_path}, extension: {ext}")
    return ext.lower() in supported_extensions

def find_files_in_directory(directory_path, supported_extensions, depth=None, diagnostics=False):
    """Find and return all supported files in the given directory up to a specified depth."""
    files = []
    
    current_depth = directory_path.count(os.sep)
    if diagnostics:
        print(f"Starting directory search at: {directory_path}, current depth: {current_depth}")

    for root, _, filenames in os.walk(directory_path):
        relative_depth = root.count(os.sep) - current_depth
        if diagnostics:
            print(f"Searching in: {root}, relative depth: {relative_depth}")

        # Stop going deeper if depth limit is reached
        if depth is not None and relative_depth > depth:
            if diagnostics:
                print(f"Skipping directory {root} due to depth limit")
            continue

        # Filter for files with the supported extensions
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if diagnostics:
                print(f"Found file: {file_path}")
            if is_supported_file(file_path, supported_extensions, diagnostics):
                if diagnostics:
                    print(f"Found supported file: {file_path}")
                files.append(file_path)
    
    return files

def get_files_to_process(path, supported_extensions, depth=None, diagnostics=False):
    """Check if the input path is a file or a directory and find valid files."""
    if diagnostics:
        print(f"Input path: {path}")
    if os.path.isfile(path):
        if diagnostics:
            print(f"Path is a file: {path}")
        # If it's a single file, check if it's a supported file
        if is_supported_file(path, supported_extensions, diagnostics):
            return [path]
        else:
            return []
    elif os.path.isdir(path):
        if diagnostics:
            print(f"Path is a directory: {path}")
        # If it's a directory, search for supported files with depth limitation
        return find_files_in_directory(path, supported_extensions, depth, diagnostics)
    else:
        print(f"Error: {path} is not a valid file or directory.")
        return []

# Parse command-line arguments
parser = argparse.ArgumentParser(description="File Search with Optional Depth for OCR Processing")
parser.add_argument('input_path', nargs='?', default=os.getcwd(), help="File or directory path to search (defaults to current directory)")
parser.add_argument('--depth', type=int, help="Optional depth to limit directory traversal")
parser.add_argument('--diagnostics', action='store_true', help="Enable detailed diagnostics")

args = parser.parse_args()

# Load supported file types from filetypes.txt (plain text) or filetypes.json
supported_filetypes_file = 'filetypes.txt'  # Change to filetypes.json if using that format
supported_extensions = load_supported_filetypes(supported_filetypes_file, args.diagnostics)

# Get files to process with optional depth
files_to_process = get_files_to_process(args.input_path, supported_extensions, args.depth, args.diagnostics)

if files_to_process:
    print(f"Files to process: {files_to_process}")
else:
    print("No supported files found.")