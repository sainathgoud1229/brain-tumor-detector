def get_recommendations(predicted_class):
    """
    Returns dynamic medical recommendations based on the tumor class.
    Always includes a medical disclaimer.
    """
    recommendations = {
        "notumor": [
            "Maintain a healthy lifestyle and balanced diet.",
            "Schedule regular annual checkups.",
            "If symptoms like headaches or dizziness persist, consult a doctor.",
            "Practice stress management and ensure adequate sleep."
        ],
        "glioma": [
            "Consult a neurologist or neuro-oncologist immediately.",
            "Carry this MRI scan and any previous medical records to your consultation.",
            "Further imaging (such as an MRI with contrast) or a biopsy may be required.",
            "Discuss potential treatment plans, which may include surgery, radiation, or chemotherapy."
        ],
        "meningioma": [
            "Schedule a consultation with a specialist (neurosurgeon or neurologist).",
            "Further imaging may be needed to determine the exact size and growth rate.",
            "Many meningiomas are benign and slow-growing, but professional evaluation is critical.",
            "Discuss regular monitoring versus active treatment options with your doctor."
        ],
        "pituitary": [
            "Consult an endocrinologist for hormonal evaluation.",
            "Consult a neurosurgeon specialized in pituitary tumors.",
            "Blood tests may be required to check hormone levels.",
            "Discuss potential visual field testing, as these tumors can affect the optic nerves."
        ]
    }
    
    class_normalized = str(predicted_class).lower()
    
    # Provide a default if class not found
    if class_normalized not in recommendations:
        return ["Consult a medical professional for a comprehensive evaluation.",
                "Bring your MRI scans to a neurologist for further diagnosis."]
                
    return recommendations[class_normalized]

def get_disclaimer():
    """Returns the standard medical disclaimer"""
    return (
        "**MEDICAL DISCLAIMER:** This AI tool is for research and educational purposes only. "
        "It does not provide medical advice, professional diagnosis, or treatment recommendations. "
        "Always seek the advice of your physician or other qualified health provider with any "
        "questions you may have regarding a medical condition."
    )
