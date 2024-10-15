import os

class FileOutputManager:
    def __init__(self, output_dir, ocr_module_name, debug=False):
        """
        Initialize FileOutputManager to handle saving OCR results.
        :param output_dir: The base directory where output will be saved.
        :param ocr_module_name: The name of the OCR module (e.g., 'tesseract', 'google') to append to filenames and create subdirectories.
        :param debug: Enable detailed logging for debugging (optional).
        """
        self.output_dir = output_dir
        self.ocr_module_name = ocr_module_name  # E.g., 'tesseract', 'google'
        self.debug = debug
        self._ensure_output_directory_exists()

    def _ensure_output_directory_exists(self):
        """
        Ensures the subdirectory for the OCR engine exists within the output directory.
        Creates the directory if it doesn't exist.
        """
        # Create the subdirectory for the OCR module
        ocr_output_path = os.path.join(self.output_dir, self.ocr_module_name)
        if not os.path.exists(ocr_output_path):
            os.makedirs(ocr_output_path)
            if self.debug:
                print(f"Created output directory: {ocr_output_path}")

    def save_text(self, text, output_filename):
        """
        Saves the OCR text output to a file, appending the OCR module name to the file name.
        :param text: The OCR text to save.
        :param output_filename: The base name of the output file.
        """
        # Append OCR module name to the output filename
        output_filename_with_module = f"{os.path.splitext(output_filename)[0]}_{self.ocr_module_name}.txt"
        
        # Save in the OCR module's subdirectory
        output_path = os.path.join(self.output_dir, self.ocr_module_name, output_filename_with_module)

        # Write the OCR result to the file
        with open(output_path, 'w') as f:
            f.write(text)

        if self.debug:
            print(f"OCR result saved to: {output_path}")

    def save_image(self, image, image_name):
        """
        Saves an image (e.g., from a converted PDF page) to the appropriate sub-directory.
        :param image: The PIL Image object to save.
        :param image_name: The base name of the image file.
        """
        # Save the image in the OCR module's subdirectory
        image_path = os.path.join(self.output_dir, self.ocr_module_name, image_name)
        image.save(image_path)

        if self.debug:
            print(f"Image saved to: {image_path}")

        return image_path  # Return the path to the saved image
