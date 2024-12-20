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
  - pandas: For data manipulation.
  - sqlalchemy: For database interaction.
  - scikit-learn: For building machine learning models.
- Tools:
  - Docker: For containerized deployment.
  - GitHub: For version control.

## 📂 Directory Structure

```plaintext
healthcare-live-analytics/
├── backend/
│   ├── app/
│   │   ├── main.py            # Flask application entry point
│   │   └── requirements.txt   # Python dependencies
│   ├── Dockerfile             # Backend Dockerfile
├── database/
│   └── init.sql               # Database schema initialization
├── kafka/                     # Placeholder for Kafka configuration
├── .env                       # Environment variables
├── docker-compose.yml         # Docker Compose configuration
├── README.md                  # Documentation for the project
└── .gitignore                 # Git ignore file
```
