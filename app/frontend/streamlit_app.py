import streamlit as st
import os
import sys
from datetime import datetime

# Add frontend directory to path to allow absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui import load_css, render_sidebar, render_home, render_results, render_history, render_about
from utils import call_prediction_api, get_image_info, process_image_for_display
from report import generate_pdf_report, generate_json_report, get_download_link
from recommendations import get_recommendations, get_disclaimer

# Configure page
st.set_page_config(
    page_title="Brain Tumor Detection AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
load_css(css_path)

# Initialize Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None
if 'current_image_info' not in st.session_state:
    st.session_state.current_image_info = None
if 'current_image' not in st.session_state:
    st.session_state.current_image = None

def main():
    # Sidebar Navigation
    current_page = render_sidebar()
    
    # Page Routing
    if current_page == "Dashboard":
        render_home()
        
    elif current_page == "Upload MRI":
        st.markdown("<h2>Upload MRI Scan</h2>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Upload a T1-weighted contrast-enhanced MRI image for AI analysis.</p>", unsafe_allow_html=True)
        
        st.info("💡 For best results, please upload a clear, high-resolution T1-weighted contrast-enhanced MRI scan.")
        uploaded_file = st.file_uploader("Drag and drop your MRI scan here", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Display image preview
                image = process_image_for_display(uploaded_file)
                st.image(image, caption="Uploaded MRI", use_container_width=True)
                
            with col2:
                # Image metadata
                st.markdown("### Image Details")
                image_info = get_image_info(uploaded_file)
                
                st.markdown(f"**File Name:** `{image_info['filename']}`")
                st.markdown(f"**Resolution:** `{image_info['resolution']}`")
                st.markdown(f"**Size:** `{image_info['size']}`")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Run AI Analysis", type="primary", use_container_width=True):
                    with st.spinner("Initializing Deep Learning Model..."):
                        # Simulate processing bar
                        progress_bar = st.progress(0)
                        import time
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        # Call API
                        prediction_data = call_prediction_api(uploaded_file)
                        
                        if prediction_data:
                            st.session_state.current_prediction = prediction_data
                            st.session_state.current_image_info = image_info
                            st.session_state.current_image = image
                            
                            # Save to persistent history
                            from history_manager import add_history_item
                            add_history_item(image, prediction_data)
                            
                            st.success("Analysis Complete!")
                            
                            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
                            
                            # Render visual results
                            render_results(prediction_data, image_info)
                            
                            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
                            
                            # Recommendations
                            st.markdown("### Patient Recommendations")
                            
                            recs = get_recommendations(prediction_data['predicted_class'])
                            recs_html = "".join([f"<li style='margin-bottom: 8px;'>{rec}</li>" for rec in recs])
                            disclaimer_html = f"<div style='margin-top: 20px; padding: 10px; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; border-radius: 4px; font-size: 0.9rem;'>{get_disclaimer()}</div>"
                            
                            st.markdown(
                                f"<div class='glass-card'><ul style='margin-top: 0;'>{recs_html}</ul>{disclaimer_html}</div>", 
                                unsafe_allow_html=True
                            )
                            
                            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
                            
                            # Downloads
                            st.markdown("### Export Results")
                            exp_col1, exp_col2, exp_col3 = st.columns(3)
                            
                            with exp_col1:
                                pdf_bytes = generate_pdf_report(prediction_data, image_info, image)
                                if pdf_bytes:
                                    st.markdown(get_download_link(pdf_bytes, "ai_medical_report.pdf", "📥 Download AI Report (PDF)"), unsafe_allow_html=True)
                                else:
                                    st.warning("PDF generation requires 'fpdf2' package. Please install it using 'pip install fpdf2'.")
                            
                            with exp_col2:
                                json_str = generate_json_report(prediction_data, image_info)
                                st.markdown(get_download_link(json_str.encode(), "prediction_data.json", "📥 Download Raw JSON"), unsafe_allow_html=True)
                                
                            with exp_col3:
                                pred_only = str(prediction_data).encode()
                                st.markdown(get_download_link(pred_only, "prediction_summary.txt", "📥 Download Prediction"), unsafe_allow_html=True)
            
    elif current_page == "Prediction History":
        st.markdown("<h2>Session History</h2>", unsafe_allow_html=True)
        render_history()
        
    elif current_page == "About Model":
        st.markdown("<h2>About the AI Model</h2>", unsafe_allow_html=True)
        render_about()
        
    # Footer
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); color: #64748b; font-size: 0.8rem;">
            Powered by TensorFlow • FastAPI • Streamlit • Docker<br>
            Made by Sai | <a href="https://github.com/sainath/brain-tumor-detector" style="color: #3b82f6; text-decoration: none;">GitHub</a>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
