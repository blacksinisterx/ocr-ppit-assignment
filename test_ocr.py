
import os
import sys
from PIL import Image

# Ensure we can import from utils
sys.path.append(os.getcwd())

from utils.ocr_processor import OCRProcessor
from utils.docx_generator import DocxGenerator

def test_ocr():
    print("Testing OCRProcessor...")
    processor = OCRProcessor(engine='tesseract')
    
    # Check if Tesseract is detected
    print(f"Proprietary Tesseract use_tesseract flag: {processor.use_tesseract}")
    
    # Test with a dummy image (create one)
    img = Image.new('RGB', (100, 100), color = 'white')
    
    # Test extract_text_with_formatting (should fallback safely)
    print("Testing extract_text_with_formatting...")
    data = processor.extract_text_with_formatting(img)
    print(f"Result type: {type(data)}")
    print(f"Result content: {data}")
    
    # Test preprocessing
    print("Testing preprocessing...")
    processed = processor.preprocess_image(img, advanced=True)
    print(f"Processed image shape: {processed.shape}")

    print("\nTesting DocxGenerator...")
    generator = DocxGenerator()
    
    # Test create_formatted_document with fallback data
    print("Testing create_formatted_document...")
    doc = generator.create_formatted_document(data, title="Test Doc")
    print("Document created successfully.")
    
    output_path = "test_output.docx"
    generator.save_to_file(output_path)
    print(f"Saved to {output_path}")
    
    if os.path.exists(output_path):
        print("Verification Successful: File exists.")
        os.remove(output_path)
    else:
        print("Verification Failed: File not found.")

if __name__ == "__main__":
    test_ocr()
