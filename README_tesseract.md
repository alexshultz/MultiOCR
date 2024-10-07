
# Tesseract Processor

The `tesseract.py` script is responsible for processing files using Tesseract OCR. It handles input files or directories, converts PDFs to images if needed, and runs OCR on the images to extract text. The results are saved as text files.

## Features

- Processes individual files or directories.
- Converts PDF files into images for OCR processing.
- Runs Tesseract OCR on supported image formats (e.g., PNG, JPEG).
- Provides command-line options to control output directories, depth of directory traversal, and diagnostics.

## Usage

You can run `tesseract.py` directly from the command line to process files or directories.

```bash
python tesseract.py [input_path] [--output output_dir] [--depth N] [--diagnostics]
```

### Command-Line Arguments

- **`input_path`**: Path to the input file or directory. If not specified, the current directory is used by default.
- **`--output`**: Path to the directory where OCR results will be saved. If not specified, it defaults to `ocr_output`.
- **`--filetypes`**: Path to a file defining supported file types (e.g., `filetypes.txt`). Defaults to `filetypes.txt`.
- **`--depth`**: Limit directory traversal to a specified depth. For example, `--depth 2` will traverse two levels deep.
- **`--diagnostics`**: Enables detailed logging and diagnostics for debugging purposes.

## Programmatic Usage

The functions in `tesseract.py` can also be called programmatically from other Python scripts. This is useful if you want to integrate OCR processing into a larger workflow or another project.

### Available Functions:

- **`process_file_with_tesseract(file_path, output_dir)`**: 
    - Processes an individual file using Tesseract. If the file is a PDF, it converts the PDF to images before processing.
    - **Parameters**:
        - `file_path` (str): Path to the input file.
        - `output_dir` (str): Path to the directory where OCR results will be saved.
    - **Example Usage**:
    ```python
    from tesseract import process_file_with_tesseract

    process_file_with_tesseract('/path/to/file.pdf', '/path/to/output')
    ```

- **`prepare_and_process_files(output_dir, input_path, depth=None, diagnostics=False)`**:
    - Processes files in a directory or a single file. Uses the `file_input_handler.py` module to traverse directories and apply OCR to all supported files.
    - **Parameters**:
        - `output_dir` (str): Directory where the OCR results will be saved.
        - `input_path` (str): Directory or file to process.
        - `depth` (int, optional): Limit directory traversal depth.
        - `diagnostics` (bool, optional): Enable detailed logging.
    - **Example Usage**:
    ```python
    from tesseract import prepare_and_process_files

    prepare_and_process_files('/path/to/output', '/path/to/input', depth=2, diagnostics=True)
    ```

## Examples

### Process the current directory with default settings:

```bash
python tesseract.py
```

### Process a specific directory and save results to a custom output directory:

```bash
python tesseract.py /path/to/input --output /path/to/output
```

### Process a directory with depth limitation and diagnostics enabled:

```bash
python tesseract.py /path/to/input --depth 2 --diagnostics
```

### Process a specific file:

```bash
python tesseract.py /path/to/file.pdf
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

You can integrate `tesseract.py` into other Python projects by importing and using it programmatically, or simply use it as a standalone script for batch OCR processing.

## Future Enhancements

Possible future improvements include:

- Adding image pre-processing (e.g., using OpenCV) to enhance OCR accuracy.
- Supporting additional OCR engines for multi-system comparison.
