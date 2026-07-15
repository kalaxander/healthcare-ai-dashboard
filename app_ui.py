import streamlit as st
import sqlite3
import pandas as pd
import sys
import joblib
import shap
import matplotlib.pyplot as plt
import numpy as np
import time

try:
    from app_controller import get_database_schema, extract_sql, DB_PATH
except Exception as e:
    st.error("⚠️ Could not import `app_controller.py`.")
    st.stop()

try:
    from llm_engine import generate_sql_response, generate_rag_response, extract_patient_entities
except ImportError:
    pass

try:
    from voice_engine import transcribe_audio
except ImportError:
    pass

try:
    from vision_engine import analyze_xray
except ImportError:
    st.warning("⚠️ `vision_engine.py` not found. Radiology tab will be disabled.")
    def analyze_xray(img): return None

def execute_query_to_df(query):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return str(e)

st.set_page_config(page_title="Medical AI Dashboard", page_icon="🏥", layout="wide")

st.title("🏥 Intelligent Medical AI Dashboard")
st.markdown("A privacy-preserving, local AI system handling natural language queries, predictive diagnostics, and clinical insights.")

if 'ehr_form_data' not in st.session_state:
    st.session_state.ehr_form_data = {"name": "", "age": 30, "gender": "Unknown", "condition": "", "status": "Stable"}

# Create the Multi-Tab Layout (Exactly 5 tabs now)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗣️ Smart Voice Assistant (EHR & SQL)", 
    "🧠 Predictive Diagnostics", 
    "📊 Clinical Analyst", 
    "📚 Medical Library (RAG)",
    "🩻 Radiology (Vision)"
])

# ==========================================
# TAB 1: Smart Voice Assistant (EHR + SQL)
# ==========================================
with tab1:
    # ------------------------------------------
    # PART A: VOICE EHR (Data Entry)
    # ------------------------------------------
    st.header("📝 Part 1: Voice EHR & Patient Management")
    st.markdown("Dictate a note like: *'Update [Name], their asthma is critical'* to auto-pull their history and append a note.")

    try:
        conn = sqlite3.connect(DB_PATH)
        patients_df = pd.read_sql_query("SELECT * FROM patients", conn)
        
        patient_options = ["➕ Register New Patient"]
        patient_mapping = {}
        
        if not patients_df.empty:
            for _, row in patients_df.iterrows():
                display_str = f"ID {row['patient_id']}: {row['name']} ({row['age']}y, {row['gender']})"
                patient_options.append(display_str)
                patient_mapping[display_str] = row
    except Exception as e:
        st.error(f"Error loading database: {e}")
        patient_options = ["➕ Register New Patient"]
        patient_mapping = {}

    if 'patient_selector' not in st.session_state:
        st.session_state.patient_selector = patient_options[0]

    ehr_audio = st.audio_input("🎙️ Dictate Patient Details / New Note", key="ehr_audio")
    
    if ehr_audio is not None:
        current_audio_hash = hash(ehr_audio.getvalue())
        if 'last_audio_hash' not in st.session_state or st.session_state.last_audio_hash != current_audio_hash:
            st.session_state.last_audio_hash = current_audio_hash
            
            with open("temp_ehr_audio.wav", "wb") as f:
                f.write(ehr_audio.getvalue())
            
            with st.spinner("🎵 Transcribing and extracting clinical entities..."):
                transcribed_ehr_text = transcribe_audio("temp_ehr_audio.wav")
                
                if transcribed_ehr_text:
                    st.success(f"**Heard:** \"{transcribed_ehr_text}\"")
                    
                    extracted_data = extract_patient_entities(transcribed_ehr_text)
                    extracted_name = extracted_data.get('name', '')
                    
                    matched_option = "➕ Register New Patient"
                    if extracted_name and extracted_name.lower() != 'unknown':
                        for opt in patient_options:
                            if opt != "➕ Register New Patient":
                                db_name = patient_mapping[opt]['name']
                                if extracted_name.lower() in db_name.lower() or db_name.lower() in extracted_name.lower():
                                    matched_option = opt
                                    break
                    
                    st.session_state.patient_selector = matched_option
                    
                    st.session_state.ehr_form_data['name'] = extracted_name
                    try:
                        st.session_state.ehr_form_data['age'] = int(extracted_data.get('age', 30))
                    except:
                        st.session_state.ehr_form_data['age'] = 30
                    st.session_state.ehr_form_data['gender'] = extracted_data.get('gender', 'Unknown')
                    st.session_state.ehr_form_data['condition'] = extracted_data.get('condition', '')
                    st.session_state.ehr_form_data['status'] = extracted_data.get('status', 'Stable')

    selected_option = st.selectbox("Select Patient to Update, or Register New:", patient_options, key="patient_selector")
    selected_patient_id = None
    
    if selected_option != "➕ Register New Patient":
        patient_info = patient_mapping[selected_option]
        selected_patient_id = patient_info['patient_id']
        st.info(f"📂 **Viewing Medical File For:** {patient_info['name']}")
        
        try:
            history_df = pd.read_sql_query(f"SELECT record_id, condition, status FROM clinical_records WHERE patient_id = {selected_patient_id}", conn)
            if not history_df.empty:
                st.dataframe(history_df, use_container_width=True, hide_index=True)
            else:
                st.write("No past clinical records found.")
        except Exception as e:
            st.error(f"Error fetching history: {e}")

    try:
        conn.close()
    except:
        pass

    form_name = patient_info['name'] if selected_patient_id else st.session_state.ehr_form_data['name']
    form_age = int(patient_info['age']) if selected_patient_id else st.session_state.ehr_form_data['age']
    form_gender = patient_info['gender'] if selected_patient_id else st.session_state.ehr_form_data['gender']
    
    with st.form("ehr_form"):
        colA, colB = st.columns(2)
        with colA:
            f_name = st.text_input("Patient Name", value=form_name, disabled=bool(selected_patient_id))
            f_age = st.number_input("Age", min_value=0, max_value=120, value=form_age, disabled=bool(selected_patient_id))
            
            gen_options = ["Male", "Female", "Other", "Unknown"]
            gen_val = form_gender.capitalize()
            f_gender = st.selectbox("Gender", gen_options, index=gen_options.index(gen_val) if gen_val in gen_options else 3, disabled=bool(selected_patient_id))
            
        with colB:
            f_condition = st.text_input("Primary Condition (New Note)", value=st.session_state.ehr_form_data['condition'])
            
            status_options = ["Stable", "Critical", "In Surgery", "Discharged", "Under Observation"]
            stat_val = st.session_state.ehr_form_data['status'].title()
            f_status = st.selectbox("Current Status", status_options, index=status_options.index(stat_val) if stat_val in status_options else 0)

        btn_text = f"💾 Append Note to {form_name}'s File" if selected_patient_id else "💾 Register New Patient & Save"
        submitted = st.form_submit_button(btn_text)
        
        if submitted:
            if f_name and f_condition:
                try:
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    
                    if selected_patient_id:
                        cursor.execute("INSERT INTO clinical_records (patient_id, condition, status) VALUES (?, ?, ?)", (selected_patient_id, f_condition, f_status))
                        conn.commit()
                        st.success(f"✅ Successfully added a new clinical note for {f_name}!")
                    else:
                        cursor.execute("INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)", (f_name, f_age, f_gender))
                        new_patient_id = cursor.lastrowid
                        cursor.execute("INSERT INTO clinical_records (patient_id, condition, status) VALUES (?, ?, ?)", (new_patient_id, f_condition, f_status))
                        conn.commit()
                        st.success(f"✅ Successfully registered {f_name} and saved first record! (ID: {new_patient_id})")
                    
                    conn.close()
                    st.balloons()
                    
                    st.session_state.ehr_form_data = {"name": "", "age": 30, "gender": "Unknown", "condition": "", "status": "Stable"}
                    if 'last_audio_hash' in st.session_state:
                        del st.session_state['last_audio_hash']
                    st.rerun() 
                    
                except Exception as e:
                    st.error(f"Database Error: {e}")
            else:
                st.warning("⚠️ Name and Condition are required fields.")

    st.divider()

    # ------------------------------------------
    # PART B: VOICE-TO-SQL (Analytics)
    # ------------------------------------------
    st.header("📊 Part 2: Database Analytics & Querying")
    with st.expander("📂 View Database Schema (What you can ask about)"):
        st.code(get_database_schema(), language="sql")

    audio_value = st.audio_input("🎙️ Speak your analytical query (e.g., 'Average age of patients')", key="sql_audio") 
    query_text = st.text_input("💬 Or type your query:", placeholder="e.g., Show me the average cholesterol by sex")

    final_query = query_text 

    if audio_value is not None:
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_value.getbuffer())
        with st.spinner("🎵 Transcribing audio..."):
            transcribed_text = transcribe_audio("temp_audio.wav")
            if transcribed_text:
                st.success(f"**Heard:** \"{transcribed_text}\"")
                final_query = transcribed_text

    if st.button("Generate & Execute SQL", type="primary"):
        if final_query:
            with st.spinner("🧠 Qwen2.5-Coder is thinking..."):
                schema = get_database_schema()
                prompt = f"""You are an expert SQL assistant. Given the following SQLite database schema:
                {schema}
                Write a valid SQLite query to answer the following request:
                "{final_query}"
                IMPORTANT: Return ONLY the SQL code. Use LOWER() on text comparisons.
                """
                
                raw_response = generate_sql_response(prompt)
                sql_query = extract_sql(raw_response)
                
                if sql_query:
                    st.success("Query generated successfully!")
                    st.code(sql_query, language="sql")
                    
                    st.subheader("📊 Query Results")
                    results = execute_query_to_df(sql_query)
                    
                    if isinstance(results, pd.DataFrame):
                        if results.empty:
                            st.info("The query executed successfully, but no records found.")
                        else:
                            st.dataframe(results, use_container_width=True, hide_index=True)
                            
                            csv = results.to_csv(index=False).encode('utf-8')
                            st.download_button("📥 Download Results as CSV", data=csv, file_name='medical_query_results.csv', mime='text/csv')
                            
                            if len(results.columns) >= 2:
                                numeric_cols = results.select_dtypes(include=['number']).columns.tolist()
                                cat_cols = results.select_dtypes(include=['object', 'string', 'category']).columns.tolist()
                                
                                if numeric_cols and cat_cols:
                                    st.subheader("📈 Data Visualization")
                                    chart_data = results.set_index(cat_cols[0])[numeric_cols[0]]
                                    st.bar_chart(chart_data)
                    else:
                        st.error(f"SQL Execution Error: {results}")

# ==========================================
# TAB 2: Predictive Diagnostics 
# ==========================================
with tab2:
    st.subheader("Cardiovascular Risk Prediction (Explainable AI)")
    st.markdown("Enter a patient's clinical vitals. The AI will predict their heart disease risk and **explain its reasoning visually.**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age_input = st.slider("Age", 20, 100, 50)
        sex_input = st.selectbox("Sex", ["Male", "Female"])
        sex_val = 1 if sex_input == "Male" else 0
        
    with col2:
        cp_input = st.selectbox("Chest Pain Type (1-4)", [1, 2, 3, 4])
        trestbps_input = st.number_input("Resting Blood Pressure (mm Hg)", 90, 200, 120)
        
    with col3:
        chol_input = st.number_input("Cholesterol (mg/dl)", 100, 600, 200)
        thalach_input = st.slider("Max Heart Rate Achieved", 60, 220, 150)
        exang_input = st.selectbox("Exercise Induced Angina?", ["No", "Yes"])
        exang_val = 1 if exang_input == "Yes" else 0
        
    if st.button("Predict Patient Risk", type="primary"):
        try:
            model = joblib.load("heart_disease_model.pkl")
            input_features = ['age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol', 'max_heart_rate', 'exercise_induced_angina']
            input_data = pd.DataFrame([[age_input, sex_val, cp_input, trestbps_input, chol_input, thalach_input, exang_val]], columns=input_features)
            
            prob = model.predict_proba(input_data)[0][1] 
            st.divider()
            
            if prob > 0.5:
                st.error(f"⚠️ **High Risk of Heart Disease** (Probability: {prob*100:.1f}%)")
            else:
                st.success(f"✅ **Low Risk of Heart Disease** (Probability: {prob*100:.1f}%)")
                
            st.subheader("Why did the AI make this prediction?")
            with st.spinner("Generating Explainable AI graph..."):
                explainer = shap.Explainer(model)
                shap_obj = explainer(input_data)
                
                fig, ax = plt.subplots(figsize=(8, 4))
                
                if len(shap_obj.values.shape) == 3:
                    shap.plots.waterfall(shap_obj[0, :, 1], show=False)
                else:
                    shap.plots.waterfall(shap_obj[0], show=False)
                
                fig.patch.set_facecolor('none')
                ax.set_facecolor('none')
                st.pyplot(fig)
                
        except FileNotFoundError:
            st.error("Model file not found! Please run `python train_ml_model.py` first.")

# ==========================================
# TAB 3: Clinical Analyst (Isolation Forest)
# ==========================================
with tab3:
    st.subheader("🕵️‍♀️ Automated Data Anomaly Detection")
    st.markdown("Uses Unsupervised Machine Learning (**Isolation Forest**) to scan thousands of hospital records and flag mathematical outliers, data-entry errors, or extreme clinical cases.")
    
    table_choice = st.selectbox("Select Database Table to Scan:", ["heart_disease_records", "diabetes_records"])
    
    if st.button(f"Scan {table_choice} for Anomalies", type="primary"):
        with st.spinner("Scanning records with Isolation Forest..."):
            try:
                conn = sqlite3.connect(DB_PATH)
                df = pd.read_sql_query(f"SELECT * FROM {table_choice}", conn)
                conn.close()
                
                if df.empty:
                    st.warning("No data found in this table.")
                else:
                    numeric_df = df.select_dtypes(include=['number']).dropna()
                    
                    if numeric_df.empty:
                        st.warning("No numeric columns available to scan.")
                    else:
                        from sklearn.ensemble import IsolationForest
                        iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
                        numeric_df['anomaly_score'] = iso_forest.fit_predict(numeric_df)
                        anomalies = df.loc[numeric_df[numeric_df['anomaly_score'] == -1].index]
                        
                        st.error(f"🚨 **Scan Complete!** Found {len(anomalies)} anomalous records out of {len(df)} total records.")
                        
                        if not anomalies.empty:
                            st.dataframe(anomalies, use_container_width=True)
                            csv_anomalies = anomalies.to_csv(index=False).encode('utf-8')
                            st.download_button("📥 Download Anomalies Report (CSV)", data=csv_anomalies, file_name=f'{table_choice}_anomalies.csv', mime='text/csv')
            except Exception as e:
                st.error(f"Error scanning data: {e}")

# ==========================================
# TAB 4: Medical Library (RAG)
# ==========================================
with tab4:
    st.subheader("📚 Medical Library (RAG)")
    st.markdown("Upload medical guidelines, research papers, or clinical notes as PDFs. The AI will read them and answer your questions directly from the text!")

    import PyPDF2
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    uploaded_file = st.file_uploader("Upload a Medical PDF", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("Extracting and indexing document..."):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_chunks = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    paragraphs = text.split('\n\n')
                    for p in paragraphs:
                        if len(p.strip()) > 50:
                            text_chunks.append(p.strip())
            
            if text_chunks:
                st.success(f"✅ Document indexed successfully! ({len(text_chunks)} text chunks extracted)")
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(text_chunks)
                
                user_q = st.text_input("💬 Ask a question about this document:")
                
                if st.button("Ask AI", type="primary", key="rag_btn"):
                    if user_q:
                        with st.spinner("Searching document & reading context..."):
                            q_vec = vectorizer.transform([user_q])
                            similarities = cosine_similarity(q_vec, tfidf_matrix).flatten()
                            best_idx = np.argmax(similarities)
                            best_score = similarities[best_idx]
                            
                            if best_score > 0.05:
                                best_context = text_chunks[best_idx]
                                try:
                                    answer = generate_rag_response(best_context, user_q)
                                    st.markdown("### 🤖 AI Response:")
                                    st.info(answer)
                                    with st.expander("🔍 View Exact Source Paragraph (For Verification)"):
                                        st.write(best_context)
                                        st.caption(f"Mathematical Confidence Score: {best_score:.2f}")
                                except Exception as e:
                                    st.error(f"Error communicating with LLM: {e}")
                            else:
                                st.warning("I couldn't find any relevant information in this document to answer your specific question.")
            else:
                st.error("Could not extract any readable text from this PDF.")

# ==========================================
# TAB 5: Radiology (Vision Engine)
# ==========================================
with tab5:
    st.subheader("🩻 Radiological Image Analysis")
    st.markdown("Upload a Chest X-Ray image. Our specialized Vision Transformer (ViT) will scan the lungs for signs of Pneumonia.")
    
    xray_upload = st.file_uploader("Upload Chest X-Ray", type=["jpg", "jpeg", "png"])
    
    if xray_upload is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(xray_upload, caption="Uploaded Patient X-Ray", use_container_width=True)
            
        with col2:
            st.markdown("### AI Diagnostic Results")
            if st.button("Scan X-Ray", type="primary", use_container_width=True):
                with st.spinner("🧠 Vision Transformer analyzing lung opacities..."):
                    try:
                        results = analyze_xray(xray_upload)
                        
                        if results:
                            top_prediction = results[0]['label']
                            confidence = results[0]['score'] * 100
                            
                            st.divider()
                            if top_prediction.upper() == "PNEUMONIA":
                                st.error(f"🚨 **DETECTED: {top_prediction.upper()}**")
                                st.progress(results[0]['score'])
                                st.caption(f"Confidence Level: {confidence:.2f}%")
                                st.markdown("*Recommendation: Urgent clinical review and potential antibiotic therapy.*")
                            else:
                                st.success(f"✅ **DETECTED: NORMAL (Healthy Lungs)**")
                                st.progress(results[0]['score'])
                                st.caption(f"Confidence Level: {confidence:.2f}%")
                                st.markdown("*Observation: No significant lung opacities detected.*")
                    except Exception as e:
                        st.error(f"Error during image analysis: {e}")