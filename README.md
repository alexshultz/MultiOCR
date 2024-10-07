
# MultiOCR Project

The **MultiOCR Project** will be a comprehensive system for processing files and extracting text using different Optical Character Recognition (OCR) engines. The project will include modular scripts for different OCR engines such as Tesseract, and it is designed to support future OCR integrations (e.g., Google Cloud Vision, Apple Vision, etc.).

## Features

- **Multi-Engine OCR**: Each OCR engine is handled by its own script, allowing flexibility and future expansion.
- **Modular Design**: Easily add new OCR processors by following the structure of the provided `ocr_tesseract.py`.
- **Batch Processing**: Handles entire directories of files, with support for depth control and file type filtering.
- **PDF to Image Conversion**: Automatically converts PDF files into images for OCR processing.
- **Diagnostics**: Optional diagnostics flag provides detailed logging of file processing steps.

## Current OCR Engines

- **Tesseract OCR**: Process files using Tesseract OCR with support for PDFs and image files.

## Installation

### Setting Up the Project

1. **Clone the Repository**:
2. 
   ```bash
   git clone https://github.com/your-repo/MultiOCR.git
   cd MultiOCR
   ```

2. **Create Conda Environment from `environment.yml`**:
3. 
   ```bash
   conda env create -f environment.yml
   conda activate ocr
   ```

## Usage

### Tesseract OCR

The `ocr_tesseract.py` script processes files using Tesseract OCR. You can use it to process both individual files and directories.

#### Command-Line Usage

To run the Tesseract OCR processor from the command line:

```bash
python ocr_tesseract.py [input_path] [--output output_dir] [--depth N] [--diagnostics]
```

- `input_path`: The file or directory you want to process.
- `--output`: Directory to save the OCR results (defaults to `ocr_output`).
- `--depth`: Optional, limits directory traversal depth.
- `--diagnostics`: Optional, enables detailed logging.

#### Example Commands

1. **Process the current directory**:
   ```bash
   python ocr_tesseract.py
   ```

2. **Process a specific directory**:
   ```bash
   python ocr_tesseract.py /path/to/input --output /path/to/output
   ```

3. **Process a PDF file**:
   ```bash
   python ocr_tesseract.py /path/to/file.pdf
   ```

## Adding New OCR Engines

The project is designed to be modular, allowing you to add new OCR engines easily. To add a new engine (e.g., Google Cloud Vision OCR), follow these steps:

1. Create a new script following the pattern of `ocr_tesseract.py` (e.g., `ocr_google.py`).
2. Use the `FileInputHandler` module to manage input files and directories.
3. Implement the OCR logic for the new engine.
4. Integrate the new script into the project and update the main README to reflect the new OCR module.

## Future Plans

- **Google Cloud Vision OCR**: Integration of Google Cloud Vision for OCR processing.
- **Apple Vision OCR**: Potential support for Apple's Vision framework for OCR.

Stay tuned for future updates!

## License

This project is licensed under the MIT License.
