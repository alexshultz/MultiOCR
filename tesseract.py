import os
import argparse
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from file_input_handler import FileInputHandler  # Import the class from the renamed file

class TesseractProcessor:
    def __init__(self, input_path, output_dir, filetypes_file='filetypes.txt', depth=None, diagnostics=False):
        """
        Initializes the TesseractProcessor with paths and processing options.
        :param input_path: Path to the input file or directory.
        :param output_dir: Directory where OCR results will be saved.
        :param filetypes_file: File defining supported file types (default is filetypes.txt).
        :param depth: Directory traversal depth (optional).
        :param diagnostics: Enable detailed logging for debugging (optional).
        """
        self.input_path = input_path
        self.output_dir = output_dir
        self.diagnostics = diagnostics
        self.file_handler = FileInputHandler(input_path, filetypes_file, depth, diagnostics)

    def process_file(self, file_path):
        """
        Processes a single file with Tesseract OCR. Converts PDFs to images if necessary.
        :param file_path: Path to the file to be processed.
        """
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == '.pdf':
            if self.diagnostics:
                print(f"Converting PDF {file_path} to images...")
            # Convert PDF to images
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                image_path = os.path.join(self.output_dir, f"{os.path.basename(file_path)}_page_{i+1}.png")
                image.save(image_path, 'PNG')
                self.ocr_image(image, os.path.join(self.output_dir, f"{os.path.basename(file_path)}_page_{i+1}.txt"))
        else:
            # If not PDF, assume it's an image
            self.ocr_image(file_path, os.path.join(self.output_dir, f"{os.path.basename(file_path)}.txt"))

    def ocr_image(self, image_input, output_txt_path):
        """
        Runs Tesseract OCR on an image and saves the results to a text file.
        :param image_input: Path to the image file or a PIL Image object.
        :param output_txt_path: Path where OCR results will be saved.
        """
        if isinstance(image_input, str):  # If input is a file path
            image = Image.open(image_input)
        else:
            image = image_input  # If it's already a PIL Image object

        if self.diagnostics:
            print(f"Running OCR on image {image_input}...")

        text = pytesseract.image_to_string(image)

        with open(output_txt_path, 'w') as f:
            f.write(text)

        if self.diagnostics:
            print(f"OCR result saved to {output_txt_path}")

    def prepare_and_process_files(self):
        """
        Prepares and processes all input files using Tesseract OCR.
        """
        # Get the list of files to process from FileInputHandler
        input_files = self.file_handler.get_supported_files()

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Process each file
        for file_path in input_files:
            self.process_file(file_path)


def main():
    # Set up argument parsing for command-line inputs
    parser = argparse.ArgumentParser(description="Process files for OCR using Tesseract")
    parser.add_argument('input_path', nargs='?', default=os.getcwd(), help="Path to the input file or directory (defaults to current directory)")
    parser.add_argument('--output', default='ocr_output', help="Directory to save OCR results (default: ocr_output)")
    parser.add_argument('--filetypes', default='filetypes.txt', help="File defining supported file types (default: filetypes.txt)")
    parser.add_argument('--depth', type=int, help="Limit directory traversal depth")
    parser.add_argument('--diagnostics', action='store_true', help="Enable detailed diagnostics")

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the TesseractProcessor with the parsed arguments
    processor = TesseractProcessor(
        input_path=args.input_path,
        output_dir=args.output,
        filetypes_file=args.filetypes,
        depth=args.depth,
        diagnostics=args.diagnostics
    )

    # Start processing the files
    processor.prepare_and_process_files()

if __name__ == "__main__":
    main()