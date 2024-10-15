import os
from typing import List, Dict, Any
from ocr_engine import OCREngineError

class FileInputHandler:
    def __init__(self, input_path: str, supported_file_types: List[str], max_depth: int = 6):
        self.input_path = input_path
        self.supported_file_types = supported_file_types
        self.max_depth = max_depth

    def get_files_to_process(self) -> List[str]:
        if os.path.isfile(self.input_path):
            return [self.input_path] if self._is_supported_file(self.input_path) else []
        elif os.path.isdir(self.input_path):
            return self._get_files_from_directory(self.input_path)
        else:
            raise OCREngineError(f"Invalid input path: {self.input_path}", "Input Validation", "error")

    def _is_supported_file(self, file_path: str) -> bool:
        _, extension = os.path.splitext(file_path)
        return extension.lower() in self.supported_file_types

    def _get_files_from_directory(self, directory: str, current_depth: int = 0) -> List[str]:
        if current_depth > self.max_depth:
            return []

        files_to_process = []
        for entry in os.scandir(directory):
            if entry.is_file() and self._is_supported_file(entry.path):
                files_to_process.append(entry.path)
            elif entry.is_dir():
                files_to_process.extend(self._get_files_from_directory(entry.path, current_depth + 1))
        return files_to_process

    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise OCREngineError(f"File not found: {file_path}", "File System", "error")
        
        return {
            "file_name": os.path.basename(file_path),
            "file_path": os.path.abspath(file_path),
            "file_size": os.path.getsize(file_path),
            "creation_time": os.path.getctime(file_path),
            "modification_time": os.path.getmtime(file_path),
            "file_type": os.path.splitext(file_path)[1].lower()
        }
