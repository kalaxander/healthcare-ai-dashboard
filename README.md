🏥 Intelligent Medical AI Dashboard

A privacy-preserving, offline, multi-modal AI system for healthcare analytics, predictive diagnostics, and clinical insights.

🏆 Project Overview

This dashboard acts as a comprehensive "AI Assistant" for doctors and hospital administrators. It runs 100% locally to ensure patient data privacy (simulating HIPAA compliance) and combines 5 major pillars of modern Artificial Intelligence:

🗣️ Smart Voice Assistant (EHR & SQL): A dual-purpose Generative NLP engine utilizing faster-whisper and Qwen 1.5B.

Voice EHR: Doctors can dictate clinical notes to automatically pull up patient histories and append structured data hands-free.

Voice-to-SQL: Translates natural language questions into complex SQLite queries to instantly visualize hospital-wide statistics.

🧠 Predictive Diagnostics (Explainable AI): Uses a Random Forest model trained on the UCI Heart Disease dataset to predict cardiovascular risk based on patient vitals. Integrates SHAP (SHapley Additive exPlanations) to visually prove to doctors why the AI made a specific prediction, removing the "Black Box" effect.

📊 Clinical Data Analyst (Unsupervised ML): Uses an Isolation Forest algorithm to scan hundreds of thousands of hospital records to automatically flag mathematical anomalies and data-entry errors.

📚 Medical Library (RAG): Uses TF-IDF and Cosine Similarity to read unstructured PDF medical guidelines and accurately answer questions based only on the provided text.

🩻 Radiology Vision Engine: Uses a Vision Transformer (ViT) to analyze Chest X-Ray images and predict the presence of Pneumonia.

🛠️ Tech Stack

Frontend: Streamlit

Database: SQLite & Pandas

Machine Learning: Scikit-Learn (Random Forest, Isolation Forest)

Deep Learning / LLMs: HuggingFace Transformers, PyTorch, Qwen2.5-Coder

Audio Processing: Faster-Whisper

Computer Vision: PIL, ViT Image Classification

Explainable AI: SHAP

🚀 How to Run Locally

1. Install Dependencies

pip install -r requirements.txt


2. Generate Local Databases
Since this project protects privacy, no real patient databases are stored on GitHub. You must generate the local SQLite database first:

python generate_data.py


(Optional: Run python load_real_data.py and python train_ml_model.py to initialize the real UCI datasets and train the ML models).

3. Launch the Dashboard

streamlit run app_ui.py
