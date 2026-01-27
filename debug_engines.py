
import os
import sys
from PIL import Image
import numpy as np

# Mocking the utils import to ensure we can run this standalone or pointing to the right path
sys.path.append(os.getcwd())

try:
    from utils.ocr_processor import OCRProcessor
except ImportError as e:
    print(f"Error importing OCRProcessor: {e}")
    sys.exit(1)

def create_dumb_image():
    # Create a simple image with text "Hello World"
    # Since we can't easily draw text without opencv or pil font which might be missing/complex
    # We'll just create a white image. The OCR won't find text but it shouldn't CRASH.
    img = Image.new('RGB', (200, 100), color = (255, 255, 255))
    return img

def test_tesseract():
    print("\n--- Testing Tesseract ---")
    try:
        import pytesseract
        print(f"pytesseract version: {pytesseract.get_tesseract_version()}")
    except Exception as e:
        print(f"pytesseract check failed: {e}")
        
    processor = OCRProcessor(engine='tesseract')
    img = create_dumb_image()
    try:
        result = processor.extract_text(img)
        print(f"Tesseract simple extraction result: '{result}'")
    except Exception as e:
        print(f"Tesseract simple extraction CRASHED: {e}")

    try:
        result = processor.extract_text_with_formatting(img)
        print(f"Tesseract formatted extraction result: {result}")
    except Exception as e:
        print(f"Tesseract formatted extraction CRASHED: {e}")

def test_paddle():
    print("\n--- Testing PaddleOCR ---")
    try:
        import paddle
        print(f"paddle version: {paddle.__version__}")
        import paddleocr
        print(f"paddleocr version: {paddleocr.__version__}")
    except Exception as e:
        print(f"Paddle import failed: {e}")

    # Use 'en' model
    try:
        print("Initializing PaddleOCR...")
        processor = OCRProcessor(engine='paddleocr')
        processor.initialize_reader()
        print("PaddleOCR Initialized.")
        
        img = create_dumb_image()
        result = processor.extract_text(img)
        print(f"PaddleOCR extraction result: '{result}'")
    except Exception as e:
        print(f"PaddleOCR CRASHED: {e}")

if __name__ == "__main__":
    print(f"Python: {sys.version}")
    test_tesseract()
    test_paddle()
