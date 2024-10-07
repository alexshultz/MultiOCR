import os
import json
import argparse

class FileInputHandler:
    def __init__(self, input_path, filetype_file, depth=None, diagnostics=False):
        """
        Initialize the file input handler with path, file types, depth, and diagnostics options.
        :param input_path: Path to file or directory.
        :param filetype_file: File (txt or json) that contains the list of supported file types.
        :param depth: Directory traversal depth (optional).
        :param diagnostics: Enable detailed logging for debugging.
        """
        self.input_path = input_path
        self.filetype_file = filetype_file
        self.depth = depth
        self.diagnostics = diagnostics
        self.supported_extensions = self._load_supported_filetypes(filetype_file)

    def _load_supported_filetypes(self, filetype_file):
        """(Private) Load supported file types from a file (txt or json)."""
        if self.diagnostics:
            print(f"Loading file types from: {filetype_file}")

        if filetype_file.endswith('.txt'):
            with open(filetype_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]  # Handles plain text format
        elif filetype_file.endswith('.json'):
            with open(filetype_file, 'r') as f:
                return json.load(f)  # Handles JSON format
        else:
            raise ValueError("Unsupported file type definition. Use .txt or .json.")

    def _is_supported_file(self, file_path):
        """(Private) Check if the file has a valid extension for OCR."""
        _, ext = os.path.splitext(file_path)
        if self.diagnostics:
            print(f"Checking file: {file_path}, extension: {ext}")
        return ext.lower() in self.supported_extensions

    def _find_files_in_directory(self, directory_path):
        """(Private) Find and return all supported files in the given directory up to a specified depth."""
        files = []
        current_depth = directory_path.count(os.sep)
        if self.diagnostics:
            print(f"Starting directory search at: {directory_path}, current depth: {current_depth}")

        for root, _, filenames in os.walk(directory_path):
            relative_depth = root.count(os.sep) - current_depth
            if self.diagnostics:
                print(f"Searching in: {root}, relative depth: {relative_depth}")

            # Stop going deeper if depth limit is reached
            if self.depth is not None and relative_depth > self.depth:
                if self.diagnostics:
                    print(f"Skipping directory {root} due to depth limit")
                continue

            # Filter for files with the supported extensions
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if self.diagnostics:
                    print(f"Found file: {file_path}")
                if self._is_supported_file(file_path):
                    if self.diagnostics:
                        print(f"Found supported file: {file_path}")
                    files.append(file_path)

        return files

    def get_supported_files(self):
        """(Public) Check if the input path is a file or a directory and return a list of valid files."""
        if self.diagnostics:
            print(f"Input path: {self.input_path}")

        if os.path.isfile(self.input_path):
            if self.diagnostics:
                print(f"Path is a file: {self.input_path}")
            # If it's a single file, check if it's a supported file
            if self._is_supported_file(self.input_path):
                return [self.input_path]
            else:
                return []
        elif os.path.isdir(self.input_path):
            if self.diagnostics:
                print(f"Path is a directory: {self.input_path}")
            # If it's a directory, search for supported files with depth limitation
            return self._find_files_in_directory(self.input_path)
        else:
            print(f"Error: {self.input_path} is not a valid file or directory.")
            return []

# Example usage if running the script directly
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="File Search with Optional Depth for OCR Processing")
    parser.add_argument('input_path', nargs='?', default=os.getcwd(), help="File or directory path to search (defaults to current directory)")
    parser.add_argument('--depth', type=int, help="Optional depth to limit directory traversal")
    parser.add_argument('--diagnostics', action='store_true', help="Enable detailed diagnostics")

    args = parser.parse_args()

    # Load supported file types from filetypes.txt (plain text) or filetypes.json
    filetypes_file = 'filetypes.txt'  # You can switch to filetypes.json if needed

    # Initialize the FileInputHandler with arguments
    handler = FileInputHandler(input_path=args.input_path, filetype_file=filetypes_file, depth=args.depth, diagnostics=args.diagnostics)

    # Get files to process
    files_to_process = handler.get_supported_files()

    if files_to_process:
        print(f"Files to process: {files_to_process}")
    else:
        print("No supported files found.")
