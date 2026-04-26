# main.py
import os
from ocr_module import detect_text
from tecc_module import correct_text, query_map
from slam_map import SemanticSLAMMap
from evaluate import generate_results

# Simulated 3D positions (x, y, z) for each image
SIMULATED_POSITIONS = [
    (1.0, 0.0, 0.0),
    (2.5, 1.0, 0.0),
    (4.0, 1.0, 0.0),
    (5.5, 2.0, 0.0),
    (7.0, 2.0, 0.0),
    (8.5, 3.0, 0.0),
    (10.0, 3.0, 0.0),
    (11.5, 4.0, 0.0),
    (13.0, 4.0, 0.0),
    (14.5, 5.0, 0.0),
]

IMAGE_FOLDER = "images"
slam_map = SemanticSLAMMap()

image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.jpg','.jpeg','.png', '.webp', '.jfif'))]
print("=== Running TECC-Enhanced SLAM ===\n")

for i, img_file in enumerate(image_files):
    path = os.path.join(IMAGE_FOLDER, img_file)
    print(f"\nProcessing: {img_file}")

    detections = detect_text(path)
    position = SIMULATED_POSITIONS[i % len(SIMULATED_POSITIONS)]

    for det in detections:
        raw = det["raw_text"]
        conf = det["confidence"]

        # Skip pure numbers
        if raw.strip().isdigit():
            continue

        # Skip single characters
        if len(raw.strip()) <= 1:
            continue

        corrected = correct_text(raw, conf)

        print(f"  Raw: '{raw}' | Corrected: '{corrected}' | Conf: {conf}")
        slam_map.add_landmark(raw, corrected, conf, position)

# Test navigation query
print("\n=== Testing Navigation Query ===")
landmark_names = list(slam_map.get_all_landmarks().keys())
if landmark_names:
    result = query_map(slam_map.get_all_landmarks(), "take me to emergency")
    nav = slam_map.navigate_to(result)
    print(nav)

# Generate results
print("\n=== Generating Results ===")
generate_results(slam_map.raw_log)
print("\nDone. Check the results/ folder.")
