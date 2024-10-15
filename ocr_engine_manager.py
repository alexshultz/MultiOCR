import asyncio
import os
from typing import List, Dict, Any
from ocr_engine import OCREngine, OCREngineError
from file_input_handler import FileInputHandler
from output_formatter import OutputFormatter
import json

class OCREngineManager:
    def __init__(self, output_dir: str):
        self.engines: List[OCREngine] = []
        self.output_formatter = OutputFormatter(output_dir)

    def register_engine(self, engine: OCREngine):
        self.engines.append(engine)

    async def process_files(self, input_path: str, max_depth: int = 6):
        supported_file_types = set()
        for engine in self.engines:
            supported_file_types.update(engine.get_supported_file_types())

        file_handler = FileInputHandler(input_path, list(supported_file_types), max_depth)
        
        try:
            files_to_process = file_handler.get_files_to_process()
        except OCREngineError as e:
            print(f"Error getting files to process: {e}")
            return

        for file_path in files_to_process:
            try:
                metadata = file_handler.extract_metadata(file_path)
                self.output_formatter.save_metadata(os.path.basename(file_path), metadata)

                results = await self._process_file(file_path)
                self.output_formatter.save_result(os.path.basename(file_path), results)
            except OCREngineError as e:
                print(f"Error processing file {file_path}: {e}")

    async def _process_file(self, file_path: str) -> Dict[str, Any]:
        results = {}
        tasks = []

        for engine in self.engines:
            task = asyncio.create_task(self._run_engine(engine, file_path))
            tasks.append(task)

        completed_tasks = await asyncio.gather(*tasks, return_exceptions=True)

        for engine, task_result in zip(self.engines, completed_tasks):
            if isinstance(task_result, Exception):
                results[engine.get_engine_name()] = {"error": str(task_result)}
            else:
                # Ensure the result is JSON serializable
                try:
                    json.dumps(task_result)  # This will raise an error if not serializable
                    results[engine.get_engine_name()] = task_result
                except TypeError:
                    results[engine.get_engine_name()] = {"error": "Result not JSON serializable"}

        return results

    async def _run_engine(self, engine: OCREngine, file_path: str) -> Dict[str, Any]:
        try:
            return await engine.run_ocr(file_path)
        except OCREngineError as e:
            raise e
        except Exception as e:
            raise OCREngineError(f"Unexpected error in {engine.get_engine_name()}: {str(e)}", "OCR Engine", "error")

    def get_overall_health(self) -> str:
        if not self.engines:
            return "RED"  # No engines registered
        
        health_statuses = [engine.get_engine_health() for engine in self.engines]
        if all(status == "GREEN" for status in health_statuses):
            return "GREEN"
        elif any(status == "RED" for status in health_statuses):
            return "RED"
        else:
            return "YELLOW"

# Usage example
async def main():
    manager = OCREngineManager("output_directory")
    tesseract_engine = TesseractEngine()
    manager.register_engine(tesseract_engine)

    await manager.process_files("input_directory")
    print(f"Overall health: {manager.get_overall_health()}")

if __name__ == "__main__":
    asyncio.run(main())
