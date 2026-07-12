import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

DB_PATH = "healthcare.db"

def train_and_save_model():
    print("🧠 Fetching Real Heart Disease Data from SQLite...")
    conn = sqlite3.connect(DB_PATH)
    
    # We will use the most common clinical features so the UI form isn't too cluttered
    query = """
    SELECT age, sex, chest_pain_type, resting_blood_pressure, 
           cholesterol, max_heart_rate, exercise_induced_angina, heart_disease_target 
    FROM heart_disease_records
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 1. Handle missing values (fill with median for simplicity)
    df = df.dropna()

    # 2. Convert 'sex' back to numeric (1=Male, 0=Female) for the ML math
    df['sex'] = df['sex'].map({'Male': 1, 'Female': 0})

    # 3. The target is 0 (No Disease) and 1-4 (Various stages of Disease)
    # Convert this to simple binary: 0 = Healthy, 1 = At Risk
    df['heart_disease_target'] = df['heart_disease_target'].apply(lambda x: 1 if x > 0 else 0)

    X = df.drop("heart_disease_target", axis=1)
    y = df["heart_disease_target"]

    print(f"📊 Training on {len(df)} patient records...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Random Forest is highly accurate and works beautifully with SHAP explainability
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"✅ Model trained successfully! Accuracy: {accuracy * 100:.2f}%")

    joblib.dump(model, "heart_disease_model.pkl")
    print("💾 Saved AI model to 'heart_disease_model.pkl'. Ready for Streamlit!")

if __name__ == "__main__":
    train_and_save_model()