🏥 Intelligent Medical AI Dashboard

A privacy-preserving, 100% offline, multi-modal AI system designed for healthcare analytics, predictive diagnostics, and clinical insights.

📑 Quick Navigation

🏆 Project Overview

🧩 The 5 AI Pillars (Interactive)

🛠️ Tech Stack

🚀 How to Run Locally

🏆 Project Overview

This dashboard acts as a comprehensive "AI Assistant" for doctors and hospital administrators. Modern medical AI often relies on public cloud APIs, creating massive HIPAA privacy vulnerabilities. This project solves that by running entirely on local edge hardware.

It unifies Generative NLP, Machine Learning, and Computer Vision into a single, seamless Streamlit interface.

🧩 The 5 AI Pillars

(Click on any module below to expand and read how it works)

🛠️ Tech Stack

Category

Technology Used

Frontend UI

Streamlit

Database

SQLite3, Pandas

Machine Learning

Scikit-Learn (Random Forest, Isolation Forest)

Deep Learning

PyTorch, HuggingFace Transformers (Qwen2.5-Coder)

Audio NLP

Faster-Whisper

Computer Vision

PIL, Vision Transformer (ViT)

Explainable AI

SHAP

🚀 How to Run Locally

1. Install Dependencies

pip install -r requirements.txt


2. Generate the Local Database

To ensure data privacy, no real patient databases are stored on GitHub. You must generate the local SQLite database first:

python generate_data.py


(Optional: Run python load_real_data.py to inject real UCI academic datasets for the anomaly scanner).

3. Launch the Dashboard

streamlit run app_ui.py
