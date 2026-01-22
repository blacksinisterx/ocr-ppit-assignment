"""
OCR Image to Word App
A Streamlit web application to convert images (including handwritten notes) into editable Word documents.
"""

import streamlit as st
from PIL import Image
import time
from datetime import datetime
import io

# Import utility modules
from utils.ocr_processor import OCRProcessor
from utils.docx_generator import DocxGenerator


# Page configuration
st.set_page_config(
    page_title="Image to Word OCR App",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'ocr_processor' not in st.session_state:
    st.session_state.ocr_processor = None
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'confidence_score' not in st.session_state:
    st.session_state.confidence_score = 0.0
if 'processing_time' not in st.session_state:
    st.session_state.processing_time = 0.0


def initialize_ocr(engine='easyocr', languages=['en'], gpu=False):
    """Initialize OCR processor with progress indicator"""
    if st.session_state.ocr_processor is None:
        spinner_messages = {
            'trocr': '🔄 Initializing TrOCR (~300MB download on first run - may take 2-3 minutes)...',
            'paddleocr': '🔄 Initializing PaddleOCR (may take 1-2 minutes)...',
            'easyocr': '🔄 Initializing EasyOCR (downloading models on first run - may take 1-2 minutes)...'
        }
        
        with st.spinner(spinner_messages.get(engine, '🔄 Initializing OCR engine...')):
            try:
                processor = OCRProcessor(engine=engine, languages=languages, gpu=gpu)
                processor.initialize_reader()
                st.session_state.ocr_processor = processor
            except Exception as e:
                st.error(f"Failed to initialize {engine}: {str(e)}")
                raise
    return st.session_state.ocr_processor


def process_image(image, preserve_structure=True):
    """Process image and extract text"""
    processor = st.session_state.ocr_processor
    
    if processor is None:
        st.error("❌ OCR processor not initialized. Please initialize first.")
        return None, 0.0, 0.0
    
    start_time = time.time()
    
    try:
        # Extract text
        if preserve_structure:
            text = processor.extract_text_with_structure(image)
        else:
            text = processor.extract_text(image)
        
        # Get confidence score
        confidence = processor.get_confidence_score(image)
        
        processing_time = time.time() - start_time
        
        return text, confidence, processing_time
    
    except Exception as e:
        st.error(f"❌ Error processing image: {str(e)}")
        return None, 0.0, 0.0


def generate_word_document(text, confidence_score=None):
    """Generate Word document from text"""
    try:
        generator = DocxGenerator()
        generator.create_document_with_sections(
            text=text,
            title="OCR Extracted Text",
            confidence_score=confidence_score
        )
        
        # Save to bytes for download
        doc_bytes = generator.save_to_bytes()
        return doc_bytes
    
    except Exception as e:
        st.error(f"❌ Error generating Word document: {str(e)}")
        return None


# Main App
def main():
    # Header
    st.markdown('<div class="main-header">📄 Image to Word OCR App</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Convert images and handwritten notes into editable Word documents</div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # OCR Engine Selection
        st.subheader("🤖 OCR Engine")
        ocr_engine_options = {
            'EasyOCR (Stable & Reliable)': 'easyocr',
            'TrOCR (Best for Handwriting)': 'trocr',
            'PaddleOCR (Fast)': 'paddleocr'
        }
        
        selected_engine = st.selectbox(
            "Select OCR Engine",
            options=list(ocr_engine_options.keys()),
            index=0,
            help="Choose OCR engine based on your needs"
        )
        
        engine = ocr_engine_options[selected_engine]
        
        # Language selection
        st.subheader("🌍 Language Options")
        
        if engine == 'trocr':
            st.info("TrOCR is optimized for English handwriting")
            languages = ['en']
        elif engine == 'easyocr':
            language_options = {
                'English': ['en'],
                'English + Chinese': ['en', 'ch_sim'],
                'English + Japanese': ['en', 'ja'],
                'English + Korean': ['en', 'ko']
            }
            selected_lang = st.selectbox(
                "Select OCR Language",
                options=list(language_options.keys()),
                index=0
            )
            languages = language_options[selected_lang]
        else:
            language_options = {
                'English': ['en'],
                'Chinese': ['ch'],
                'Japanese': ['japan'],
                'Korean': ['korean']
            }
            selected_lang = st.selectbox(
                "Select OCR Language",
                options=list(language_options.keys()),
                index=0
            )
            languages = language_options[selected_lang]
        
        # Processing options
        st.subheader("Processing Options")
        preserve_structure = st.checkbox("Preserve text structure", value=True, 
                                        help="Attempts to maintain paragraph layout")
        
        use_gpu = st.checkbox("Use GPU (if available)", value=False,
                            help="Faster processing with GPU, requires CUDA")
        
        # Initialize OCR button
        st.markdown("---")
        if st.button("🚀 Initialize OCR Engine"):
            try:
                initialize_ocr(engine=engine, languages=languages, gpu=use_gpu)
                st.success("✅ OCR engine initialized!")
            except Exception as e:
                st.error(f"❌ Failed to initialize OCR: {str(e)}")
                st.info("💡 Try a different OCR engine")
        
        # Info
        st.markdown("---")
        
        # Engine-specific info
        if engine == 'easyocr':
            st.success("""
            **EasyOCR**
            ✅ Stable and reliable
            ✅ Good for handwriting & print
            ✅ Multi-language support
            ✅ ~100MB models
            """)
        elif engine == 'trocr':
            st.success("""
            **TrOCR (Microsoft)**
            ✅ Best for handwritten notes
            ✅ Transformer-based AI
            ⚠️ Slower (~30-60s per image)
            ⚠️ ~300MB model download
            """)
        else:
            st.warning("""
            **PaddleOCR**
            ✅ Fast processing
            ⚠️ May have initialization issues
            💡 If fails, try EasyOCR
            """)
        
        st.markdown("---")
        st.caption("""
        **Tips for best results:**
        - Clear, well-lit images
        - High resolution
        - Dark text on light background
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png'],
            help="Upload an image containing text you want to extract"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Image info
            st.caption(f"📊 Image size: {image.width} x {image.height} pixels")
            
            # Process button
            if st.button("🔍 Extract Text", type="primary"):
                # Check if OCR is initialized
                if st.session_state.ocr_processor is None:
                    st.warning("⚠️ Please initialize OCR engine first (see sidebar)")
                else:
                    try:
                        with st.spinner("🔄 Processing image... This may take 10-30 seconds..."):
                            text, confidence, proc_time = process_image(image, preserve_structure)
                            
                            if text is not None:
                                st.session_state.extracted_text = text
                                st.session_state.confidence_score = confidence
                                st.session_state.processing_time = proc_time
                                
                                st.markdown(f"""
                                    <div class="success-box">
                                        ✅ <strong>Text extracted successfully!</strong><br>
                                        ⏱️ Processing time: {proc_time:.2f} seconds<br>
                                        📊 Confidence: {confidence*100:.1f}%
                                    </div>
                                """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Error processing image: {str(e)}")
                        st.info("💡 Try switching to a different OCR engine or reinitialize")
    
    with col2:
        st.header("📝 Extracted Text")
        
        if st.session_state.extracted_text:
            # Display extracted text
            text_area = st.text_area(
                "Edit extracted text if needed:",
                value=st.session_state.extracted_text,
                height=400,
                help="You can edit the text before generating the Word document"
            )
            
            # Update session state if text is edited
            if text_area != st.session_state.extracted_text:
                st.session_state.extracted_text = text_area
            
            # Stats
            word_count = len(st.session_state.extracted_text.split())
            char_count = len(st.session_state.extracted_text)
            st.caption(f"📊 Words: {word_count} | Characters: {char_count}")
            
            # Generate Word document button
            st.markdown("---")
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("📥 Generate Word Document", type="primary"):
                    with st.spinner("📝 Creating Word document..."):
                        doc_bytes = generate_word_document(
                            st.session_state.extracted_text,
                            st.session_state.confidence_score
                        )
                        
                        if doc_bytes:
                            st.success("✅ Word document created!")
                            
                            # Generate filename
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"ocr_extracted_{timestamp}.docx"
                            
                            # Download button
                            st.download_button(
                                label="⬇️ Download Word Document",
                                data=doc_bytes,
                                file_name=filename,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
            
            with col_b:
                # Clear button
                if st.button("🗑️ Clear"):
                    st.session_state.extracted_text = ""
                    st.session_state.confidence_score = 0.0
                    st.session_state.processing_time = 0.0
                    st.rerun()
        
        else:
            st.info("👈 Upload an image and click 'Extract Text' to see results here")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
            Built with Streamlit 🎈 | Powered by EasyOCR 🤖 | Free & Open Source 💙
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
