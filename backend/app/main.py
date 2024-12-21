from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
import os
from sklearn.linear_model import LogisticRegression
import numpy as np
import joblib

app = Flask(__name__)

# Database configuration
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)

# Model initialization and training
def train_model():
    with engine.connect() as conn:
        # Fetch data
        result = conn.execute(text("SELECT heart_rate, bp, risk_label FROM patients")).mappings()
        data = [dict(row) for row in result]

    # Prepare training data
    X_train = np.array([[row['heart_rate'], int(row['bp'].split('/')[0])] for row in data])
    y_train = np.array([row['risk_label'] for row in data])

    # Train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'model.pkl')
    return model

# Load model or train if not available
if os.path.exists('model.pkl'):
    model = joblib.load('model.pkl')
else:
    model = train_model()

@app.route('/patients', methods=['POST'])
def add_patient():
    try:
        data = request.json
        patient_id = data['patient_id']
        heart_rate = data['heart_rate']
        bp = int(data['bp'].split('/')[0])

        # Check if the patient_id already exists
        query_check = text("SELECT * FROM patients WHERE patient_id = :patient_id")
        with engine.connect() as conn:
            result = conn.execute(query_check, {"patient_id": patient_id}).fetchone()

        if result:
            return jsonify({"error": f"Patient with id {patient_id} already exists"}), 400

        # Predict risk label
        X_new = np.array([[heart_rate, bp]])
        prediction = int(model.predict(X_new)[0])

        # Insert patient into database
        query_insert = text(
            "INSERT INTO patients (patient_id, heart_rate, bp, risk_label) VALUES (:patient_id, :heart_rate, :bp, :risk_label)"
        )
        with engine.connect() as conn:
            conn.execute(query_insert, {**data, "risk_label": prediction})
            conn.commit()

        return jsonify({"message": "Patient added successfully!", "risk_level": "High Risk" if prediction == 1 else "Low Risk"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/patients', methods=['GET'])
def get_patients():
    try:
        # Fetch all patients from database
        query = text("SELECT * FROM patients")
        with engine.connect() as conn:
            result = conn.execute(query)
            patients = [dict(row) for row in result.mappings()]
        return jsonify(patients)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        heart_rate = data.get('heart_rate')
        bp = int(data.get('bp').split('/')[0])  # Extract systolic BP

        if heart_rate is None or bp is None:
            return jsonify({"error": "Invalid input"}), 400

        # Predict risk level
        X_new = np.array([[heart_rate, bp]])
        prediction = model.predict(X_new)[0]  # 0: Low Risk, 1: High Risk
        risk_level = "High Risk" if prediction == 1 else "Low Risk"
        return jsonify({"risk_level": risk_level})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrain', methods=['POST'])
def retrain():
    try:
        # Retrain the model
        global model
        model = train_model()
        return jsonify({"message": "Model retrained successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)