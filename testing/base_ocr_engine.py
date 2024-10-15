from abc import ABC, abstractmethod

class BaseOCREngine(ABC):
    @abstractmethod
    def process_image(self, image_input, output_txt_name):
        """
        Abstract method to process an image with OCR.
        Must be implemented by each OCR engine.
        :param image_input: Path to image file or PIL Image object.
        :param output_txt_name: Name of the text file to save OCR results.
        """
        pass

