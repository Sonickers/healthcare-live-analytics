from faker import Faker
from sqlalchemy import create_engine, text
import random
from datetime import datetime, timedelta
import os

# Configure the database connection
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)

# Initialize Faker
fake = Faker()


# Function to generate mock data
def generate_mock_data(num_records=100):
    data = []
    for _ in range(num_records):
        patient_id = random.randint(1, 50)  # Random patient IDs
        heart_rate = random.randint(60, 120)  # Random heart rate
        systolic_bp = random.randint(100, 180)  # Random systolic blood pressure
        diastolic_bp = random.randint(60, 120)  # Random diastolic blood pressure
        risk_label = random.choice([0, 1])  # Low Risk: 0, High Risk: 1
        created_at = fake.date_time_between(
            start_date="-30d", end_date="now"
        )  # Past 30 days
        bp = f"{systolic_bp}/{diastolic_bp}"
        data.append((patient_id, heart_rate, bp, risk_label, created_at))
    return data


# Insert data into the database
def insert_mock_data(data):
    query = text(
        "INSERT INTO patients (patient_id, heart_rate, bp, risk_label, created_at) VALUES (:patient_id, :heart_rate, :bp, :risk_label, :created_at)"
    )
    with engine.connect() as conn:
        for record in data:
            conn.execute(
                query,
                {
                    "patient_id": record[0],
                    "heart_rate": record[1],
                    "bp": record[2],
                    "risk_label": record[3],
                    "created_at": record[4],
                },
            )
        conn.commit()


if __name__ == "__main__":
    print("Generating mock data...")
    mock_data = generate_mock_data(100)  # Generate 100 records
    insert_mock_data(mock_data)
    print("Mock data inserted into the database!")
