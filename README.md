# 📄 OCR Image to Word App

A powerful application that converts images (including handwritten notes) into editable Word documents using AI-powered OCR technology.

## ✨ Features

- 🖼️ **Image Upload**: Support for JPG, PNG, JPEG formats
- 🤖 **Multiple OCR Engines**: 
  - **EasyOCR** - Stable and reliable for general use (default)
  - **PaddleOCR** - High accuracy option
  - **Tesseract** - Preserves text formatting (bold/italic)
- ✍️ **Handwriting Support**: Works with both printed and handwritten text
- 📝 **Editable Output**: Generate fully editable Word (.docx) documents
- 🌍 **Multi-language**: Support for English, Hindi, Arabic, Chinese, Korean, Japanese, and more
- 🎨 **Two Interfaces**: Streamlit web app AND native Desktop GUI
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

4. **Install compatible PaddleOCR (important!):**
```bash
pip install paddlepaddle==2.6.2 paddleocr==2.7.3
```

5. **Install Tesseract (optional, for formatting preservation):**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to default path (`C:\Program Files\Tesseract-OCR`)

## 🖥️ Running the App

### Option 1: Desktop App (Recommended)
```bash
python desktop_app.py
```
Native GUI with all features including:
- Engine selection dropdown
- Enhanced preprocessing toggle
- Real-time extraction preview
- Direct Word document export

### Option 2: Web App (Streamlit)
```bash
streamlit run app.py
```
Opens in browser at `http://localhost:8501`

## 📖 How to Use (Desktop App)

1. **Launch**: Run `python desktop_app.py`
2. **Select Engine**: Choose EasyOCR, PaddleOCR, or Tesseract from dropdown
3. **Load Image**: Click "Select Image" and choose your file
4. **Extract**: Click "Extract Text" - results appear in preview
5. **Save**: Click "Save as Word" to generate .docx file

### Preprocessing Toggle
- **OFF (default)**: Best for clean, high-quality images
- **ON**: Use for noisy/low-quality scans (applies blur + thresholding)

## ⚙️ OCR Engine Comparison

| Engine | Speed | Accuracy | Formatting | Best For |
|--------|-------|----------|------------|----------|
| EasyOCR | Medium | High | No | General use |
| PaddleOCR | Fast | Very High | No | High accuracy needs |
| Tesseract | Fast | Good | Yes (bold/italic) | Document formatting |

## 📁 Project Structure

```
ocr-ppit-assignment/
├── app.py                 # Streamlit web app
├── desktop_app.py         # Tkinter desktop app (NEW)
├── requirements.txt       # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── ocr_processor.py   # OCR processing logic
│   └── docx_generator.py  # Word document generation
├── img 1.jpeg             # Sample image
├── img 2.jpeg             # Sample image
└── img 3.jpeg             # Sample image
```

## 🔧 Troubleshooting

### PaddleOCR Issues
**Important**: Use these specific versions to avoid crashes:
```bash
pip install paddlepaddle==2.6.2 paddleocr==2.7.3
```

### Tesseract Not Found
- Install from: https://github.com/UB-Mannheim/tesseract/wiki
- The app auto-detects common install paths
- If not found, EasyOCR is used as fallback

### Slow Processing
- Disable "Enhanced Preprocessing" for clean images
- First run downloads models (one-time delay)
- Enable GPU if available

### Poor Text Recognition
- Ensure image is clear and well-lit
- Try different engines (PaddleOCR often best for printed text)
- Use Tesseract for preserving formatting

## 🛠️ Technical Details

### Dependencies
- **EasyOCR** (1.7.1) - Default OCR engine
- **PaddleOCR** (2.7.3) - High accuracy OCR
- **PaddlePaddle** (2.6.2) - Deep learning framework
- **pytesseract** - Tesseract wrapper
- **python-docx** (1.1.0) - Word generation
- **Pillow** - Image processing
- **OpenCV** - Image preprocessing

## 🤝 Contributing

This project was created for educational purposes as part of the PPIT course at FAST University.

---

**Made with ❤️ for OCR and Document Processing**
