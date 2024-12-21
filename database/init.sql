CREATE TABLE patients (
  id SERIAL PRIMARY KEY,
  patient_id INT NOT NULL,
  heart_rate INT,
  bp VARCHAR(10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE patients ADD COLUMN risk_label INT DEFAULT NULL;

ALTER TABLE patients
ADD CONSTRAINT unique_patient_id UNIQUE (patient_id);
