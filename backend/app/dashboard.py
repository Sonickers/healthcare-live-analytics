import dash
from dash import dcc, html, Input, Output
import pandas as pd
from sqlalchemy import create_engine
import os

# Connect to the database
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)

# Initialize Dash app
app = dash.Dash(__name__, title="Healthcare Dashboard")
server = app.server  # Use Flask server for deployment compatibility

# Layout for the dashboard
app.layout = html.Div([
    html.H1("Healthcare Dashboard", style={"textAlign": "center"}),

    html.Div([
        dcc.Dropdown(
            id="metric-selector",
            options=[
                {"label": "Risk Distribution", "value": "risk_dist"},
                {"label": "Heart Rate Trends", "value": "heart_rate_trend"}
            ],
            value="risk_dist",
            style={"width": "50%"}
        )
    ], style={"textAlign": "center"}),

    html.Div(id="graph-container", children=[
        dcc.Graph(id="metric-graph")
    ])
])

# Fetch patient data from the database
def fetch_data():
    query = "SELECT created_at, heart_rate, bp, risk_label FROM patients ORDER BY created_at"
    with engine.connect() as conn:
        data = pd.read_sql(query, conn)
    data["created_at"] = pd.to_datetime(data["created_at"])
    return data

# Callback to update the graph based on the selected metric
@app.callback(
    Output("metric-graph", "figure"),
    [Input("metric-selector", "value")]
)
def update_graph(selected_metric):
    data = fetch_data()

    if selected_metric == "risk_dist":
        # Risk Distribution (Bar Chart)
        risk_counts = data["risk_label"].value_counts()
        figure = {
            "data": [
                {"x": ["Low Risk", "High Risk"], "y": risk_counts, "type": "bar"}
            ],
            "layout": {"title": "Risk Distribution"}
        }

    elif selected_metric == "heart_rate_trend":
        # Heart Rate Trends (Line Chart)
        figure = {
            "data": [
                {"x": data["created_at"], "y": data["heart_rate"], "type": "line", "name": "Heart Rate"}
            ],
            "layout": {"title": "Heart Rate Trends Over Time"}
        }

    return figure

# Run the Dash app
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
