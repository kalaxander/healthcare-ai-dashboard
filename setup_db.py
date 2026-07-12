import sqlite3

def init_database():
    # Connect to SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create Patients Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            admission_date DATE NOT NULL
        )
    ''')

    # 2. Create Clinical Records Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clinical_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            condition TEXT NOT NULL,
            medication TEXT,
            status TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
        )
    ''')

    # Sample Data to Insert
    sample_patients = [
        ('Arjun Sharma', 62, 'Male', '2026-05-12'),
        ('Priya Patel', 45, 'Female', '2026-06-01'),
        ('Amit Verma', 71, 'Male', '2026-06-15'),
        ('Sneha Reddy', 29, 'Female', '2026-06-20'),
        ('Rohan Joshi', 55, 'Male', '2026-06-28')
    ]

    sample_records = [
        (1, 'Type 2 Diabetes', 'Metformin', 'Stable'),
        (2, 'Hypertension', 'Lisinopril', 'Recovering'),
        (3, 'Glaucoma', 'Timolol Maleate Drops', 'Critical'),
        (4, 'Asthma', 'Albuterol Inhaler', 'Stable'),
        (5, 'Type 2 Diabetes', 'Insulin', 'Critical')
    ]

    # Insert Data Safely
    cursor.executemany(
        "INSERT INTO patients (name, age, gender, admission_date) VALUES (?, ?, ?, ?)", 
        sample_patients
    )
    cursor.executemany(
        "INSERT INTO clinical_records (patient_id, condition, medication, status) VALUES (?, ?, ?, ?)", 
        sample_records
    )

    # Commit changes and close the connection
    conn.commit()
    print(f"Database successfully initialized with {len(sample_patients)} patient profiles.")
    conn.close()

if __name__ == "__main__":
    init_database()