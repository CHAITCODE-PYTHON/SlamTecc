# ocr_module.py

#This is your CNN perception layer from the paper.

import easyocr
import cv2

reader = easyocr.Reader(['en'])


def detect_text(image_path):
    image = cv2.imread(image_path)
    results = reader.readtext(image)

    detections = []
    for (bbox, text, confidence) in results:
        detections.append({
            "raw_text": text,
            "confidence": round(confidence, 3),
            "bbox": bbox
        })

    return detections

# What this gives you: raw noisy text like "Emergancy Rm", "EXIT→",
# "ICU ward 3" with confidence scores.
