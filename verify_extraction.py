
import os
import sys
from utils.ocr_processor import OCRProcessor
from PIL import Image

def test_engine(engine_name, image_path):
    print(f"\n--- Testing {engine_name} ---")
    try:
        processor = OCRProcessor(engine=engine_name)
        processor.initialize_reader()
        if engine_name == 'tesseract':
            # Force check
            import pytesseract
            print(f"Tesseract version: {pytesseract.get_tesseract_version()}")
            
        img = Image.open(image_path)
        text = processor.extract_text(img)
        print(f"[{engine_name}] Output len: {len(text)}")
        print(f"[{engine_name}] Sample: {text[:100]}...")
    except Exception as e:
        print(f"[{engine_name}] Failed: {e}")

if __name__ == "__main__":
    img_path = "img 1.jpeg"
    if not os.path.exists(img_path):
        print(f"Image not found: {img_path}")
    else:
        test_engine('tesseract', img_path)
        test_engine('paddleocr', img_path)
        test_engine('easyocr', img_path)
