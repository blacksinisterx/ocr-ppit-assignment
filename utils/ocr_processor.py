"""
OCR Processor Module
Handles image-to-text extraction using multiple OCR engines
Supports: EasyOCR, PaddleOCR, and TrOCR (Microsoft's handwriting model)
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io

try:
    import cv2
except ImportError:
    cv2 = None

# Fix for PaddleOCR crash on some Windows systems (fused_conv2d error)
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['FLAGS_enable_mkldnn'] = '0'

try:
    import pytesseract
except ImportError:
    pytesseract = None



class OCRProcessor:
    """Handle OCR operations for image-to-text conversion"""
    
    def __init__(self, engine='easyocr', languages=['en'], gpu=False):
        """
        Initialize OCR processor
        
        Args:
            engine: OCR engine to use ('easyocr', 'paddleocr', 'trocr')
            languages: List of language codes (default: ['en'])
            gpu: Use GPU acceleration if available (default: False)
        """
        self.reader = None
        self.engine = engine
        self.languages = languages
        self.gpu = gpu
        self.processor = None  # For TrOCR
        self.use_tesseract = False
        
        # Check if Tesseract is available
        if pytesseract:
            # Smart Tesseract Path Auto-detection
            tesseract_in_path = False
            try:
                # Actual check if binary is available/callable
                pytesseract.get_tesseract_version()
                tesseract_in_path = True
            except Exception:
                pass
                
            if not tesseract_in_path:
                import os
                common_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                    os.path.expanduser(r'~\AppData\Local\Tesseract-OCR\tesseract.exe')
                ]
                for path in common_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        tesseract_in_path = True
                        break
            
            self.use_tesseract = tesseract_in_path
    
    def initialize_reader(self):
        """
        Initialize the selected OCR reader (downloads models on first run)
        This is separated from __init__ to show progress to user
        """
        if self.reader is None:
            if self.engine == 'easyocr':
                import easyocr
                self.reader = easyocr.Reader(self.languages, gpu=self.gpu)
            
            elif self.engine == 'paddleocr':
                try:
                    from paddleocr import PaddleOCR
                    import logging
                    # Suppress Paddle logging
                    logging.getLogger('ppocr').setLevel(logging.ERROR)
                    
                    lang = self.languages[0] if self.languages else 'en'
                    self.reader = PaddleOCR(
                        use_angle_cls=True, 
                        lang=lang
                        # Removed extra params (det_db_box_thresh, det_db_unclip_ratio) due to internal Paddle errors
                    )
                except Exception as e:
                    print(f"PaddleOCR failed to initialize: {e}")
                    self.reader = None
                    # We might want to switch engine here or handle in caller
                    raise ImportError(f"PaddleOCR init failed: {e}")
            
            elif self.engine == 'trocr':
                from transformers import TrOCRProcessor, VisionEncoderDecoderModel
                import easyocr
                # TrOCR for handwriting + EasyOCR for text detection
                self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
                self.reader = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
                self.detector = easyocr.Reader(['en'], gpu=self.gpu)
                if self.gpu:
                    self.reader = self.reader.to('cuda')
        
        return self.reader
    
    def preprocess_image(self, image, enhance=True, advanced=True):
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image: PIL Image object
            enhance: Whether to apply basic enhancement (default: True)
            advanced: Whether to use advanced OpenCV preprocessing (default: True)
            
        Returns:
            numpy array of processed image
        """
        # Convert PIL to numpy if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image.convert('RGB'))
        else:
            img_array = image
            
        if advanced and cv2 is not None:
            # Convert to grayscale
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Apply Gaussian Blur to remove noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Adaptive Thresholding to binarize
            # This handles varying lighting conditions better than global threshold
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
            
            # Convert back to RGB format for consistency
            processed_img = cv2.cvtColor(denoised, cv2.COLOR_GRAY2RGB)
            return processed_img
            
        # Fallback to basic PIL enhancement if OpenCV not available or advanced=False
        if isinstance(image, np.ndarray):
            pil_image = Image.fromarray(image)
        else:
            pil_image = image
            
        # Convert to RGB if needed
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Optional enhancement for better OCR
        if enhance:
            # Increase contrast
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.5)
            
            # Increase sharpness
            enhancer = ImageEnhance.Sharpness(pil_image)
            pil_image = enhancer.enhance(1.3)
        
        # Convert PIL Image to numpy array
        img_array = np.array(pil_image)
        
        return img_array
    
    def extract_text(self, image, detail=0, advanced_preprocess=True):
        """
        Extract text from image using selected OCR engine
        
        Args:
            image: PIL Image object or file path
            detail: 0 = text only, 1 = text with confidence, 2 = full details
            advanced_preprocess: Whether to use advanced OpenCV preprocessing
            
        Returns:
            Extracted text as string or detailed results
        """
        # Ensure reader is initialized
        if self.reader is None:
            self.initialize_reader()
        
        # Handle PIL Image
        if isinstance(image, Image.Image):
            img_array = self.preprocess_image(image, advanced=advanced_preprocess)
            pil_image = image
        else:
            img_array = image
            pil_image = Image.fromarray(image) if isinstance(image, np.ndarray) else Image.open(image)
        
        # Perform OCR based on engine
        if self.engine == 'easyocr':
            results = self.reader.readtext(img_array)
            
            if detail == 0:
                text = '\n'.join([item[1] for item in results])
                return text
            elif detail == 1:
                return [(item[1], item[2]) for item in results]
            else:
                return results
        
        elif self.engine == 'paddleocr':
            results = self.reader.ocr(img_array)
            
            if not results or not results[0]:
                return "" if detail == 0 else []
            
            if detail == 0:
                text_lines = [line[1][0] for line in results[0] if line and len(line) > 1]
                text = '\n'.join(text_lines)
                return text
            elif detail == 1:
                return [(line[1][0], line[1][1]) for line in results[0] if line and len(line) > 1]
            else:
                return results
        
        elif self.engine == 'trocr':
            # Use EasyOCR to detect text regions, TrOCR to recognize
            return self._extract_with_trocr(pil_image, img_array)
            
        elif self.engine == 'tesseract':
            if pytesseract:
                try:
                    return pytesseract.image_to_string(pil_image).strip()
                except Exception as e:
                    # print(f"Tesseract simple extraction failed: {e}")
                    return ""
            else:
                return ""
        
        return ""
    
    def _extract_with_trocr(self, pil_image, img_array):
        """Extract text using TrOCR with EasyOCR for detection"""
        import torch
        
        # Detect text regions using EasyOCR
        detections = self.detector.readtext(img_array)
        
        if not detections:
            return ""
        
        # Sort by vertical position
        sorted_detections = sorted(detections, key=lambda x: x[0][0][1])
        
        recognized_texts = []
        for bbox, _, _ in sorted_detections:
            # Extract region
            x_coords = [point[0] for point in bbox]
            y_coords = [point[1] for point in bbox]
            x1, x2 = int(min(x_coords)), int(max(x_coords))
            y1, y2 = int(min(y_coords)), int(max(y_coords))
            
            # Crop region
            cropped = pil_image.crop((x1, y1, x2, y2))
            
            # Recognize with TrOCR
            pixel_values = self.processor(cropped, return_tensors="pt").pixel_values
            if self.gpu:
                pixel_values = pixel_values.to('cuda')
            
            generated_ids = self.reader.generate(pixel_values)
            text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            recognized_texts.append(text)
        
        return '\n'.join(recognized_texts)
    
    def extract_text_with_structure(self, image):
        """
        Extract text while attempting to preserve document structure
        Groups text by vertical position to maintain paragraph structure
        
        Args:
            image: PIL Image object
            
        Returns:
            Text string with attempted paragraph preservation
        """
        if self.reader is None:
            self.initialize_reader()
        
        img_array = self.preprocess_image(image)
        
        # Get results based on engine
        if self.engine == 'easyocr':
            results = self.reader.readtext(img_array)
            if not results:
                return ""
            sorted_results = sorted(results, key=lambda x: x[0][0][1])
            text_items = [(bbox, text, conf) for bbox, text, conf in sorted_results]
        
        elif self.engine == 'paddleocr':
            results = self.reader.ocr(img_array)
            if not results or not results[0]:
                return ""
            sorted_results = sorted(results[0], key=lambda x: x[0][0][1] if x and len(x) > 0 else 0)
            text_items = [(line[0], line[1][0], line[1][1]) for line in sorted_results if line and len(line) > 1]
        
        else:
            return ""
        
        # Group text by approximate line (with some tolerance)
        lines = []
        current_line = []
        current_y = None
        y_threshold = 20  # pixels tolerance for same line
        
        for bbox, text, conf in text_items:
            # Get center y-coordinate
            if isinstance(bbox, (list, tuple)) and len(bbox) >= 2:
                y_coord = (bbox[0][1] + bbox[2][1]) / 2
            else:
                continue
            
            if current_y is None or abs(y_coord - current_y) < y_threshold:
                # Same line
                current_line.append(text)
                current_y = y_coord if current_y is None else current_y
            else:
                # New line
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [text]
                current_y = y_coord
        
        # Add last line
        if current_line:
            lines.append(' '.join(current_line))
        
        # Join lines with newlines
        return '\n'.join(lines)
    
    def get_confidence_score(self, image, advanced_preprocess=True):
        """
        Get average confidence score for OCR results
        
        Args:
            image: PIL Image object
            advanced_preprocess: Whether to use advanced OpenCV preprocessing
            
        Returns:
            Average confidence score (0-1)
        """
        if self.reader is None and self.engine != 'tesseract':
            self.initialize_reader()
        
        # TrOCR doesn't provide confidence scores
        img_array = self.preprocess_image(image, advanced=advanced_preprocess)
        
        if self.engine == 'easyocr':
            results = self.reader.readtext(img_array)
            if not results:
                return 0.0
            confidences = [item[2] for item in results]
            return sum(confidences) / len(confidences)
        
        elif self.engine == 'paddleocr':
            results = self.reader.ocr(img_array)
            if not results or not results[0]:
                return 0.0
            confidences = [line[1][1] for line in results[0] if line and len(line) > 1]
            if not confidences:
                return 0.0
        
        elif self.engine == 'tesseract' and pytesseract:
             try:
                data = pytesseract.image_to_data(img_array, output_type=pytesseract.Output.DICT)
                confidences = [float(conf) for conf in data['conf'] if conf != '-1']
                if not confidences:
                    return 0.0
                return sum(confidences) / len(confidences) / 100.0
             except:
                 return 0.0
                 
        return 0.0

    def extract_text_with_formatting(self, image, advanced_preprocess=True):
        """
        Extract text with formatting attributes using Tesseract
        
        Args:
            image: PIL Image object
            advanced_preprocess: Whether to use advanced OpenCV preprocessing
            
        Returns:
            List of dictionaries containing text and formatting data
            or raw text if Tesseract unavailable
        """
        if not pytesseract:
            return [{'text': self.extract_text(image, advanced_preprocess=advanced_preprocess), 'bold': False, 'italic': False, 'paragraph': 0}]
            
        img_array = self.preprocess_image(image, advanced=advanced_preprocess)
        
        try:
            # Get verbose data including boxes, confidences, line and page numbers
            data = pytesseract.image_to_data(img_array, output_type=pytesseract.Output.DICT)
            
            structured_data = []
            curr_paragraph = 0
            
            # Tesseract structure:
            # level: 1=page, 2=block, 3=para, 4=line, 5=word
            
            n_boxes = len(data['level'])
            for i in range(n_boxes):
                if data['level'][i] == 5:  # Word level
                    text = data['text'][i].strip()
                    if not text:
                        continue
                        
                    # Basic font checks (Tesseract doesn't give bold/italic directly in standard mode
                    # without hOCR, but we can infer some things or use osd)
                    # For now, we'll store the structural info which is most reliable
                    
                    structured_data.append({
                        'text': text,
                        'block': data['block_num'][i],
                        'para': data['par_num'][i],
                        'line': data['line_num'][i],
                        'left': data['left'][i],
                        'top': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i],
                        'conf': data['conf'][i]
                    })
            
            return structured_data
            
        except Exception as e:
            # print(f"Tesseract extraction failed: {e}") # Suppress noise
            return [{'text': self.extract_text(image, advanced_preprocess=advanced_preprocess), 'bold': False, 'italic': False, 'paragraph': 0}]

