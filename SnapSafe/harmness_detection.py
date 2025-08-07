import numpy as np
import pandas as pd 
import pytesseract
import cv2
import pubchempy as pcp
from PIL import Image
import matplotlib.pyplot as plt
import ctypes
from pyzbar import pyzbar
from pyzbar import zbar_library
import joblib

from ensemble import MajorityVotingEnsemble 
label_encoder = joblib.load("label_encode_main.joblib")
vectorizer = joblib.load("tfidf_vectorizer_main.joblib")

def patch_ensemble(ensemble):
    if not hasattr(ensemble, "weights"):
        ensemble.weights = [1.0] * len(ensemble.models)
    if not hasattr(ensemble, "tie_breaker_order"):
        ensemble.tie_breaker_order = list(range(len(ensemble.models)))
    if not hasattr(ensemble, "n_classes"):
        ensemble.n_classes = None
    return ensemble
model = joblib.load("majority_ensemble.pkl")

dll_path = r"C:\Users\dhruv\AppData\Roaming\Python\Python311\site-packages\pyzbar\libzbar-64.dll"
zbar_library.load = lambda: ctypes.cdll.LoadLibrary(dll_path)

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\dhruv\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' #img->text

import spacy
nlp = spacy.load("en_ner_bc5cdr_md") #chemicals extraction

#preprocessing
import re

def preprocess_text(text):
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip().lower()
    return text

#prediction using model 
def predict_category_with_fallback(text, model, vectorizer, label_encoder, threshold=0.45):
    clean_text = preprocess_text(text)
    X_vec = vectorizer.transform([clean_text])
    
    proba = model.predict_proba(X_vec)[0]
    max_confidence = np.max(proba)
    predicted_index = np.argmax(proba)
    predicted_label = label_encoder.inverse_transform([predicted_index])[0]

    if max_confidence < threshold:
        return "others", max_confidence
    return predicted_label, max_confidence

harm_df=pd.read_csv("chemical_harmness_category.csv")
def calculate_harm_score(chemicals, category):
    
    category_col = f"harm_score_{category.lower()}"
    if category_col not in harm_df.columns:
        raise ValueError(f"Category '{category}' not found in harm score table.")
    
    individual_scores = {}
    for chem in chemicals:
        row = harm_df[harm_df['chemical_name'].str.lower() == chem.lower()]
        if not row.empty:
            score = row[category_col].values[0]
            individual_scores[chem] = score

    if not individual_scores:
        return {}, None, None  # No matching chemicals

    avg_score = sum(individual_scores.values()) / len(individual_scores)

    if avg_score <= 30:
        risk = "Low Risk"
    elif avg_score <= 70:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"
    return individual_scores, avg_score, risk

import requests
def get_general_product_info(barcode):
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode}"
    
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Failed to fetch data from UPCitemdb API.")
        return None
    
    data = response.json()
    
    if not data.get('items'):
        print("❌ No product found for this barcode.")
        return None

    item = data['items'][0]
    title = item.get('title', 'N/A')
    brand = item.get('brand', 'N/A')
    category = item.get('category', 'N/A')
    description = item.get('description', 'N/A')

    print(f"Product Title: {title}")
    print(f"Brand: {brand}")
    print(f"Category: {category}")
    print(f"Description: {description}")

    return {
        'title': title,
        'brand': brand,
        'category': category
    }

# Mapping category keywords to harm score columns
category_mapping = {
    'food': 'harm_score_food',
    'cosmetic': 'harm_score_cosmetic',
    'personal care': 'harm_score_personal_care',
    'cleaning': 'harm_score_cleaning',
    'stationery': 'harm_score_stationery',
    'household': 'harm_score_household',
    'medicine': 'harm_score_medicine',
    'others': 'harm_score_others'
}

# img_path="Screenshot 2025-06-08 161620.png" #live image 
# image=cv2.imread(img_path)

def process_barcode_image(gray, category_mapping, chemicals):
    if gray is None:
        print("❌ Upload proper image.")
        return None

    barcodes = pyzbar.decode(gray)

    if not barcodes:
        print("⚠️ No barcodes found.")
        return None

    barcode_results = []

    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        print(f"✅ Detected {barcode_type} barcode: {barcode_data}")

        url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={barcode_data}"
        response = requests.get(url)

        if response.status_code != 200:
            print("❌ Failed to fetch data from UPCitemdb API.")
            continue

        data = response.json()
        if not data.get('items'):
            print("❌ No product found for this barcode.")
            continue

        item = data['items'][0]
        title = item.get('title', 'N/A')
        brand = item.get('brand', 'N/A')
        category = item.get('category', 'N/A')
        description = item.get('description', 'N/A')

        print(f"🛍️ Product Title: {title}")
        print(f"🏢 Brand: {brand}")
        print(f"📂 Category: {category}")

        api_category = category
        matched_key = next((key for key in category_mapping if key in api_category.lower()), 'others')
        harm_score_column = category_mapping[matched_key]
        print(f"🔎 Using column: {harm_score_column}")

        filtered_df = harm_df[harm_df['chemical_name'].isin(chemicals)]

        if filtered_df.empty:
            print("⚠️ No matching chemicals found.")
            continue

        avg_score = filtered_df[harm_score_column].sum() / len(filtered_df)
        if avg_score <= 30:
            risk = "Low Risk"
        elif avg_score <= 70:
            risk = "Moderate Risk"
        else:
            risk = "High Risk"

        print(f"📉 Harm Score ({matched_key}): {avg_score:.2f}")
        print(f"⚠️ Risk Level: {risk}")

        barcode_results.append({
            "barcode_data": barcode_data,
            "barcode_type": barcode_type,
            "title": title,
            "brand": brand,
            "category": category,
            "harm_score": avg_score,
            "risk_level": risk
        })

    return barcode_results

def Harmness_Detection_function(img_path):
    try:
        # img_path="C:\\Users\\dhruv\\OneDrive\\Documents\\Desktop\\Neural\\Screenshot 2025-06-08 161620.png"
        image = cv2.imread(img_path)
        if image is None:
            print("❌ Failed to load image. Exiting.")
            return None

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        text = pytesseract.image_to_string(gray)
        clean_text = preprocess_text(text)

        doc = nlp(clean_text)
        chemicals = [ent.text for ent in doc.ents if ent.label_ == "CHEMICAL"]
        chemicals = list(set(chemicals))

        if len(chemicals) == 0:
            print("⚠️ No Chemicals detected.")
        else:
            print("🧪 Detected Chemicals:", chemicals)

        # ✅ Get barcode info
        barcode_info = process_barcode_image(gray, category_mapping, chemicals)

        # 🧠 ML category prediction
        category, confidence = predict_category_with_fallback(
            clean_text, model, vectorizer, label_encoder, threshold=0.45
        )

        # 📊 Harm score calculation
        individual_scores, avg_score, risk = calculate_harm_score(chemicals, category)

        print(f"🧠 Predicted Category: {category} | Confidence: {confidence:.2f}")
        print(f"📉 Avg Harm Score: {avg_score:.2f}%")
        print(f"⚠️ Risk Level: {risk}")
        print(f"📋 Individual Scores: {individual_scores}")

        return {
            "chemicals": chemicals,
            "category": category,
            "confidence": confidence,
            "individual_scores": individual_scores,
            "average_score": avg_score,
            "risk_level": risk,
            "barcode_info": barcode_info  # ✅ Included here
        }

    except Exception as e:
        print("❌ Error in detection pipeline:", str(e))
        return None
