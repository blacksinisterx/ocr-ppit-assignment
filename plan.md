# Plan: Image-to-Word OCR App

## Objective
Build a simple Streamlit web app that converts images (typed text and handwritten notes) into editable Word (.docx) documents using free AI-powered OCR.

## Deliverables
- Streamlit web application with image upload functionality
- OCR processing using free AI service (EasyOCR or Azure Computer Vision free tier)
- Word document generation with extracted text
- Download functionality for generated .docx files

## Acceptance Criteria
- ✅ User can upload image files (JPG, PNG, JPEG)
- ✅ App processes images and extracts text using OCR
- ✅ Works reasonably well with both printed and handwritten text
- ✅ Generated Word document is editable and downloadable
- ✅ Simple, clean UI that's easy to understand
- ✅ Entire implementation takes 2-3 hours maximum
- ✅ Uses only free tools/services (no paid API keys required)

## Technology Stack

### Core Components
1. **Streamlit** - Web framework (free, easy to use)
2. **EasyOCR** - OCR engine (free, supports 80+ languages, handles handwriting)
   - Alternative: PaddleOCR (also free, good with handwriting)
3. **python-docx** - Word document generation
4. **Pillow (PIL)** - Image processing

### Why EasyOCR?
- ✅ Completely free and open-source
- ✅ No API keys or registration needed
- ✅ Works offline
- ✅ Good accuracy with handwritten text
- ✅ Supports multiple languages
- ✅ Easy to implement

## Implementation Steps

### Phase 1: Environment Setup (15-20 mins)
- [ ] Create project directory structure
- [ ] Create requirements.txt with dependencies
- [ ] Set up virtual environment
- [ ] Install required packages

### Phase 2: Basic Streamlit App Structure (20-25 mins)
- [ ] Create main app.py file
- [ ] Set up Streamlit page configuration
- [ ] Add title, description, and instructions
- [ ] Implement file uploader widget
- [ ] Add basic UI elements (buttons, status messages)

### Phase 3: OCR Integration (30-40 mins)
- [ ] Initialize EasyOCR reader
- [ ] Create function to process uploaded images
- [ ] Extract text from images using OCR
- [ ] Handle different image formats and sizes
- [ ] Add progress indicators for processing

### Phase 4: Word Document Generation (25-30 mins)
- [ ] Create function to generate .docx files
- [ ] Format extracted text properly (preserve paragraphs)
- [ ] Add metadata (creation date, source info)
- [ ] Implement download functionality

### Phase 5: UI/UX Improvements (15-20 mins)
- [ ] Add image preview before processing
- [ ] Show extracted text preview in app
- [ ] Add error handling and user-friendly messages
- [ ] Add processing time display
- [ ] Polish layout and styling

### Phase 6: Testing & Refinement (15-20 mins)
- [ ] Test with printed text images
- [ ] Test with handwritten notes
- [ ] Test with different image qualities
- [ ] Fix any bugs or issues
- [ ] Add usage instructions

**Total Estimated Time: 2-3 hours**

## Files Structure
```
Tasks/
├── plan.md (this file)
├── app.py (main Streamlit app)
├── requirements.txt (Python dependencies)
├── README.md (usage instructions)
└── utils/
    ├── ocr_processor.py (OCR logic)
    └── docx_generator.py (Word doc creation)
```

## Edge Cases & Constraints

### Constraints
- First run will download EasyOCR models (~100-200MB) - warn user
- Processing time depends on image size and complexity (5-30 seconds)
- Handwriting accuracy depends on legibility
- Works best with clear, well-lit images

### Edge Cases
- Very large images (handle with resizing)
- Multiple columns or complex layouts (may need preprocessing)
- Mixed languages (EasyOCR supports this)
- Poor image quality (add preprocessing: contrast enhancement, noise reduction)
- Empty or non-text images (add validation)

## Manual QA / Verification Steps

### Smoke Checks
1. **App Launches Successfully**
   - Run: `streamlit run app.py`
   - Verify: App opens in browser without errors
   - Expected: Clean UI with upload button visible

2. **Package Installation**
   - Run: `pip install -r requirements.txt`
   - Verify: All packages install without conflicts
   - Expected: EasyOCR and dependencies installed (~500MB total)

### Acceptance Flow Testing
3. **Test with Printed Text Image**
   - Upload a screenshot or typed document image
   - Click "Extract Text" button
   - Verify: Text is extracted accurately (>95% accuracy)
   - Download Word document
   - Open in Word/LibreOffice and verify text is editable

4. **Test with Handwritten Notes**
   - Upload one of the provided handwritten chemistry notes
   - Process the image
   - Verify: Most text is recognizable (>70% accuracy for clear handwriting)
   - Check Word document for formatting

5. **Test Multiple Uploads**
   - Upload and process 3 different images in sequence
   - Verify: Each generates separate Word documents
   - Check: No memory leaks or slowdowns

### Edge Case Checks
6. **Invalid File Types**
   - Try uploading .pdf, .txt, or .docx
   - Verify: App shows appropriate error message
   - Expected: "Please upload JPG, PNG, or JPEG images only"

7. **Large Images**
   - Upload a 10MB+ high-resolution image
   - Verify: App handles it without crashing
   - Check: Processing completes within reasonable time (<60 seconds)

8. **Empty/Blank Images**
   - Upload a blank white image
   - Verify: App handles gracefully
   - Expected: "No text detected" message or empty document

### Performance Checks
9. **Processing Time**
   - Record time for small (< 1MB) image: Expected <10 seconds
   - Record time for large (> 5MB) image: Expected <30 seconds
   - Display these times in the app

10. **First-Time Model Download**
    - Run on fresh environment
    - Verify: Clear message about downloading models
    - Monitor: Download progress visible to user

### Quality Checks
11. **Text Formatting in Word**
    - Open generated .docx in Microsoft Word
    - Verify: Text is properly paragraphed
    - Check: Font is readable (default Times New Roman or Arial)
    - Ensure: No corrupt or unreadable characters

12. **Multiple Language Support** (Optional)
    - Test with image containing non-English text if needed
    - Verify: EasyOCR detects language automatically

## Notes / Decisions

### Why Streamlit?
- Zero HTML/CSS/JavaScript knowledge needed
- Built-in file upload and download widgets
- Rapid prototyping (2-3 hours realistic)
- Free deployment options (Streamlit Cloud)

### Why EasyOCR over alternatives?
- **vs Tesseract**: Better handwriting recognition, easier setup
- **vs Google Vision API**: No API key needed, no usage limits
- **vs Azure**: No registration, works offline
- **vs PaddleOCR**: Slightly easier to use, better documentation

### Processing Flow
```
Upload Image → Display Preview → Run EasyOCR → 
Extract Text → Format Text → Generate .docx → 
Show Preview → Download Button
```

### Optional Enhancements (If Time Permits)
- Image preprocessing (auto-contrast, deskew)
- Batch processing (multiple images at once)
- Language selection dropdown
- Confidence score display
- Side-by-side comparison (image vs extracted text)

## Rollback Plan
- If EasyOCR is too slow or inaccurate: Switch to PaddleOCR
- If model download fails: Add clear instructions for manual download
- If Word generation fails: Fall back to .txt file output
- If Streamlit deployment fails: Provide localhost-only instructions

## Success Metrics
- ✅ App runs locally without errors
- ✅ Can process the provided handwritten notes
- ✅ Generated Word documents are editable
- ✅ Total development time < 3 hours
- ✅ No paid services required
