# 📄 OCR Image to Word App

A simple and powerful web application that converts images (including handwritten notes) into editable Word documents using AI-powered OCR.

## ✨ Features

- 🖼️ **Image Upload**: Support for JPG, PNG, JPEG formats
- 🤖 **AI-Powered OCR**: Uses EasyOCR for accurate text extraction
- ✍️ **Handwriting Support**: Works with both printed and handwritten text
- 📝 **Editable Output**: Generate fully editable Word (.docx) documents
- 🌍 **Multi-language**: Support for English, Hindi, Arabic, Chinese, Urdu, and more
- 🎨 **Clean UI**: Simple and intuitive Streamlit interface
- 💯 **Confidence Scores**: See OCR accuracy for each extraction
- 🆓 **Completely Free**: No API keys, no usage limits

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd "d:\FAST\Semester 8\PPIT\Tasks"
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
- EasyOCR models (~100-200MB)
- Other dependencies

### Running the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 📖 How to Use

### Step 1: Initialize OCR Engine
1. Click the **"🚀 Initialize OCR Engine"** button in the sidebar
2. Wait for models to download (first time only, ~1-2 minutes)
3. You'll see "✅ OCR engine initialized!" when ready

### Step 2: Upload Image
1. Click **"Browse files"** or drag and drop an image
2. Supported formats: JPG, JPEG, PNG
3. Preview will appear once uploaded

### Step 3: Extract Text
1. Click **"🔍 Extract Text"** button
2. Wait 10-30 seconds for processing
3. View extracted text in the right panel

### Step 4: Generate Word Document
1. Review and edit extracted text if needed
2. Click **"📥 Generate Word Document"**
3. Click **"⬇️ Download Word Document"** to save

## ⚙️ Configuration Options

### Language Support
Choose from sidebar:
- **English** (default)
- **English + Hindi**
- **English + Arabic**
- **English + Chinese**
- **English + Urdu**

### Processing Options
- ✅ **Preserve text structure**: Maintains paragraph layout
- 🚀 **Use GPU**: Faster processing if CUDA-enabled GPU available

## 📁 Project Structure

```
Tasks/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── plan.md                     # Implementation plan
└── utils/
    ├── __init__.py
    ├── ocr_processor.py        # OCR processing logic
    └── docx_generator.py       # Word document generation
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

### Poor Text Recognition
- Ensure image is clear and well-lit
- Try increasing image resolution
- For handwriting, ensure text is legible
- Adjust language settings if needed

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment if you created one

## 🛠️ Technical Details

### Technologies Used
- **Streamlit** (1.31.0) - Web framework
- **EasyOCR** (1.7.1) - OCR engine
- **python-docx** (1.1.0) - Word document generation
- **Pillow** (10.2.0) - Image processing
- **PyTorch** - Deep learning backend

### OCR Accuracy
- Printed text: 95-99% accuracy
- Clear handwriting: 70-85% accuracy
- Complex handwriting: 50-70% accuracy
- Depends on image quality and legibility

## 📝 Tips for Best Results

1. **Image Quality**: Use high-resolution, well-lit images
2. **Contrast**: Ensure good contrast between text and background
3. **Orientation**: Keep text horizontal and upright
4. **Multiple Languages**: Select appropriate language combination
5. **Editing**: Review and correct extracted text before generating document

## 🐛 Known Limitations

- Complex multi-column layouts may not preserve perfectly
- Extremely stylized fonts may reduce accuracy
- Mathematical equations/symbols have limited support
- Very small text (<10pt) may be difficult to read

## 📄 License

Free to use for personal and educational purposes.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the [plan.md](plan.md) file for technical details
3. Ensure all dependencies are correctly installed

## 🎓 Educational Use

This project was created for educational purposes as part of the PPIT course at FAST University.

---

**Happy OCR-ing! 🎉**
