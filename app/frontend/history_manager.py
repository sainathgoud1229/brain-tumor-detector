import json
import os
import base64
from io import BytesIO
import time
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def add_history_item(image, prediction_data):
    history = load_history()
    
    # convert image to base64
    buffered = BytesIO()
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    item_id = str(int(time.time() * 1000))
    
    new_item = {
        "id": item_id,
        "image_b64": img_str,
        "prediction": prediction_data['predicted_class'],
        "confidence": prediction_data['confidence'],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "starred": False
    }
    history.append(new_item)
    save_history(history)

def toggle_star(item_id):
    history = load_history()
    for item in history:
        if item["id"] == item_id:
            item["starred"] = not item.get("starred", False)
            break
    save_history(history)

def delete_item(item_id):
    history = load_history()
    history = [item for item in history if item["id"] != item_id]
    save_history(history)
