
# MultiOCR

MultiOCR is a multi-OCR system that combines Tesseract, Apple's Vision framework, and Google Cloud Vision API to improve text extraction accuracy from scanned PDF documents. By using multiple OCR engines and comparing their results, MultiOCR ensures the most reliable recognition of text, ideal for processing invoices, statements, and other scanned files.

## Features
- Utilizes **Tesseract**, **Apple's Vision framework**, and **Google Cloud Vision API** for robust text recognition.
- Implements a comparison algorithm to combine results and resolve discrepancies.
- Enhances OCR accuracy through pre-processing and multi-system voting.
- Suitable for automating document processing with high precision.

## Current Progress
- **File Input Handling**: The system can now accept files or directories as input, filter based on supported file types, and limit directory traversal depth using the `--depth` flag.
- **Diagnostics Mode**: The `--diagnostics` flag has been added to provide detailed debugging information, including file and directory checks during the processing.
- **Supported File Types**: File types are now defined in `filetypes.txt` or `filetypes.json`, allowing flexible control over which file formats to process (PDF, PNG, JPG, etc.).
- **Depth Limitation**: Users can now specify how deep the script will search directories for files using the `--depth` flag.

## Installation

### Requirements
- Python 3.x
- Tesseract OCR (optional for OCR processing)
- OpenCV (optional for image pre-processing)
- Google Cloud Vision API credentials (for multi-system OCR)
- `pytesseract`, `pdf2image`, `google-cloud-vision`

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MultiOCR.git
   cd MultiOCR
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Google Cloud Vision API:
   - Follow [Google's guide](https://cloud.google.com/vision/docs/setup) to set up your API key.

4. Run the sample OCR processing:
   ```bash
   python main.py path_to_your_pdf.pdf
   ```

## Usage

### File Search with Depth Limitation:
- To search the current directory only:
  ```bash
  python get_input.py --depth 0
  ```

- To search the current directory and one level of subdirectories:
  ```bash
  python get_input.py --depth 1
  ```

### Diagnostics Mode:
- Enable diagnostics mode to show detailed information about file checking:
  ```bash
  python get_input.py --depth 1 --diagnostics
  ```

## License
This project is licensed under the **CC0 1.0 Universal (CC0 1.0) Public Domain Dedication**. See the [LICENSE](LICENSE) file for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

### Disclaimer
This project is in active development and subject to change as we add more features and refine the OCR comparison process.
