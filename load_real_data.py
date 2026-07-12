import sqlite3
import pandas as pd
import os

DB_PATH = "healthcare.db"

def load_real_datasets():
    print("🏥 Initializing Real-World Academic Datasets...")
    
    # 1. Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Optional: Clear out the old mock tables so the AI focuses on the real data
    cursor.execute("DROP TABLE IF EXISTS patients")
    cursor.execute("DROP TABLE IF EXISTS clinical_records")
    print("🧹 Cleared old synthetic mock data.")

    # ---------------------------------------------------------
    # DATASET 1: Heart Disease (Cleveland)
    # ---------------------------------------------------------
    heart_file = "processed.cleveland.data"
    if os.path.exists(heart_file):
        print(f"❤️ Found {heart_file}! Processing Heart Disease dataset...")
        
        # The UCI heart disease dataset doesn't have headers, so we define them based on their documentation
        heart_columns = [
            "age", "sex", "chest_pain_type", "resting_blood_pressure", 
            "cholesterol", "fasting_blood_sugar", "resting_ecg", 
            "max_heart_rate", "exercise_induced_angina", "st_depression", 
            "slope", "num_major_vessels", "thalassemia", "heart_disease_target"
        ]
        
        df_heart = pd.read_csv(heart_file, names=heart_columns, na_values="?")
        
        # Make sex more readable for the AI (1 = Male, 0 = Female)
        df_heart['sex'] = df_heart['sex'].map({1.0: 'Male', 0.0: 'Female'})
        
        # Load into SQLite
        df_heart.to_sql("heart_disease_records", conn, if_exists="replace", index=False)
        print(f"✅ Successfully loaded {len(df_heart)} Heart Disease records!")
    else:
        print(f"⚠️ Warning: Could not find {heart_file}. Skipping.")

    # ---------------------------------------------------------
    # DATASET 2: Diabetes 130-US Hospitals
    # ---------------------------------------------------------
    diabetes_file = "diabetic_data.csv"
    if os.path.exists(diabetes_file):
        print(f"🩸 Found {diabetes_file}! Processing Diabetes dataset (This one is huge, give it a second)...")
        
        # Load the CSV, telling pandas that "?" means missing data (NaN)
        df_diabetes = pd.read_csv(diabetes_file, na_values="?")
        
        # Load into SQLite
        df_diabetes.to_sql("diabetes_records", conn, if_exists="replace", index=False)
        print(f"✅ Successfully loaded {len(df_diabetes)} Diabetes hospital records!")
    else:
        print(f"⚠️ Warning: Could not find {diabetes_file}. Skipping.")

    conn.close()
    print("\n🎉 Database upgrade complete! Your app is now powered by real academic data.")

if __name__ == "__main__":
    load_real_datasets()