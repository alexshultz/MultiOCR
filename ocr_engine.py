from abc import ABC, abstractmethod
from typing import Dict, Any, List

class OCREngineError(Exception):
    def __init__(self, message: str, category: str, severity: str):
        self.message = message
        self.category = category
        self.severity = severity
        super().__init__(self.message)

class OCREngine(ABC):
    def __init__(self, engine_options: Dict[str, Any] = None):
        self.engine_options = engine_options or {}

    @abstractmethod
    async def prepare_file(self, file_path: str) -> Any:
        pass

    @abstractmethod
    async def process_file(self, prepared_file: Any) -> Any:
        pass

    @abstractmethod
    async def parse_results(self, raw_results: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_engine_name(self) -> str:
        pass

    @abstractmethod
    def get_supported_file_types(self) -> List[str]:
        pass

    @abstractmethod
    def get_engine_health(self) -> str:
        pass

    async def run_ocr(self, file_path: str) -> Dict[str, Any]:
        try:
            prepared_file = await self.prepare_file(file_path)
            raw_results = await self.process_file(prepared_file)
            return await self.parse_results(raw_results)
        except OCREngineError:
            raise
        except Exception as e:
            raise OCREngineError(f"Unexpected error during OCR process: {str(e)}", "OCR Engine", "critical")
