import os
import json
from google.cloud import secretmanager
from google.oauth2 import service_account
from google.cloud import vision
from pdf2image import convert_from_path
from file_input_manager import FileInputManager  # Updated import
from file_output_manager import FileOutputManager  # Updated import
from PIL import Image

class GoogleVisionProcessor:
    def __init__(self, output_dir, filetypes_file='filetypes.txt', debug=False):
        """
        Initializes the GoogleVisionProcessor and sets up the output directory.
        """
        self.input_manager = FileInputManager(output_dir, filetypes_file, debug=debug)
        self.output_manager = FileOutputManager(output_dir, 'google_vision', debug=debug)
        self.filetypes_file = filetypes_file
        self.debug = debug

        # Set up Google Vision client
        self.client = self.setup_google_vision_client()

    def setup_google_vision_client(self):
        """
        Set up Google Vision client using the service account key stored in Google Secret Manager.
        """
        client = secretmanager.SecretManagerServiceClient()
        secret_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/MultiOCR-service-account-key/versions/latest"
        response = client.access_secret_version(request={"name": secret_name})
        secret_payload = response.payload.data.decode("UTF-8")

        service_account_info = json.loads(secret_payload)
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        return vision.ImageAnnotatorClient(credentials=credentials)

    def process_file(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == '.pdf':
            if self.debug:
                print(f"Converting PDF {file_path} to images...")
            # Convert PDF to images
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                image_path = os.path.join(self.output_manager.output_dir, f"{os.path.basename(file_path)}_page_{i+1}_google_vision.png")
                image.save(image_path, 'PNG')
                self._ocr_image(image_path, self.output_manager.generate_output_path(file_path, page_number=i+1))
        else:
            # If not PDF, assume it's an image
            self._ocr_image(file_path, self.output_manager.generate_output_path(file_path))

    def process_directory(self, input_path, depth=None):
        """
        Processes a directory of files using Google Vision OCR, applying depth control for directory traversal.
        """
        input_files = self.input_manager.get_supported_files()

        # Process each file
        for file_path in input_files:
            self.process_file(file_path)

    def _ocr_image(self, image_input, output_txt_path):
        """
        Runs Google Vision OCR on an image file and saves the results.
        """
        with open(image_input, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        if self.debug:
            print(f"Running OCR on image {image_input}...")

        # Perform text detection using Google Vision API
        response = self.client.text_detection(image=image)
        texts = response.text_annotations

        # Save the extracted text
        if texts:
            text = texts[0].description
        else:
            text = "No text detected"

        # Save the OCR result using save_text instead of save_ocr_result
        self.output_manager.save_text(text, output_txt_path)


# Command-line entry point
if __name__ == "__main__":
    import argparse

    # Set up argument parsing for command-line inputs
    parser = argparse.ArgumentParser(description="Process files for OCR using Google Vision")
    parser.add_argument('input_path', nargs='?', default=os.getcwd(), help="Path to the input file or directory (defaults to current directory)")
    parser.add_argument('--output', default='ocr_output', help="Directory to save OCR results (default: ocr_output)")
    parser.add_argument('--filetypes', default='filetypes.txt', help="File defining supported file types (default: filetypes.txt)")
    parser.add_argument('--depth', type=int, help="Limit directory traversal depth")
    parser.add_argument('--debug', action='store_true', help="Enable detailed debug logging")

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the GoogleVisionProcessor
    processor = GoogleVisionProcessor(output_dir=args.output, filetypes_file=args.filetypes, debug=args.debug)

    # Check if the input path is a file or a directory
    if os.path.isdir(args.input_path):
        processor.process_directory(args.input_path, depth=args.depth)
    else:
        processor.process_file(args.input_path)
