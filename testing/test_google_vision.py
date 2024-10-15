import os
import json
from google.cloud import secretmanager
from google.oauth2 import service_account
from google.cloud import vision

# Replace with your project ID and secret name
PROJECT_ID = "multiocr-project"
SECRET_NAME = "MultiOCR-service-account-key"

def get_service_account_key_from_secret_manager():
    """
    Retrieves the service account key JSON from Google Secret Manager
    """
    client = secretmanager.SecretManagerServiceClient()

    # Access the latest version of the secret
    secret_name = f"projects/{PROJECT_ID}/secrets/{SECRET_NAME}/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})

    # Extract the secret payload (service account JSON key)
    secret_payload = response.payload.data.decode("UTF-8")

    # Parse the JSON key into a dictionary
    service_account_info = json.loads(secret_payload)
    
    return service_account_info

def setup_google_vision_client():
    """
    Set up Google Vision client using the service account retrieved from Secret Manager
    """
    # Retrieve the service account key from Secret Manager
    service_account_info = get_service_account_key_from_secret_manager()

    # Authenticate using the retrieved service account key
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    # Create a Vision API client using the credentials
    vision_client = vision.ImageAnnotatorClient(credentials=credentials)
    
    return vision_client

def main():
    # Set up the Google Vision client
    vision_client = setup_google_vision_client()

    # Load an image and perform OCR
    file_name = '/Users/alex/git/MultiOCR/testing/sample.pdf'
    with open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform text detection
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        print('Detected text:')
        print(texts[0].description)
    else:
        print('No text detected')

if __name__ == "__main__":
    main()
