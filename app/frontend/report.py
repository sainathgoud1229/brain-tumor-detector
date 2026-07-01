import json
import base64
from datetime import datetime
from recommendations import get_recommendations
try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    HAS_FPDF = False

def generate_pdf_report(prediction_data, image_info, image_path=None):
    """
    Generates a PDF report containing the AI analysis results.
    """
    if not HAS_FPDF:
        return None

    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Brain Tumor AI Detection Report', 0, 1, 'C')
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Date and Time
    pdf.set_font('Arial', 'B', 10)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 10, f'Generated On: {now}', 0, 1, 'R')
    pdf.ln(5)
    
    # Model Information
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Model Information', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, 'Architecture: EfficientNetB0 (Transfer Learning)', 0, 1, 'L')
    pdf.cell(0, 8, 'Input Size: 224x224 pixels', 0, 1, 'L')
    pdf.cell(0, 8, 'Target Classes: Glioma, Meningioma, Pituitary Tumor, No Tumor', 0, 1, 'L')
    pdf.ln(10)
    
    # Image Information
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Uploaded MRI Details', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f"File Name: {image_info['filename']}", 0, 1, 'L')
    pdf.cell(0, 8, f"Resolution: {image_info['resolution']}", 0, 1, 'L')
    pdf.cell(0, 8, f"File Size: {image_info['size']}", 0, 1, 'L')
    pdf.ln(5)

    if image_path is not None:
        import tempfile
        import os
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                if hasattr(image_path, 'mode') and image_path.mode != 'RGB':
                    image_path = image_path.convert('RGB')
                image_path.save(tmp.name)
            # Embed image in PDF, 80 units wide
            pdf.image(tmp.name, w=80)
            os.remove(tmp.name)
        except Exception as e:
            pass # Ignore if image embedding fails
    
    pdf.ln(10)

    # Prediction Results
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 51, 153)
    pdf.cell(0, 10, 'AI Analysis Results', 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    
    pred_class = prediction_data.get('predicted_class', 'Unknown').capitalize()
    confidence = prediction_data.get('confidence', 0.0)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(50, 10, 'Predicted Class:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'{pred_class}', 0, 1)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(50, 10, 'Confidence:', 0, 0)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'{confidence:.2f}%', 0, 1)
    
    pdf.ln(5)
    
    # Probabilities
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Class Probabilities:', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    probs = prediction_data.get('probabilities', {})
    for cls_name, prob in probs.items():
        pdf.cell(0, 8, f'- {cls_name.capitalize()}: {prob:.2f}%', 0, 1, 'L')
        
    pdf.ln(10)
    
    # Recommendations
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Patient Recommendations:', 0, 1, 'L')
    pdf.set_font('Arial', '', 11)
    
    recs = get_recommendations(prediction_data.get('predicted_class', ''))
    for rec in recs:
        pdf.multi_cell(0, 6, f'- {rec}')
        pdf.ln(2)
        
    pdf.ln(10)
    
    # Disclaimer
    pdf.set_text_color(200, 0, 0)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, 'MEDICAL DISCLAIMER:', 0, 1, 'L')
    pdf.set_font('Arial', '', 9)
    disclaimer = "This AI tool is for research and educational purposes only. It does not provide medical advice, professional diagnosis, or treatment recommendations. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition."
    pdf.multi_cell(0, 5, disclaimer)
    
    return bytes(pdf.output())

def generate_json_report(prediction_data, image_info):
    """
    Generates a JSON version of the report.
    """
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "model_info": {
            "architecture": "EfficientNetB0",
            "input_size": "224x224",
            "classes": ["glioma", "meningioma", "pituitary", "notumor"]
        },
        "image_info": image_info,
        "prediction": prediction_data
    }
    return json.dumps(report_data, indent=4)

def get_download_link(data, filename, text):
    """
    Generates a download link for binary or text data.
    """
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}" class="stButton" style="text-decoration:none;"><button style="width:100%;">{text}</button></a>'
    return href
