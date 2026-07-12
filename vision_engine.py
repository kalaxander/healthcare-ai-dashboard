from transformers import pipeline
from PIL import Image

# Cache the model so it only loads once!
_vision_classifier = None

def setup_vision_model():
    """Initializes the Vision Transformer model and caches it."""
    global _vision_classifier
    
    if _vision_classifier is not None:
        return _vision_classifier
        
    print("Loading Radiology Vision Model... (This will take a minute on the first run)")
    
    # We use a highly accurate, pre-trained Vision model specifically fine-tuned for Chest X-Rays
    # This model predicts either "NORMAL" or "PNEUMONIA"
    _vision_classifier = pipeline(
        "image-classification", 
        model="nickmuchi/vit-finetuned-chest-xray-pneumonia"
    )
    
    return _vision_classifier

def analyze_xray(image_file):
    """
    Takes an uploaded image file, converts it, and runs it through the AI.
    """
    # 1. Load the model
    classifier = setup_vision_model()
    
    # 2. Open the image using Pillow (PIL)
    img = Image.open(image_file).convert('RGB')
    
    # 3. Analyze the image
    print("\n[👁️] AI is scanning the X-Ray...")
    results = classifier(img)
    
    return results