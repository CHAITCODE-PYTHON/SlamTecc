#Simulated SLAM Map
# This replaces the actual robot. You're simulating the map with Python.

# slam_map.py

class SemanticSLAMMap:
    def __init__(self):
        self.landmarks = {}  # label -> position (x, y, z simulated)
        self.raw_log = []  # for evaluation

    def add_landmark(self, raw_text, corrected_text, confidence, position):
        if corrected_text == "INVALID":
            return

        self.landmarks[corrected_text] = {
            "position": position,
            "confidence": confidence,
            "raw": raw_text
        }

        self.raw_log.append({
            "raw": raw_text,
            "corrected": corrected_text,
            "confidence": confidence,
            "position": position
        })

    def navigate_to(self, target):
        if target in self.landmarks:
            pos = self.landmarks[target]["position"]
            return f"Navigating to {target} at position {pos}"
        return f"Landmark '{target}' not found in map"

    def get_all_landmarks(self):
        return self.landmarks
