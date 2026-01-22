# 📄 OCR Image to Word App

A powerful web application that converts images (including handwritten notes) into editable Word documents using AI-powered OCR technology.

## ✨ Features

- 🖼️ **Image Upload**: Support for JPG, PNG, JPEG formats
- 🤖 **Multiple OCR Engines**: 
  - **EasyOCR** - Stable and reliable for general use
  - **TrOCR** - Microsoft's transformer model, best for handwriting
  - **PaddleOCR** - Fast processing option
- ✍️ **Handwriting Support**: Works with both printed and handwritten text
- 📝 **Editable Output**: Generate fully editable Word (.docx) documents
- 🌍 **Multi-language**: Support for English, Hindi, Arabic, Chinese, Korean, Japanese, and more
- 🎨 **Clean UI**: Simple and intuitive Streamlit interface
- 💯 **Confidence Scores**: See OCR accuracy for each extraction
- 🆓 **Completely Free**: No API keys, no usage limits

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/blacksinisterx/ocr-ppit-assignment.git
cd ocr-ppit-assignment
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

**⚠️ Note:** First installation will take 5-10 minutes as it downloads:
- PyTorch (~500MB)
- PaddlePaddle (~100MB)
- OCR models (~100-300MB depending on engine)
- Other dependencies

### Running the App

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Initialize OCR Engine
1. Open the app in your browser
2. In the sidebar, select your preferred OCR engine:
   - **EasyOCR** - Most stable, good for general use
   - **TrOCR** - Best for handwritten notes (slower but more accurate)
   - **PaddleOCR** - Fastest option
3. Click **"🚀 Initialize OCR Engine"**
4. Wait for models to download (first time only, 1-3 minutes)
5. You'll see "✅ OCR engine initialized!" when ready

### Step 2: Upload Image
1. Click **"Browse files"** or drag and drop an image
2. Supported formats: JPG, JPEG, PNG
3. Preview will appear once uploaded

### Step 3: Extract Text
1. Click **"🔍 Extract Text"** button
2. Wait 10-60 seconds for processing (varies by engine and image size)
3. View extracted text in the right panel

### Step 4: Generate Word Document
1. Review and edit extracted text if needed
2. Click **"📥 Generate Word Document"**
3. Click **"⬇️ Download Word Document"** to save

## ⚙️ Configuration Options

### OCR Engine Selection

**EasyOCR (Recommended for most users)**
- ✅ Stable and reliable
- ✅ Good for both handwriting & print
- ✅ Multi-language support
- ~100MB models

**TrOCR (Best for handwriting)**
- ✅ Excellent for handwritten notes
- ✅ Microsoft's transformer-based AI
- ⚠️ Slower processing (30-60s per image)
- ~300MB model download

**PaddleOCR (Fastest)**
- ✅ Fast processing (10-20s)
- ⚠️ May have initialization issues on some systems

### Language Support

- **EasyOCR**: English, Chinese, Japanese, Korean, and 80+ languages
- **TrOCR**: Optimized for English handwriting
- **PaddleOCR**: English, Chinese, Japanese, Korean

### Processing Options

- ✅ **Preserve text structure**: Maintains paragraph layout
- 🚀 **Use GPU**: Faster processing if CUDA-enabled GPU available

## 📁 Project Structure

```
ocr-ppit-assignment/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── ocr_processor.py        # OCR processing logic
│   └── docx_generator.py       # Word document generation
├── img 1.jpeg                  # Sample handwritten notes
├── img 2.jpeg                  # Sample handwritten notes
└── img 3.jpeg                  # Sample handwritten notes
```

## 🎯 Use Cases

- 📚 **Study Notes**: Convert handwritten notes to digital documents
- 📄 **Document Digitization**: Extract text from scanned documents
- 📝 **Form Processing**: Extract data from forms and receipts
- 🌐 **Translation Prep**: Extract text for translation
- 📊 **Data Entry**: Automate text extraction from images

## 🔧 Troubleshooting

### "OCR processor not initialized"
- Click the "Initialize OCR Engine" button in sidebar
- Wait for initialization to complete

### Slow Processing
- Large images (>5MB) take longer
- First run downloads models (one-time delay)
- Consider enabling GPU if available
- Try EasyOCR for faster processing

### Poor Text Recognition
- Ensure image is clear and well-lit
- Try increasing image resolution
- For handwriting, ensure text is legible
- Try TrOCR engine for better handwriting recognition
- Adjust language settings if needed

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment if you created one
- Try reinstalling: `pip install --force-reinstall -r requirements.txt`

### PaddleOCR Issues
- If PaddleOCR fails to initialize, switch to EasyOCR
- Some Windows systems may have compatibility issues
- EasyOCR is the most reliable alternative

## 🛠️ Technical Details

### Technologies Used
- **Streamlit** (1.31.0) - Web framework
- **EasyOCR** (1.7.1) - OCR engine
- **PaddleOCR** (2.7.3) - Alternative OCR engine
- **PaddlePaddle** (3.3.0) - Deep learning framework
- **Transformers** (4.36.0) - For TrOCR model
- **python-docx** (1.1.0) - Word document generation
- **Pillow** (10.2.0) - Image processing
- **PyTorch** - Deep learning backend

### OCR Accuracy
- Printed text: 95-99% accuracy
- Clear handwriting: 70-90% accuracy
- Complex handwriting: 50-70% accuracy
- Depends on image quality and legibility

## 📝 Tips for Best Results

1. **Image Quality**: Use high-resolution, well-lit images
2. **Contrast**: Ensure good contrast between text and background
3. **Orientation**: Keep text horizontal and upright
4. **Multiple Languages**: Select appropriate language combination
5. **Editing**: Review and correct extracted text before generating document
6. **Engine Choice**: Use TrOCR for handwriting, EasyOCR for general use

## 🐛 Known Limitations

- Complex multi-column layouts may not preserve perfectly
- Extremely stylized fonts may reduce accuracy
- Mathematical equations/symbols have limited support
- Very small text (<10pt) may be difficult to read



## 🤝 Contributing

This project was created for educational purposes as part of the PPIT course at FAST University.

---

**Made with ❤️ for OCR and Document Processing**
