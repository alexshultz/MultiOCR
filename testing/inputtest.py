import fitz  # PyMuPDF

def extract_text_from_pdf_or_image(file_path):
    try:
        doc = fitz.open(file_path)  # Open the document (PDF or image)
        
        # Check if it's a PDF or an image
        if doc.is_pdf:
            print(f"Processing PDF: {file_path}")
            text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)  # Load each page
                text += page.get_text()  # Extract text from page
            return text
        else:
            print(f"Processing Image: {file_path}")
            # Extract text from the image if it's an image
            pix = doc.get_page_pixmap(0)
            return pix
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Example usage:
file_path = "/Users/alex/Documents/github/MultiOCR/sample.pdf"  # Replace with your file
text_or_image = extract_text_from_pdf_or_image(file_path)
if isinstance(text_or_image, str):
    print("Extracted text:", text_or_image)
else:
    print("Extracted image information.")
