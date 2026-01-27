"""Quick test to check PaddleOCR extraction with minimal config"""
from PIL import Image
import sys

print("Testing PaddleOCR extraction (minimal config)...")

try:
    from paddleocr import PaddleOCR
    
    # Create reader with MINIMAL params
    print("Creating PaddleOCR reader...")
    reader = PaddleOCR(use_angle_cls=True, lang='en')
    
    # Test on image
    img_path = "img 1.jpeg"
    print(f"Testing OCR on: {img_path}")
    
    # Call ocr method
    results = reader.ocr(img_path)
    
    print(f"Results type: {type(results)}")
    
    if results and results[0]:
        print(f"Found {len(results[0])} text regions")
        for line in results[0][:3]:  # Show first 3 lines
            print(f"  Text: {line[1][0]}, Conf: {line[1][1]:.2f}")
        print("\n✅ PaddleOCR extraction works!")
    else:
        print("No results returned")
    
except Exception as e:
    print(f"\n❌ PaddleOCR error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
