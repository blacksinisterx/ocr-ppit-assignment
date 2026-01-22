"""
OCR Processor Module
Handles image-to-text extraction using multiple OCR engines
Supports: EasyOCR, PaddleOCR, and TrOCR (Microsoft's handwriting model)
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io


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
                from paddleocr import PaddleOCR
                lang = self.languages[0] if self.languages else 'en'
                self.reader = PaddleOCR(
                    use_angle_cls=True, 
                    lang=lang, 
                    use_gpu=self.gpu, 
                    show_log=False,
                    det_db_box_thresh=0.3,
                    det_db_unclip_ratio=2.0
                )
            
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
    
    def preprocess_image(self, image, enhance=True):
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image: PIL Image object
            enhance: Whether to apply enhancement (default: True)
            
        Returns:
            numpy array of processed image
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Optional enhancement for better OCR
        if enhance:
            # Increase contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Increase sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.3)
        
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        return img_array
    
    def extract_text(self, image, detail=0):
        """
        Extract text from image using selected OCR engine
        
        Args:
            image: PIL Image object or file path
            detail: 0 = text only, 1 = text with confidence, 2 = full details
            
        Returns:
            Extracted text as string or detailed results
        """
        # Ensure reader is initialized
        if self.reader is None:
            self.initialize_reader()
        
        # Handle PIL Image
        if isinstance(image, Image.Image):
            img_array = self.preprocess_image(image)
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
            results = self.reader.ocr(img_array, cls=True)
            
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
            results = self.reader.ocr(img_array, cls=True)
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
    
    def get_confidence_score(self, image):
        """
        Get average confidence score for OCR results
        
        Args:
            image: PIL Image object
            
        Returns:
            Average confidence score (0-1)
        """
        if self.reader is None:
            self.initialize_reader()
        
        # TrOCR doesn't provide confidence scores
        img_array = self.preprocess_image(image)
        
        if self.engine == 'easyocr':
            results = self.reader.readtext(img_array)
            if not results:
                return 0.0
            confidences = [item[2] for item in results]
            return sum(confidences) / len(confidences)
        
        elif self.engine == 'paddleocr':
            results = self.reader.ocr(img_array, cls=True)
            if not results or not results[0]:
                return 0.0
            confidences = [line[1][1] for line in results[0] if line and len(line) > 1]
            if not confidences:
                return 0.0
        
        return 0.0
