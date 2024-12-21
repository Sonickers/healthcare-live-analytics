import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://admin:admin@localhost:5432/healthcare_analytics"
engine = create_engine(DATABASE_URL)

def prepare_data():
    with engine.connect() as conn:
        query = text("SELECT heart_rate, bp, risk_label FROM patients")
        data = pd.read_sql(query, conn)
    
    data['systolic_bp'] = data['bp'].str.split('/').str[0].astype(int)

    X = data[['heart_rate', 'systolic_bp']]
    y = data['risk_label']

    return X, y

if __name__ == "__main__":
    X, y = prepare_data()
    print("Features (X):\n", X.head())
    print("Target (y):\n", y.head())
