
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import threading
import os
from datetime import datetime

# Import utilities
from utils.ocr_processor import OCRProcessor
from utils.docx_generator import DocxGenerator

class OCRDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Image to Word Converter")
        self.root.geometry("1100x700")
        
        # State variables
        self.ocr_processor = None
        self.current_image_path = None
        self.current_image = None
        self.extracted_data = None
        self.extracted_text = ""
        self.confidence_score = 0.0
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        
        # Initialize default OCR in background (use easyocr as default since tesseract requires separate installation)
        threading.Thread(target=self.init_ocr, args=('easyocr',), daemon=True).start()

    def create_widgets(self):
        # Main layout
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Panel (Controls & Image)
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Controls Group
        control_frame = ttk.LabelFrame(left_frame, text="Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # OCR Engine Selection
        ttk.Label(control_frame, text="OCR Engine:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.engine_var = tk.StringVar(value="easyocr")
        engine_combo = ttk.Combobox(control_frame, textvariable=self.engine_var, state="readonly")
        engine_combo['values'] = ('easyocr', 'paddleocr', 'tesseract')
        engine_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        engine_combo.bind('<<ComboboxSelected>>', self.on_engine_change)
        
        # Preprocessing Options
        self.preprocess_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="Enhanced Preprocessing (OpenCV)", variable=self.preprocess_var).grid(row=1, column=0, columnspan=2, padx=5, sticky=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Select Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        self.process_btn = ttk.Button(btn_frame, text="Extract Text", command=self.start_processing, state=tk.DISABLED)
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        # Image Preview
        self.img_frame = ttk.LabelFrame(left_frame, text="Image Preview")
        self.img_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.img_label = ttk.Label(self.img_frame, text="No image selected")
        self.img_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right Panel (Text & Output)
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # Text Preview
        text_frame = ttk.LabelFrame(right_frame, text="Extracted Text")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_area = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export Controls
        export_frame = ttk.Frame(right_frame)
        export_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(export_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        self.save_btn = ttk.Button(export_frame, text="Save as Word Document", command=self.save_document, state=tk.DISABLED)
        self.save_btn.pack(side=tk.RIGHT, pady=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(export_frame, mode='indeterminate')
        # Packed only when needed

    def on_engine_change(self, event):
        engine = self.engine_var.get()
        threading.Thread(target=self.init_ocr, args=(engine,), daemon=True).start()

    def init_ocr(self, engine):
        self.update_status(f"Initializing {engine}...")
        try:
            self.ocr_processor = OCRProcessor(engine=engine)
            self.ocr_processor.initialize_reader()
            self.update_status(f"{engine} initialized successfully.")
            self.root.after(0, lambda: self.process_btn.configure(state=tk.NORMAL if self.current_image else tk.DISABLED))
        except Exception as e:
            print(f"Failed to initialize {engine}: {e}")
            if engine != 'easyocr':
                print("Falling back to EasyOCR...")
                self.root.after(0, lambda: messagebox.showwarning("Initialization Error", f"Failed to initialize {engine}. Falling back to EasyOCR.\nError: {e}"))
                self.engine_var.set('easyocr')
                self.init_ocr('easyocr')
            else:
                self.update_status(f"Error initializing {engine}: {str(e)}")
                self.root.after(0, lambda: messagebox.showerror("Fatal Error", f"Could not initialize any OCR engine. Error: {str(e)}"))

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.current_image_path = file_path
            self.current_image = Image.open(file_path)
            
            # Resize for preview
            display_img = self.current_image.copy()
            display_img.thumbnail((500, 500))
            photo = ImageTk.PhotoImage(display_img)
            
            self.img_label.configure(image=photo, text="")
            self.img_label.image = photo  # Keep reference
            
            self.process_btn.configure(state=tk.NORMAL)
            self.status_label.configure(text=f"Loaded: {os.path.basename(file_path)}")

    def start_processing(self):
        if not self.current_image:
            return
            
        self.process_btn.configure(state=tk.DISABLED)
        self.save_btn.configure(state=tk.DISABLED)
        self.progress.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.progress.start(10)
        self.update_status("Processing image...")
        
        # Run in thread
        threading.Thread(target=self.process_image, daemon=True).start()

    def process_image(self):
        try:
            advanced_preprocess = self.preprocess_var.get()
            
            # If using tesseract, we get structured data
            if self.engine_var.get() == 'tesseract':
                self._process_tesseract(advanced_preprocess)
            else:
                # Other engines
                self._process_standard(advanced_preprocess)
                
            self.root.after(0, self.processing_complete)
            
        except Exception as e:
            # Capture e in default arg to avoid late binding issues
            error_msg = str(e)
            self.root.after(0, lambda msg=error_msg: self.processing_error(msg))

    def _process_tesseract(self, advanced_preprocess=True):
        """Handle Tesseract specific processing with fallback"""
        if self.ocr_processor.use_tesseract:
            try:
                self.extracted_data = self.ocr_processor.extract_text_with_formatting(self.current_image, advanced_preprocess=advanced_preprocess)
                self._flatten_structured_data()
                self.confidence_score = self.ocr_processor.get_confidence_score(self.current_image, advanced_preprocess=advanced_preprocess)
            except Exception as e:
                # Fallback to EasyOCR if Tesseract runtime fails
                print(f"Tesseract failed: {e}. Falling back to EasyOCR.")
                self.root.after(0, lambda: messagebox.showwarning("Tesseract Error", "Tesseract execution failed. Using EasyOCR as fallback."))
                self._fallback_to_easyocr(advanced_preprocess)
        else:
            # Tesseract not installed/found - use EasyOCR
            self.root.after(0, lambda: messagebox.showwarning(
                "Tesseract Not Found", 
                "Tesseract is not installed or not in PATH.\n\n"
                "Please download it from:\n"
                "https://github.com/UB-Mannheim/tesseract/wiki\n\n"
                "Using EasyOCR as fallback."
            ))
            self._fallback_to_easyocr(advanced_preprocess)

    def _fallback_to_easyocr(self, advanced_preprocess=True):
        """Fallback to EasyOCR when Tesseract is unavailable"""
        try:
            # Create a temporary EasyOCR processor for fallback
            fallback_processor = OCRProcessor(engine='easyocr')
            fallback_processor.initialize_reader()
            self.extracted_text = fallback_processor.extract_text(self.current_image, advanced_preprocess=advanced_preprocess)
            self.extracted_data = [{'text': self.extracted_text}]
            self.confidence_score = fallback_processor.get_confidence_score(self.current_image, advanced_preprocess=advanced_preprocess)
        except Exception as e:
            print(f"EasyOCR fallback also failed: {e}")
            self.extracted_text = ""
            self.extracted_data = [{'text': ''}]
            self.confidence_score = 0.0

    def _process_standard(self, advanced_preprocess=True):
        """Handle standard OCR processing"""
        self.extracted_text = self.ocr_processor.extract_text(self.current_image, advanced_preprocess=advanced_preprocess)
        self.extracted_data = [{'text': self.extracted_text}]
        self.confidence_score = self.ocr_processor.get_confidence_score(self.current_image, advanced_preprocess=advanced_preprocess)

    def _flatten_structured_data(self):
        """Convert structured data to plain text for display"""
        text_lines = []
        current_block = -1
        current_para = -1
        line_buffer = []
        
        for item in self.extracted_data:
            if item['block'] != current_block or item['para'] != current_para:
                if line_buffer:
                    text_lines.append(' '.join(line_buffer))
                    line_buffer = []
                current_block = item['block']
                current_para = item['para']
            line_buffer.append(item['text'])
        if line_buffer:
            text_lines.append(' '.join(line_buffer))
            
        self.extracted_text = '\n'.join(text_lines)

    def processing_complete(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.process_btn.configure(state=tk.NORMAL)
        self.save_btn.configure(state=tk.NORMAL)
        
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.extracted_text)
        
        if self.extracted_text:
            score_display = f"{self.confidence_score*100:.1f}%"
        else:
            score_display = "N/A"
            
        self.update_status(f"Extraction complete (Confidence: {score_display})")

    def processing_error(self, error_msg):
        self.progress.stop()
        self.progress.pack_forget()
        self.process_btn.configure(state=tk.NORMAL)
        self.update_status(f"Error: {error_msg}")
        messagebox.showerror("Processing Error", error_msg)

    def save_document(self):
        if not self.extracted_data:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Document", "*.docx")]
        )
        
        if file_path:
            try:
                generator = DocxGenerator()
                if self.engine_var.get() == 'tesseract' and self.ocr_processor.use_tesseract:
                     generator.create_formatted_document(
                         self.extracted_data, 
                         confidence_score=self.confidence_score
                     )
                else:
                    generator.create_document_with_sections(
                        self.extracted_text, 
                        confidence_score=self.confidence_score
                    )
                    
                generator.save_to_file(file_path)
                messagebox.showinfo("Success", f"Document saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def update_status(self, text):
        self.status_label.configure(text=text)

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRDesktopApp(root)
    root.mainloop()
