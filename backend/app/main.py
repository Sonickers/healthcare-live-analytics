from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
import os
from sklearn.linear_model import LogisticRegression
import numpy as np

app = Flask(__name__)

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT heart_rate, bp, risk_label FROM patients")).mappings()
    data = [dict(row) for row in result]

X_train = np.array([[row['heart_rate'], int(row['bp'].split('/')[0])] for row in data])
y_train = np.array([row['risk_label'] for row in data])

model = LogisticRegression()
model.fit(X_train, y_train)

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    heart_rate = data['heart_rate']
    bp = int(data['bp'].split('/')[0])

    X_new = np.array([[heart_rate, bp]])
    prediction = int(model.predict(X_new)[0])

    query = text("INSERT INTO patients (patient_id, heart_rate, bp, risk_label) VALUES (:patient_id, :heart_rate, :bp, :risk_label)")
    with engine.connect() as conn:
        conn.execute(query, {**data, "risk_label": prediction})
        conn.commit()
    return jsonify({"message": "Patient added successfully!", "risk_level": "High Risk" if prediction == 1 else "Low Risk"}), 201


@app.route('/patients', methods=['GET'])
def get_patients():
    query = text("SELECT * FROM patients")
    with engine.connect() as conn:
        result = conn.execute(query)
        patients = [dict(row) for row in result.mappings()]
    return jsonify(patients)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    heart_rate = data.get('heart_rate')
    bp = int(data.get('bp').split('/')[0])  # Extract systolic BP
    
    if heart_rate is None or bp is None:
        return jsonify({"error": "Invalid input"}), 400

    X_new = np.array([[heart_rate, bp]])
    prediction = model.predict(X_new)[0]  # 0: Low Risk, 1: High Risk
    risk_level = "High Risk" if prediction == 1 else "Low Risk"
    return jsonify({"risk_level": risk_level})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)