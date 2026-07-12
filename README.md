# 🏥 Intelligent Medical AI Dashboard

A privacy-preserving, offline, multi-modal AI system for healthcare analytics, predictive diagnostics, and clinical insights.

## 🏆 Project Overview
This dashboard acts as a comprehensive "AI Assistant" for doctors and hospital administrators. It runs 100% locally to ensure patient data privacy (simulating HIPAA compliance) and combines 5 major pillars of modern Artificial Intelligence:

1. **🗣️ Voice-to-SQL (NLP & Generative AI):** Uses `faster-whisper` for audio transcription and a local `Qwen 1.5B` LLM to translate natural language into complex SQLite queries.
2. **🧠 Predictive Diagnostics (Supervised ML):** Uses a Random Forest model trained on the UCI Heart Disease dataset to predict cardiovascular risk based on patient vitals.
3. **📈 Explainable AI (XAI):** Integrates `SHAP` (SHapley Additive exPlanations) to visually prove to doctors *why* the AI made a specific prediction, removing the "Black Box" effect.
4. **🕵️‍♀️ Clinical Data Analyst (Unsupervised ML):** Uses an `Isolation Forest` algorithm to scan hundreds of thousands of hospital records to automatically flag mathematical anomalies and data-entry errors.
5. **📚 Medical Library (RAG):** Uses TF-IDF and Cosine Similarity to read unstructured PDF medical guidelines and accurately answer questions based *only* on the provided text.
6. **🩻 Radiology Vision Engine:** Uses a Vision Transformer (ViT) to analyze Chest X-Ray images and predict the presence of Pneumonia.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Database:** SQLite & Pandas
* **Machine Learning:** Scikit-Learn (Random Forest, Isolation Forest)
* **Deep Learning / LLMs:** HuggingFace Transformers, PyTorch, Qwen2.5-Coder
* **Audio Processing:** Faster-Whisper
* **Computer Vision:** PIL, ViT Image Classification
* **Explainable AI:** SHAP

## 🚀 How to Run Locally

**1. Install Dependencies**
```bash
pip install -r requirements.txt
