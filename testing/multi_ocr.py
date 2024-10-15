import os
import argparse
from file_processor import FileProcessor
from tesseract_processor import TesseractProcessor
from google_vision_processor import GoogleVisionProcessor

# Available OCR engines
available_engines = {
    'tesseract': TesseractProcessor,
    'google_vision': GoogleVisionProcessor
}

def parse_engines(args):
    """
    Parse the engine flags to determine which OCR engines to use.
    :param args: Command-line arguments
    :return: List of OCR engines to use and their corresponding PDF conversion flag
    """
    selected_engines = []

    # If no --engine flag is specified, use all available engines
    if args.engine is None:
        return list(available_engines.keys())  # Use all available engines by default

    # Handle the case where the user provides a comma-separated list or multiple --engine flags
    for engine_arg in args.engine:
        # Split comma-separated values and add them to the list
        selected_engines.extend(engine_arg.split(','))

    # Remove any duplicates and ensure valid engine names
    selected_engines = list(set([engine.strip() for engine in selected_engines if engine.strip() in available_engines]))

    return selected_engines


if __name__ == "__main__":
    # Set up argument parsing for command-line inputs
    parser = argparse.ArgumentParser(description="Process files for OCR using Tesseract or Google Vision")
    parser.add_argument('input_path', nargs='?', default=os.getcwd(), help="Path to the input file or directory (defaults to current directory)")
    parser.add_argument('--output', default='ocr_output', help="Directory to save OCR results (default: ocr_output)")
    parser.add_argument('--filetypes', default='filetypes.txt', help="File defining supported file types (default: filetypes.txt)")
    parser.add_argument('--engine', action='append', help="Specify OCR engine(s) to use. Can be used multiple times or as a comma-separated list (e.g., --engine tesseract,google_vision).")
    parser.add_argument('--depth', type=int, help="Limit directory traversal depth")
    parser.add_argument('--debug', action='store_true', help="Enable detailed debug logging")

    # Parse the arguments
    args = parser.parse_args()

    # Determine which engines to use based on the parsed input
    selected_engines = parse_engines(args)

    # Process files with each selected OCR engine
    for engine_name in selected_engines:
        if engine_name == 'tesseract':
            ocr_engine = TesseractProcessor(output_dir=args.output, debug=args.debug)
            convert_pdf = True  # Tesseract needs PDF conversion
        elif engine_name == 'google_vision':
            ocr_engine = GoogleVisionProcessor(output_dir=args.output, debug=args.debug)
            convert_pdf = False  # Google Vision does not need PDF conversion

        print(f"Using {engine_name} engine...")

        # Initialize the FileProcessor with the selected OCR engine
        processor = FileProcessor(ocr_engine=ocr_engine, output_dir=args.output, filetypes_file=args.filetypes, debug=args.debug)

        # Check if the input path is a file or a directory
        if os.path.isdir(args.input_path):
            processor.process_directory(args.input_path, convert_pdf=convert_pdf, depth=args.depth)
        else:
            processor.process_file(args.input_path, convert_pdf=convert_pdf)
