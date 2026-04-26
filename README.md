# SlamTecc
TECC-Enhanced Text-Aware SLAM using EasyOCR for scene text detection and LLaMA 3.3 70B via Groq API for real-time OCR error correction before semantic map integration.

1. Get a free Groq API key from console.groq.com
2. Paste your key in tecc_module.py:
   client = Groq(api_key="your_key_here")
3. Install dependencies:
   pip install easyocr groq pandas matplotlib opencv-python pillow
4. Run:
   python main.py
