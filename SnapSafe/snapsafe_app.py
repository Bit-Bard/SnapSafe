import streamlit as st
from PIL import Image
import tempfile
import os
from harmness_detection import Harmness_Detection_function

# Configure page - MUST BE FIRST
st.set_page_config(
    page_title="SnapSafe - Product Safety Analyzer", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛡️"
)

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app dark theme */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar dark theme styling */
    .css-1d391kg, section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .css-1d391kg .css-1v3fvcr, section[data-testid="stSidebar"] > div {
        background: transparent;
        padding-top: 2rem;
    }
    
    /* Sidebar content styling */
    .sidebar-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .sidebar-card h2, .sidebar-card h4 {
        color: #ffffff;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .sidebar-card p, .sidebar-card li {
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.6;
    }
    
    .sidebar-card ul {
        padding-left: 1.2rem;
        margin: 1rem 0;
    }
    
    .sidebar-card li {
        margin-bottom: 0.5rem;
        list-style-type: none;
        position: relative;
    }
    
    .sidebar-card li::before {
        content: "▸";
        color: #64ffda;
        font-weight: bold;
        position: absolute;
        left: -1rem;
    }
    
    .sidebar-card hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 1.5rem 0;
    }
    
    .sidebar-card a {
        color: #64ffda;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        background: rgba(100, 255, 218, 0.1);
        border: 1px solid rgba(100, 255, 218, 0.2);
    }
    
    .sidebar-card a:hover {
        color: #ffffff;
        background: rgba(100, 255, 218, 0.2);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(100, 255, 218, 0.3);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin-bottom: 2rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        background: linear-gradient(135deg, #64ffda 0%, #ffffff 50%, #bb86fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .main-header h3 {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
        margin-top: 0;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.7);
        margin-top: 1rem;
    }
    
    /* Dark theme card styling */
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        color: #ffffff;
    }
    
    .result-card h3, .result-card h4 {
        color: #ffffff;
        font-weight: 600;
    }
    
    .chemical-card {
        background: linear-gradient(135deg, rgba(100, 255, 218, 0.1) 0%, rgba(187, 134, 252, 0.1) 100%);
        border: 1px solid rgba(100, 255, 218, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: #ffffff;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 24px rgba(100, 255, 218, 0.1);
    }
    
    .chemical-card h3 {
        color: #64ffda;
        margin-bottom: 1rem;
    }
    
    .score-card {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 193, 7, 0.1) 100%);
        border: 1px solid rgba(255, 193, 7, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: #ffffff;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 24px rgba(255, 193, 7, 0.1);
    }
    
    .score-card h3 {
        color: #ffc107;
        margin-bottom: 1rem;
    }
    
    .barcode-card {
        background: linear-gradient(135deg, rgba(187, 134, 252, 0.1) 0%, rgba(255, 64, 129, 0.1) 100%);
        border: 1px solid rgba(187, 134, 252, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: #ffffff;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 24px rgba(187, 134, 252, 0.1);
    }
    
    .barcode-card h3 {
        color: #bb86fc;
        margin-bottom: 1rem;
    }
    
    /* Dark theme risk indicators */
    .risk-low {
        background: linear-gradient(135deg, #4caf50 0%, #81c784 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-block;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ff9800 0%, #ffb74d 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-block;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #f44336 0%, #ef5350 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-block;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
    }
    
    /* Button dark theme styling */
    .stButton > button {
        background: linear-gradient(135deg, #64ffda 0%, #bb86fc 100%);
        color: #000000;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(100, 255, 218, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(100, 255, 218, 0.4);
    }
    
    /* Radio button dark theme */
    .stRadio > label {
        color: #ffffff;
        font-weight: 500;
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* File uploader dark theme */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed rgba(100, 255, 218, 0.3);
        border-radius: 10px;
    }
    
    /* Progress bar dark theme */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #64ffda 0%, #bb86fc 100%);
    }
    
    /* Text styling */
    .stMarkdown, .stText {
        color: #ffffff;
    }
    
    /* Success/Error messages dark theme */
    .stAlert {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
    }
    
    /* JSON viewer dark theme */
    .stJson {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    
    /* Footer dark theme */
    .footer-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .footer-card p {
        color: rgba(255, 255, 255, 0.8);
        margin: 0;
        font-size: 1.1rem;
    }
    
    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🛡️ SnapSafe</h1>
    <h3>🔍 AI-Powered Product Safety Analyzer</h3>
    <p style="color: rgba(255, 255, 255, 0.8); font-size: 1.2rem;">
        Instantly analyze product safety by scanning labels with advanced AI technology
    </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📌 About SnapSafe")
    st.write(
        "SnapSafe uses cutting-edge AI to detect harmful chemicals in products "
        "through intelligent image analysis of product labels."
    )
    st.markdown("---")
    st.markdown("### 🚀 Features")
    st.write("- Real-time chemical detection")
    st.write("- Risk assessment scoring")
    st.write("- Barcode information extraction")
    st.write("- Instant safety recommendations")
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.write("**Dhruv Devaliya**  \nAI & Data Science Enthusiast")
    st.write("📍 India")
    st.write("[🐙 GitHub](https://github.com/Bit-Bard) | [💼 LinkedIn](https://www.linkedin.com/in/dhruv-devaliya/)")
    st.markdown("---")
    st.markdown("### 📧 Contact")
    st.write("**Email**: dhruv.devaliya@example.com")
    st.markdown("> 💡 Interested in AI/ML collaborations? Let’s connect!")

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="result-card">
        <h3 style="text-align: center; margin-bottom: 1.5rem; color: #2d3748;">
            📤 Choose Your Input Method
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Input method selection with better styling
    option = st.radio(
        "",
        ["📂 Upload from Device", "📸 Capture from Webcam"],
        horizontal=True
    )

    img = None

    # File upload section
    if option == "📂 Upload from Device":
        st.markdown("""
        <div class="result-card">
            <h4 style="text-align: center; color: #4a5568;">📁 Upload Product Image</h4>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=["png", "jpg", "jpeg"],
            help="Upload a clear image of the product label for best results"
        )
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.markdown("""
            <div class="result-card">
                <h4 style="text-align: center; color: #4a5568;">📷 Uploaded Image</h4>
            </div>
            """, unsafe_allow_html=True)
            st.image(img, caption="✅ Image uploaded successfully", use_column_width=True)

    # Camera capture section
    elif option == "📸 Capture from Webcam":
        st.markdown("""
        <div class="result-card">
            <h4 style="text-align: center; color: #4a5568;">📸 Capture from Camera</h4>
        </div>
        """, unsafe_allow_html=True)
        
        captured_img = st.camera_input("📷 Take a picture of the product label")
        
        if captured_img:
            img = Image.open(captured_img)
            st.markdown("""
            <div class="result-card">
                <h4 style="text-align: center; color: #4a5568;">📷 Captured Image</h4>
            </div>
            """, unsafe_allow_html=True)
            st.image(img, caption="✅ Image captured successfully", use_column_width=True)

    # Analysis section
    if img:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Animated analysis
        with st.spinner("🔬 Analyzing image with AI..."):
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔍 Extracting text from image...")
                elif i < 60:
                    status_text.text("🧪 Identifying chemicals...")
                elif i < 90:
                    status_text.text("📊 Calculating risk scores...")
                else:
                    status_text.text("✅ Finalizing analysis...")
            
            # Process the image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                img_path = tmp_file.name
                img.save(img_path)

            try:
                result = Harmness_Detection_function(img_path)
            finally:
                os.remove(img_path)

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

        if result:
            st.balloons()  # Celebration animation
            
            st.markdown("""
            <div style="text-align: center; padding: 1rem; background: rgba(76, 175, 80, 0.1); border-radius: 15px; margin: 2rem 0;">
                <h2 style="color: #4caf50;">✅ Analysis Completed Successfully!</h2>
            </div>
            """, unsafe_allow_html=True)

            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("""
                <div class="chemical-card">
                    <h3>🧪 Detected Chemicals</h3>
                    <div style="background: rgba(255, 255, 255, 0.3); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                """, unsafe_allow_html=True)
                
                if result["chemicals"]:
                    st.write(result["chemicals"])
                else:
                    st.write("✅ No harmful chemicals detected")
                
                st.markdown("</div></div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div class="score-card">
                    <h3>🧠 AI Prediction Results</h3>
                    <div style="background: rgba(255, 255, 255, 0.3); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                        <p><strong>Category:</strong> {result['category'].title()}</p>
                        <p><strong>Confidence:</strong> {result['confidence']*100:.1f}%</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_right:
                risk_class = "risk-low" if result['risk_level'].lower() == "low" else "risk-medium" if result['risk_level'].lower() == "medium" else "risk-high"
                
                st.markdown(f"""
                <div class="score-card">
                    <h3>📉 Safety Assessment</h3>
                    <div style="background: rgba(255, 255, 255, 0.3); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                        <p><strong>Average Harm Score:</strong> {result['average_score']:.1f}%</p>
                        <p><strong>Risk Level:</strong> <span class="{risk_class}">{result['risk_level'].upper()}</span></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="chemical-card">
                    <h3>📊 Detailed Scores</h3>
                    <div style="background: rgba(255, 255, 255, 0.3); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                """, unsafe_allow_html=True)
                
                st.json(result['individual_scores'])
                st.markdown("</div></div>", unsafe_allow_html=True)

            if result['barcode_info']:
                st.markdown("""
                <div class="barcode-card">
                    <h3 style="text-align: center;">📦 Product Information</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for i, info in enumerate(result['barcode_info']):
                    risk_class = "risk-low" if info['risk_level'].lower() == "low" else "risk-medium" if info['risk_level'].lower() == "medium" else "risk-high"
                    
                    st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.9); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border-left: 5px solid #667eea;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div>
                                <p><strong>🏷️ Title:</strong> {info['title']}</p>
                                <p><strong>🏢 Brand:</strong> {info['brand']}</p>
                            </div>
                            <div>
                                <p><strong>📂 Category:</strong> {info['category']}</p>
                                <p><strong>📊 Harm Score:</strong> {info['harm_score']:.1f}%</p>
                                <p><strong>⚠️ Risk Level:</strong> <span class="{risk_class}">{info['risk_level'].upper()}</span></p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(244, 67, 54, 0.1); border-radius: 15px; margin: 2rem 0;">
                <h3 style="color: #f44336;">❌ Analysis Failed</h3>
                <p style="color: #666;">Please upload a clear, valid image of a product label and try again.</p>
            </div>
            """, unsafe_allow_html=True)

# Footer with dark theme
st.markdown("""
<div class="footer-card">
    <p>Made with ❤️ by Dhruv Devaliya | Powered by AI & Computer Vision</p>
</div>
""", unsafe_allow_html=True)