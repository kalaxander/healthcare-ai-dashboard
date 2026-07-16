<div align="center">
  <h1>🏥 Intelligent Medical AI Dashboard</h1>
  <p><i>A privacy-preserving, 100% offline, multi-modal AI system for healthcare analytics & EHR.</i></p>

  <!-- Interactive Tech Stack Badges -->
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/HuggingFace-F9AB00?style=for-the-badge&logo=huggingface&logoColor=white" alt="HuggingFace" />
  <img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit" />
</div>

<hr>

## 📑 Quick Navigation
- [🏆 Project Overview](#-project-overview)
- [🧩 The 5 AI Pillars (Interactive)](#-the-5-ai-pillars)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 How to Run Locally](#-how-to-run-locally)

---

## 🏆 Project Overview

This dashboard acts as a comprehensive **"AI Assistant"** for doctors and hospital administrators. Modern medical AI often relies on public cloud APIs, creating massive HIPAA privacy vulnerabilities. **This project solves that by running entirely on local edge hardware.** 

It unifies Generative NLP, Machine Learning, and Computer Vision into a single, seamless Streamlit interface.

---

## 🧩 The 5 AI Pillars 
*(Click on any module below to expand and read how it works)*

<details>
<summary><b>1. 🗣️ Smart Voice Assistant (EHR & SQL)</b></summary>
<br>
A centralized command center utilizing <code>faster-whisper</code> and <code>Qwen 1.5B</code> for hands-free operations.
<ul>
<li><b>Voice EHR (Data Entry):</b> Doctors can dictate clinical notes (e.g., <i>"Update John Doe, he is now critical"</i>). The AI automatically finds the patient, extracts the condition/status, mentally corrects phonetic transcription errors, and appends the structured data to their medical history timeline.</li>
<li><b>Voice-to-SQL (Analytics):</b> Translates natural language questions into complex SQLite queries to instantly visualize hospital-wide statistics with automated bar charts.</li>
</ul>
</details>

<details>
<summary><b>2. 🧠 Predictive Diagnostics (Explainable AI)</b></summary>
<br>
Uses a <b>Random Forest Classifier</b> trained on the UCI Heart Disease dataset to predict cardiovascular risk based on patient vitals.
<ul>
<li><b>Solving the Black Box:</b> Integrates <b>SHAP</b> (SHapley Additive exPlanations) to generate Waterfall plots. This visually proves to doctors exactly <i>why</i> the AI made a specific prediction by calculating the marginal risk contribution of each vital sign.</li>
</ul>
</details>

<details>
<summary><b>3. 📊 Clinical Data Analyst (Unsupervised ML)</b></summary>
<br>
Acts as an automated Quality Assurance tool for hospital databases.
<ul>
<li>Uses an <b>Isolation Forest</b> algorithm to scan hundreds of thousands of hospital records in seconds.</li>
<li>Mathematically flags extreme clinical outliers and human data-entry errors for administrative review.</li>
</ul>
</details>

<details>
<summary><b>4. 📚 Medical Library (RAG Search)</b></summary>
<br>
A lightweight, offline Retrieval-Augmented Generation (RAG) engine.
<ul>
<li>Uses <b>TF-IDF and Cosine Similarity</b> to read unstructured PDF medical guidelines (like Asthma treatment protocols).</li>
<li>Accurately answers clinical questions based <i>only</i> on the provided text, eliminating LLM hallucinations.</li>
</ul>
</details>

<details>
<summary><b>5. 🩻 Radiology Vision Engine (Computer Vision)</b></summary>
<br>
Brings deep learning image analysis directly to the dashboard.
<ul>
<li>Uses a fine-tuned <b>Vision Transformer (ViT)</b> to analyze Chest X-Ray images.</li>
<li>Predicts the presence of Pneumonia lung opacities with statistical confidence levels.</li>
</ul>
</details>

---

## 🛠️ Tech Stack

| Category | Technology Used |
| :--- | :--- |
| **Frontend UI** | Streamlit |
| **Database** | SQLite3, Pandas |
| **Machine Learning** | Scikit-Learn (Random Forest, Isolation Forest) |
| **Deep Learning** | PyTorch, HuggingFace Transformers (Qwen2.5-Coder) |
| **Audio NLP** | Faster-Whisper |
| **Computer Vision** | PIL, Vision Transformer (ViT) |
| **Explainable AI** | SHAP |

---

## 🚀 How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt