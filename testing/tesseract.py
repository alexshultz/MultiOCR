import pytesseract
from pdf2image import convert_from_path

def pdf_to_images(pdf_path):
    # Convert PDF to a list of images (each page becomes an image)
    images = convert_from_path(pdf_path)
    return images

def extract_text_from_images(images):
    # Extract text from each image using Tesseract OCR
    text = ""
    for image in images:
        page_text = pytesseract.image_to_string(image)
        text += page_text + "\n\n"  # Add a separator between pages
    return text

def process_pdf_with_tesseract(pdf_path):
    # Convert the PDF to images
    images = pdf_to_images(pdf_path)
    
    # Extract text from those images
    extracted_text = extract_text_from_images(images)
    
    return extracted_text

# Example usage
pdf_path = 'path_to_your_pdf.pdf'
text_output = process_pdf_with_tesseract(pdf_path)

# You can print or save the text
print(text_output)
