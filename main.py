import asyncio
import argparse
from ocr_engine_manager import OCREngineManager
from tesseract_engine import TesseractEngine

async def main(input_path: str, output_dir: str, max_depth: int):
    # Initialize OCREngineManager
    manager = OCREngineManager(output_dir)

    # Register Tesseract engine
    tesseract_engine = TesseractEngine()
    manager.register_engine(tesseract_engine)

    # Process files
    await manager.process_files(input_path, max_depth)

    # Print overall health
    print(f"Overall system health: {manager.get_overall_health()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MultiOCR System")
    parser.add_argument("input_path", help="Path to input file or directory")
    parser.add_argument("--output", default="ocr_output", help="Output directory for OCR results")
    parser.add_argument("--max-depth", type=int, default=6, help="Maximum depth for directory traversal")

    args = parser.parse_args()

    asyncio.run(main(args.input_path, args.output, args.max_depth))
