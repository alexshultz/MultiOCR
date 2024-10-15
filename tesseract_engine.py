import asyncio
from typing import Dict, Any, List
from collections import deque
import pytesseract
from PIL import Image
import os
from datetime import datetime

from ocr_engine import OCREngine, OCREngineError

class TesseractEngine(OCREngine):
    def __init__(self, engine_options: Dict[str, Any] = None):
        super().__init__(engine_options)
        self.name = "Tesseract"
        self.supported_file_types = ['.pdf', '.png', '.jpg', '.jpeg', '.tif', '.tiff', '.gif']
        self.health_queue = deque(maxlen=10)  # Store last 10 operation statuses
        self.initialize_engine()

    def initialize_engine(self):
        try:
            self.tesseract_version = str(pytesseract.get_tesseract_version())  # Convert to string
            self.health_queue.append(True)
        except Exception as e:
            self.health_queue.append(False)
            raise OCREngineError(f"Failed to initialize Tesseract: {str(e)}", "OCR Engine", "critical")

    async def prepare_file(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise OCREngineError(f"File not found: {file_path}", "File System", "error")
        if not os.access(file_path, os.R_OK):
            raise OCREngineError(f"No read permission for file: {file_path}", "File System", "error")
        
        # Verify file integrity
        try:
            with Image.open(file_path) as img:
                img.verify()
        except Exception as e:
            raise OCREngineError(f"Invalid or corrupted image file: {file_path}. Error: {str(e)}", "Input Validation", "error")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in self.supported_file_types:
            raise OCREngineError(f"Unsupported file type: {file_extension}", "Input Validation", "error")
        return file_path

    async def process_file(self, prepared_file: str) -> Dict[str, Any]:
        try:
            start_time = datetime.now()
            with Image.open(prepared_file) as image:
                result = await asyncio.to_thread(
                    pytesseract.image_to_string,
                    image,
                    lang=self.engine_options.get('lang', 'eng'),
                    config=self.engine_options.get('config', '--psm 1')
                )
            processing_time = (datetime.now() - start_time).total_seconds()
            return {"raw_result": result, "processing_time": processing_time}
        except Exception as e:
            self.health_queue.append(False)
            raise OCREngineError(f"Tesseract processing failed: {str(e)}", "OCR Engine", "error")

    async def parse_results(self, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        try:
            text = raw_results["raw_result"]
            
            result = {
                "text": text,
                "confidence": None,  # Tesseract doesn't provide overall confidence for image_to_string
                "pages": [
                    {
                        "page_number": 1,
                        "text": text,
                        "confidence": None,
                    }
                ],
                "metadata": {
                    "engine_name": self.name,
                    "tesseract_version": self.tesseract_version,  # This is now a string
                    "processing_time": raw_results["processing_time"],
                    "lang": self.engine_options.get('lang', 'eng'),
                }
            }

            self.health_queue.append(True)
            return result
        except Exception as e:
            self.health_queue.append(False)
            raise OCREngineError(f"Failed to parse Tesseract results: {str(e)}", "OCR Engine", "error")

    def get_engine_name(self) -> str:
        return self.name

    def get_supported_file_types(self) -> List[str]:
        return self.supported_file_types

    def get_engine_health(self) -> str:
        if not self.health_queue:
            return "YELLOW"  # No operations performed yet
        
        success_rate = sum(self.health_queue) / len(self.health_queue)
        if success_rate == 1.0 and len(self.health_queue) == self.health_queue.maxlen:
            return "GREEN"
        elif success_rate >= 0.7:
            return "YELLOW"
        else:
            return "RED"
