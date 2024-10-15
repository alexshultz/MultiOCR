import os
from pdf2image import convert_from_path
from file_input_manager import FileInputManager

class FileProcessor:
    def __init__(self, ocr_engine, output_dir, filetypes_file='filetypes.txt', debug=False):
        """
        Initialize FileProcessor for managing file preparation and processing for OCR.
        :param ocr_engine: The OCR engine to use (must implement BaseOCREngine).
        :param output_dir: Directory where OCR results will be saved.
        :param filetypes_file: File defining supported file types (default is filetypes.txt).
        :param debug: Enable detailed logging for debugging (optional).
        """
        self.ocr_engine = ocr_engine  # Any OCR engine implementing BaseOCREngine
        self.output_dir = output_dir
        self.filetypes_file = filetypes_file
        self.debug = debug

    def process_file(self, file_path, convert_pdf=False):
        """
        Process a single file: if it's a PDF, convert it to images if required.
        :param file_path: Path to the file to be processed.
        :param convert_pdf: If True, converts PDFs to images before processing.
        """
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == '.pdf':
            if convert_pdf:
                if self.debug:
                    print(f"Converting PDF {file_path} to images for {self.ocr_engine.__class__.__name__}...")
                images = convert_from_path(file_path)
                for i, image in enumerate(images):
                    image_name = f"{os.path.basename(file_path)}_page_{i+1}.png"
                    self.ocr_engine.process_image(image, image_name)
            else:
                if self.debug:
                    print(f"Processing PDF {file_path} directly with {self.ocr_engine.__class__.__name__}...")
                self.ocr_engine.process_image(file_path, f"{os.path.basename(file_path)}.txt")
        else:
            if self.debug:
                print(f"Processing image {file_path} with {self.ocr_engine.__class__.__name__}...")
            self.ocr_engine.process_image(file_path, f"{os.path.basename(file_path)}.txt")

    def process_directory(self, input_path, convert_pdf=False, depth=None):
        """
        Process a directory: traverse files, and process each supported file for OCR.
        :param input_path: Path to the input directory.
        :param convert_pdf: If True, converts PDFs to images before processing.
        :param depth: Directory traversal depth (optional).
        """
        file_manager = FileInputManager(input_path, self.filetypes_file, depth=depth, debug=self.debug)
        input_files = file_manager.get_supported_files()

        for file_path in input_files:
            self.process_file(file_path, convert_pdf=convert_pdf)
