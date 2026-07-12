import sqlite3
import random
from faker import Faker

# Initialize Faker (using Indian locale since you might be based in India based on timezone, but it works universally!)
fake = Faker('en_IN') 

DB_PATH = "healthcare.db"

# Medical data pools to randomly select from
CONDITIONS = [
    "Type 2 Diabetes", "Hypertension", "Asthma", "Glaucoma", 
    "Coronary Artery Disease", "Osteoarthritis", "Chronic Kidney Disease",
    "Migraine", "Pneumonia", "Covid-19"
]

STATUSES = [
    "Stable", "Critical", "In Surgery", "Discharged", "Under Observation"
]

GENDERS = ["Male", "Female", "Other"]

def generate_mock_data():
    """Generates 200 patients and 250 clinical records."""
    print("Connecting to healthcare.db...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Clearing old mock data...")
    cursor.execute("DELETE FROM clinical_records;")
    cursor.execute("DELETE FROM patients;")
    
    print("Generating 200 realistic patients...")
    patients_data = []
    for i in range(1, 201):
        # Generate realistic names based on gender
        gender = random.choice(GENDERS)
        if gender == "Male":
            name = fake.name_male()
        elif gender == "Female":
            name = fake.name_female()
        else:
            name = fake.name()
            
        age = random.randint(18, 95)
        
        patients_data.append((i, name, age, gender))
        
    cursor.executemany(
        "INSERT INTO patients (patient_id, name, age, gender) VALUES (?, ?, ?, ?)", 
        patients_data
    )
    
    print("Generating 250 clinical records...")
    records_data = []
    for i in range(1, 251):
        # Randomly assign this record to one of our 200 patients
        patient_id = random.randint(1, 200)
        condition = random.choice(CONDITIONS)
        status = random.choice(STATUSES)
        
        records_data.append((i, patient_id, condition, status))
        
    cursor.executemany(
        "INSERT INTO clinical_records (record_id, patient_id, condition, status) VALUES (?, ?, ?, ?)", 
        records_data
    )
    
    conn.commit()
    conn.close()
    print("✅ Successfully injected 200 patients and 250 clinical records into the database!")

if __name__ == "__main__":
    generate_mock_data()