# 📸 SnapSafe – AI-based Product Harmfulness Analyzer

SnapSafe is an intelligent, real-time **AI tool** that helps users assess the **harm score of daily-use products** simply by scanning product packaging — **from live camera or image upload**.
It combines OCR, barcode reading, chemical hazard analysis, and ML-based risk prediction to ensure consumers are better informed about what they're using on or in their bodies.

---

## 🧠 Why We Built It

Everyday products like cosmetics, food items, and household cleaners contain chemical ingredients that can be harmful. However, most users don't have the time (or expertise) to research each ingredient individually.

**SnapSafe bridges that gap** by providing:

* Fast and reliable **harm score analysis** of products
* **Live image capture** or **image upload** options
* A clear and accessible **risk category**: High, Medium, or Low Risk
---

## Tech Stack

| Layer                 | Tech/Library Used                 |
| --------------------- | --------------------------------- |
| Frontend (GUI)        | Streamlit                         |
| OCR (Text Extraction) | pytesseract, OpenCV               |
| Barcode Detection     | pyzbar                            |
| Chemical Analysis     | PubChemPy API                     |
| Ensemble ML Model     | Trained with joblib (loaded live) |
| Image Handling        | PIL, tempfile                     |
| Data Processing       | pandas, numpy                     |

---

##  How It Works (System Architecture)
```
User upload/take live image -> Text Extraction -> OCR -> Barcode Detection -> Chemicals Extraction -> Category Classification Based on Ml model & Barcode number (if available) -> Based on Category Harmness Score prediction -> Showcasing : Average score and other Details 
```

### 🔄 Step-by-Step Pipeline:

1. **Image Input**: Capture through webcam or upload manually
2. **OCR Module**: Extracts chemical names from the product image using `pytesseract` & `OpenCV`
3. **Barcode Detection**: Decodes product barcodes to optionally cross-validate product info
4. **Chemical Extraction**: Uses `PubChemPy` to fetch chemical toxicity data
5. **ML Ensemble Model**: Predicts harm score and category (Low, Medium, High Risk)
6. **Output**: User sees harm percentage, chemicals detected, and final prediction

---

## 🚀 How to Use SnapSafe (Streamlit Cloud)

### ▶️ Hosted Version (Recommended)
You can use SnapSafe **anytime, anywhere** by visiting the hosted Streamlit link:

> 📍 [https://snapsafe.streamlit.app](#) *(replace with real link after deployment)*

### ⚙️ Local Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/Bit-Bard/SnapSafe
   cd snapsafe
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   streamlit run snapsafe_app.py
   ```

---

## ✅ Requirements (Already Included)

* Python >= 3.8
* streamlit
* pytesseract
* opencv-python
* pyzbar
* pubchempy
* joblib
* numpy
* pandas
* Pillow

---

## 📬 Contact / Collaboration

Want to contribute, collaborate, or use SnapSafe in your company?
👉 Reach out via [LinkedIn](https://www.linkedin.com/in/dhruv-devaliya/)
Or fork the project and submit a pull request.



# Add img video and working link 
