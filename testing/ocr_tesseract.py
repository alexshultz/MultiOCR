import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from file_input_manager import FileInputManager
from file_output_manager import FileOutputManager  # Importing the external FileOutputManager

class TesseractProcessor:
    def __init__(self, output_dir, filetypes_file='filetypes.txt', debug=False):
        """
        Initializes the TesseractProcessor with output directory and file type filter options.
        :param output_dir: Directory where OCR results will be saved.
        :param filetypes_file: File defining supported file types (default is filetypes.txt).
        :param debug: Enable detailed logging for debugging (optional).
        """
        self.output_dir = output_dir
        self.filetypes_file = filetypes_file
        self.debug = debug

        # Initialize FileOutputManager for handling output
        self.output_manager = FileOutputManager(output_dir, debug=self.debug)

    def process_file(self, file_path):
        """
        Processes a single file with Tesseract OCR. Converts PDFs to images if necessary.
        :param file_path: Path to the file to be processed.
        """
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == '.pdf':
            if self.debug:
                print(f"Converting PDF {file_path} to images...")
            # Convert PDF to images
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                image_name = f"{os.path.basename(file_path)}_page_{i+1}.png"
                image_path = self.output_manager.save_image(image, image_name)
                self._ocr_image(image_path, f"{os.path.basename(file_path)}_page_{i+1}.txt")
        else:
            # If not PDF, assume it's an image
            self._ocr_image(file_path, f"{os.path.basename(file_path)}.txt")

    def process_directory(self, input_path, depth=None):
        """
        Processes a directory of files using Tesseract OCR, applying depth control for directory traversal.
        :param input_path: Path to the input directory.
        :param depth: Limits directory traversal depth (optional).
        """
        # Initialize the file manager
        file_manager = FileInputManager(input_path, self.filetypes_file, depth=depth, debug=self.debug, output_dir=self.output_dir)

        # Get the list of supported files
        input_files = file_manager.get_supported_files()

        # Process each file
        for file_path in input_files:
            self.process_file(file_path)

    def _ocr_image(self, image_input, output_txt_name):
        """
        Runs Tesseract OCR on an image file and saves the results.
        :param image_input: Path to image file or PIL Image object.
        :param output_txt_name: Name of the text file to save OCR results.
        """
        if isinstance(image_input, str):  # If input is a file path
            image = Image.open(image_input)
        else:
            image = image_input  # If it's already a PIL Image object

        if self.debug:
            print(f"Running OCR on image {image_input}...")

        text = pytesseract.image_to_string(image)

        # Use FileOutputManager to save OCR text
        self.output_manager.save_text(text, output_txt_name)


if __name__ == "__main__":
    import argparse

    # Set up argument parsing for command-line inputs
    parser = argparse.ArgumentParser(description="Process files for OCR using Tesseract")
    parser.add_argument('input_path', nargs='?', default=os.getcwd(), help="Path to the input file or directory (defaults to current directory)")
    parser.add_argument('--output', default='ocr_output', help="Directory to save OCR results (default: ocr_output)")
    parser.add_argument('--filetypes', default='filetypes.txt', help="File defining supported file types (default: filetypes.txt)")
    parser.add_argument('--depth', type=int, help="Limit directory traversal depth")
    parser.add_argument('--debug', action='store_true', help="Enable detailed debug logging")  # Updated to --debug

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the TesseractProcessor
    processor = TesseractProcessor(output_dir=args.output, filetypes_file=args.filetypes, debug=args.debug)  # Use debug flag

    # Check if the input path is a file or a directory
    if os.path.isdir(args.input_path):
        processor.process_directory(args.input_path, depth=args.depth)
    else:
        processor.process_file(args.input_path)
