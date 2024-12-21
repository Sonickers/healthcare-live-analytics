# 🩺 Project: Healthcare Live Analytics

This project is a real-time analytics platform for patient health monitoring and risk prediction. The platform ingests, processes, and analyzes healthcare data to provide insights such as risk levels, real-time patient metrics, and future predictions for healthcare professionals.

## 📖 Features
- Data Ingestion: Real-time ingestion of patient data into a PostgreSQL database using Flask and Python.
- Risk Prediction: Machine learning models to predict patient health risk levels.
- Metrics Examples:
  - Real-time health risk scores for patients.
  - Historical trends in patient vitals (heart rate, blood pressure).
  - Aggregated insights for healthcare providers.
- Scalability: Built with Docker to handle large-scale data simulations.
- Future Plans:
  - Interactive dashboard for visualizing patient health trends.
  - Advanced machine learning models for more accurate predictions.
  - Integration with IoT devices for live data streaming.

## 🛠️ Technologies Used

- Languages: Python, SQL
- Database: PostgreSQL
- Libraries:
  - `pandas`: For data manipulation.
  - `sqlalchemy`: For database interaction.
  - `scikit-learn`: For building machine learning models.
  - `dash`: For creating interactive dashboards.
  - `dash-bootstrap-components`: For styling Dash components.
  - `faker`: For generating mock data.
  - `numpy`: For numerical computations.
  - `joblib`: For saving and loading machine learning models.
- Tools:
  - Docker: For containerized deployment.
  - GitHub: For version control.

## 📂 Directory Structure

healthcare_analytics/
├── backend/
│   ├── app/
│   │   ├── __pycache__/          # Python cache files
│   │   ├── dashboard.py          # Dash-based visualization dashboard
│   │   ├── generate_data.py      # Script for generating mock data
│   │   ├── main.py               # Flask application entry point
│   │   ├── requirements.txt      # Python dependencies
│   │   ├── model.pkl             # Trained machine learning model
│   ├── Dockerfile                # Backend Dockerfile
├── database/
│   └── init.sql                  # Database schema initialization
├── kafka/                        # Placeholder for Kafka configurations
├── scripts/
│   ├── data_preparation.py       # Script for preparing training data
│   ├── db.sh                     # Shell script for managing the database
├── .env                          # Environment variables
├── .gitignore                    # Git ignore file
├── docker-compose.yml            # Docker Compose configuration
└── README.md                     # Documentation for the project
```
