
# Tesseract OCR Processor

The `ocr_tesseract.py` script is responsible for processing files using Tesseract OCR. It handles input files or directories, converts PDFs to images if needed, and runs OCR on the images to extract text. The results are saved as text files.

## Features

- Processes individual files or directories.
- Converts PDF files into images for OCR processing.
- Runs Tesseract OCR on supported image formats (e.g., PNG, JPEG).
- Provides command-line options to control output directories, depth of directory traversal, and diagnostics.

## Programmatic Usage

The `ocr_tesseract.py` script encapsulates its functionality in the `TesseractProcessor` class, which allows you to integrate it into other Python scripts.

### Available Methods:

- **`process_file(file_path)`**: 
    - Processes a single file using Tesseract. If the file is a PDF, it converts the PDF to images before processing.
    - **Parameters**:
        - `file_path` (str): Path to the input file.
        - `output_dir` (str): Path to the directory where OCR results will be saved.
    - **Example Usage**:
    ```python
    from ocr_tesseract import TesseractProcessor

    processor = TesseractProcessor(output_dir='/path/to/output')
    processor.process_file('/path/to/file.pdf')
    ```

- **`process_directory(input_path, depth=None)`**:
    - Processes files in a directory, using the file input handler to filter supported files.
    - **Parameters**:
        - `input_path` (str): Path to the input directory.
        - `depth` (int, optional): Limits directory traversal depth.
        - `output_dir` (str): Directory where the OCR results will be saved.
    - **Example Usage**:
    ```python
    from ocr_tesseract import TesseractProcessor

    processor = TesseractProcessor(output_dir='/path/to/output')
    processor.process_directory('/path/to/input', depth=2)
    ```

## Usage (Command Line)

You can run `ocr_tesseract.py` directly from the command line to process files or directories.

```bash
python ocr_tesseract.py [input_path] [--output output_dir] [--depth N] [--diagnostics]
```

### Command-Line Arguments

- **`input_path`**: Path to the input file or directory. If not specified, the current directory is used by default.
- **`--output`**: Path to the directory where OCR results will be saved. If not specified, it defaults to `ocr_output`.
- **`--filetypes`**: Path to a file defining supported file types (e.g., `filetypes.txt`). Defaults to `filetypes.txt`.
- **`--depth`**: Limit directory traversal to a specified depth. For example, `--depth 2` will traverse two levels deep.
- **`--diagnostics`**: Enables detailed logging and diagnostics for debugging purposes.

## Examples

### Process the current directory with default settings:

```bash
python ocr_tesseract.py
```

### Process a specific directory and save results to a custom output directory:

```bash
python ocr_tesseract.py /path/to/input --output /path/to/output
```

### Process a directory with depth limitation and diagnostics enabled:

```bash
python ocr_tesseract.py /path/to/input --depth 2 --diagnostics
```

### Process a specific file:

```bash
python ocr_tesseract.py /path/to/file.pdf
```

## How It Works

The script operates in several stages:

1. **File Input Handling**:
   - It accepts a single file or directory as input.
   - If a directory is provided, it traverses the directory (up to the specified depth) to locate files that match the supported file types.
   - Supported file types are defined in `filetypes.txt` (or a custom file), which typically includes formats like PDFs and common image types (e.g., PNG, JPG).

2. **PDF to Image Conversion**:
   - If the input is a PDF, the script converts each page of the PDF into an image using `pdf2image`.

3. **OCR Processing**:
   - For each image, the script runs Tesseract OCR to extract text.
   - The results are saved as `.txt` files in the specified output directory.

4. **Diagnostics**:
   - When the `--diagnostics` flag is enabled, the script provides detailed logging of the processing steps, including file discovery, PDF conversion, and OCR results.

## Integration

You can integrate `ocr_tesseract.py` into other Python projects by importing and using the `TesseractProcessor` class, or simply use it as a standalone script for batch OCR processing.

## Future Enhancements

Possible future improvements include:

- Adding image pre-processing (e.g., using OpenCV) to enhance OCR accuracy.