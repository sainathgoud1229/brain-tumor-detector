import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def load_css(file_path):
    """Loads custom CSS."""
    try:
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Falling back to default styles.")

def render_sidebar():
    """Renders the modern sidebar."""
    with st.sidebar:
        import os
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
        if os.path.exists(logo_path):
            col_l, col_c, col_r = st.columns([1, 2, 1])
            with col_c:
                st.image(logo_path, width=100)
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="color: #3b82f6; font-weight: 800; letter-spacing: 1px;">NeuroAI<br>Diagnostics</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown("### Navigation")
        # In a multi-page app, this would use st.page_link or radio buttons
        page = st.radio(
            "Select Page", 
            ["Dashboard", "Upload MRI", "Prediction History", "About Model"],
            label_visibility="collapsed"
        )
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        st.markdown("### Resources")
        st.markdown("🔗 [GitHub Repository](https://github.com/sainath/brain-tumor-detector)")
        st.markdown("🔗 [LinkedIn](https://linkedin.com/in/sainath)")
        
        return page

def render_home():
    """Renders the Home Dashboard page."""
    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 3rem 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem; background: -webkit-linear-gradient(45deg, #3b82f6, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Brain Tumor Detection AI
            </h1>
            <p class="subtitle" style="font-size: 1.2rem;">Deep Learning Powered MRI Analysis Pipeline</p>
            <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto 2rem auto;">
                An advanced medical imaging AI powered by EfficientNetB0 transfer learning to detect and classify brain tumors from MRI scans with high accuracy.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; height: 100%;">
                <h3 style="color: #3b82f6;">🚀 High Accuracy</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">Powered by state-of-the-art CNN architecture</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; height: 100%;">
                <h3 style="color: #10b981;">⚡ Real-time</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">Millisecond inference with FastAPI</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; height: 100%;">
                <h3 style="color: #f59e0b;">🏥 Clinical Focus</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">Provides medical recommendations and reports</p>
            </div>
            """, unsafe_allow_html=True
        )

def render_results(prediction_data, image_info):
    """Renders the prediction results visually."""
    st.markdown("### AI Analysis Results")
    
    pred_class = prediction_data.get('predicted_class', 'Unknown')
    confidence = prediction_data.get('confidence', 0.0)
    
    # Determine confidence badge and risk status
    if confidence >= 90:
        conf_badge = '<span class="badge badge-success">High Confidence</span>'
    elif confidence >= 70:
        conf_badge = '<span class="badge badge-warning">Medium Confidence</span>'
    else:
        conf_badge = '<span class="badge badge-danger">Low Confidence</span>'
        
    if pred_class.lower() == 'notumor':
        risk_badge = '<span class="badge badge-success">Normal</span>'
        risk_text = "No anomaly detected."
    else:
        risk_badge = '<span class="badge badge-danger">Critical Risk</span>'
        risk_text = f"Tumor signature detected: {pred_class.capitalize()}"
        
    # Main Prediction Card
    st.markdown(
        f"""
        <div class="glass-card" style="margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h2 style="margin: 0; color: #f8fafc;">{pred_class.capitalize()}</h2>
                    <p style="margin: 5px 0 0 0; color: var(--text-muted);">{risk_text}</p>
                </div>
                <div style="text-align: right;">
                    <h1 style="margin: 0; color: #3b82f6;">{confidence:.2f}%</h1>
                    <div style="margin-top: 5px;">{conf_badge} {risk_badge}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Visualizations
    st.markdown("### Probability Distribution")
    probs = prediction_data.get('probabilities', {})
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            """
            <div class='glass-card' style='padding: 15px; margin-bottom: 20px; text-align: center; border-left: 4px solid #3b82f6;'>
                <p style='margin: 0; font-size: 0.95rem; color: #94a3b8;'>
                    The AI model evaluates the MRI scan against 4 distinct tumor signatures to determine the most probable diagnosis.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        for cls_name, prob in probs.items():
            st.markdown(f"<p style='margin-bottom: 2px;'>{cls_name.capitalize()}</p>", unsafe_allow_html=True)
            st.progress(prob / 100.0)
        
    with col2:
        # Plotly Bar Chart
        labels = [c.capitalize() for c in probs.keys()]
        values = list(probs.values())
        
        fig = go.Figure(data=[go.Bar(
            x=values,
            y=labels,
            orientation='h',
            marker=dict(color=['#3b82f6', '#10b981', '#f59e0b', '#ef4444']),
            text=[f"{v:.1f}%" for v in values],
            textposition='auto'
        )])
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=0, b=0, l=0, r=0),
            xaxis=dict(showgrid=False, showticklabels=False, range=[0, 100]),
            yaxis=dict(showgrid=False, color='white'),
            height=200
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_history():
    import base64
    from io import BytesIO
    from PIL import Image
    from history_manager import load_history, toggle_star, delete_item
    
    history = load_history()
    
    if not history:
        st.info("No predictions made in this session yet.")
        return
        
    for item in reversed(history):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            img_data = base64.b64decode(item['image_b64'])
            img = Image.open(BytesIO(img_data))
            st.image(img, use_container_width=True)
        with col2:
            star_html = "⭐ " if item.get('starred') else ""
            border_color = "#f59e0b" if item.get('starred') else "rgba(255,255,255,0.1)"
            
            st.markdown(
                f"""
                <div class="glass-card" style="padding: 15px; border-left: 4px solid {border_color};">
                    <h4 style="margin:0;">{star_html}{item['prediction'].capitalize()}</h4>
                    <p style="color: #3b82f6; margin: 5px 0;">Confidence: {item['confidence']:.2f}%</p>
                    <p style="color: var(--text-muted); font-size: 0.8rem; margin: 0;">Time: {item['timestamp']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            # Wrap buttons in a styled container for alignment
            st.markdown("<div style='display: flex; flex-direction: column; gap: 10px; height: 100%; justify-content: center;'>", unsafe_allow_html=True)
            star_label = "Unstar" if item.get("starred") else "⭐ Star"
            if st.button(star_label, key=f"star_{item['id']}", use_container_width=True):
                toggle_star(item['id'])
                st.rerun()
                
            if st.button("🗑️ Delete", key=f"del_{item['id']}", use_container_width=True):
                delete_item(item['id'])
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)

def render_about():
    """Renders the about model page."""
    st.markdown(
        """
        <div class="glass-card">
            <h2>Model Architecture</h2>
            <p>This application utilizes a deep learning model based on the EfficientNetB0 architecture, fine-tuned using transfer learning.</p>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding: 10px 0; color: #94a3b8;">Base Architecture</td><td style="text-align: right; font-weight: bold;">EfficientNetB0</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding: 10px 0; color: #94a3b8;">Framework</td><td style="text-align: right; font-weight: bold;">TensorFlow / Keras</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding: 10px 0; color: #94a3b8;">Input Image Size</td><td style="text-align: right; font-weight: bold;">224x224 pixels</td></tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);"><td style="padding: 10px 0; color: #94a3b8;">Target Classes</td><td style="text-align: right; font-weight: bold;">4 (Glioma, Meningioma, Pituitary, Normal)</td></tr>
                <tr><td style="padding: 10px 0; color: #94a3b8;">Reported Accuracy</td><td style="text-align: right; font-weight: bold; color: #10b981;">82%</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )
