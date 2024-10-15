from base_ocr_engine import BaseOCREngine
import pytesseract
from PIL import Image
from file_output_manager import FileOutputManager

class TesseractProcessor(BaseOCREngine):
    def __init__(self, output_dir, debug=False):
        """
        Initializes the TesseractProcessor with output directory and debugging options.
        :param output_dir: Directory where OCR results will be saved.
        :param debug: Enable detailed logging for debugging (optional).
        """
        self.output_manager = FileOutputManager(output_dir, 'tesseract', debug=debug)
        self.debug = debug

    def process_image(self, image_input, output_txt_name):
        """
        Processes an image using Tesseract OCR and saves the results.
        :param image_input: Path to image file or PIL Image object.
        :param output_txt_name: Name of the text file to save OCR results.
        """
        if isinstance(image_input, str):
            image = Image.open(image_input)
        else:
            image = image_input  # Assuming it's a PIL Image object

        if self.debug:
            print(f"Running Tesseract OCR on {image_input}...")

        # Run OCR with Tesseract
        text = pytesseract.image_to_string(image)

        # Save the OCR result
        self.output_manager.save_text(text, output_txt_name)

    def requires_pdf_conversion(self):
        """
        Tesseract requires PDFs to be converted to images first.
        """
        return True
