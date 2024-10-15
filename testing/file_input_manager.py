import os

class FileInputManager:
    def __init__(self, input_path, filetypes_file='filetypes.txt', depth=None, debug=False, output_dir='ocr_output'):
        """
        Initialize the FileInputManager with input directory, file types, and directory traversal settings.
        :param input_path: The directory or file to process.
        :param filetypes_file: File defining supported file types (default is filetypes.txt).
        :param depth: Optional. Limit how deep the system will traverse directories.
        :param debug: Enable detailed logging for debugging (optional).
        :param output_dir: The directory to save output, which will be ignored during input file collection.
        """
        self.input_path = input_path
        self.filetypes_file = filetypes_file
        self.depth = depth
        self.debug = debug
        self.output_dir = output_dir  # Directory to ignore during file collection
        self.supported_filetypes = self._load_supported_filetypes()

    def _load_supported_filetypes(self):
        """
        Loads the supported file types from the provided filetypes file.
        """
        with open(self.filetypes_file, 'r') as f:
            filetypes = f.read().splitlines()
        return [filetype.strip() for filetype in filetypes]

    def get_supported_files(self):
        """
        Returns a list of files that match the supported file types, excluding the output directory.
        """
        files_to_process = []

        # Check if input path is a directory
        if os.path.isdir(self.input_path):
            for root, dirs, files in os.walk(self.input_path):
                # Skip the output directory
                if os.path.abspath(root) == os.path.abspath(self.output_dir):
                    if self.debug:
                        print(f"Skipping output directory: {self.output_dir}")
                    continue

                # Check directory depth, if applicable
                if self.depth is not None:
                    current_depth = root[len(self.input_path):].count(os.sep)
                    if current_depth >= self.depth:
                        if self.debug:
                            print(f"Skipping directory due to depth limit: {root}")
                        continue

                for file in files:
                    file_path = os.path.join(root, file)
                    if self._is_supported_file(file_path):
                        if self.debug:
                            print(f"Found supported file: {file_path}")
                        files_to_process.append(file_path)
        else:
            # If input path is a single file, check if it's supported
            if self._is_supported_file(self.input_path):
                files_to_process.append(self.input_path)

        return files_to_process

    def _is_supported_file(self, file_path):
        """
        Checks if the file has a supported extension based on the filetypes list.
        :param file_path: Path to the file being checked.
        :return: True if file is supported, False otherwise.
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in self.supported_filetypes
