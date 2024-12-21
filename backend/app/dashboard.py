from dash import dcc, html, Input, Output
import dash
import pandas as pd
from sqlalchemy import create_engine
import os

# Configure the database connection
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)

# Initialize the Dash app
app = dash.Dash(__name__, title="Healthcare Dashboard")
server = app.server

# Layout for the dashboard
app.layout = html.Div(
    [
        html.H1("Healthcare Dashboard", style={"textAlign": "center"}),
        html.Div(
            [
                dcc.Dropdown(
                    id="metric-selector",
                    options=[
                        {"label": "Risk Distribution", "value": "risk_dist"},
                        {"label": "Heart Rate Trends", "value": "heart_rate_trend"},
                        {"label": "Average Blood Pressure", "value": "avg_bp"},
                    ],
                    value="heart_rate_trend",
                    style={"width": "50%"},
                )
            ],
            style={"textAlign": "center"},
        ),
        html.Div(id="graph-container", children=[dcc.Graph(id="metric-graph")]),
    ]
)


# Fetch patient data from the database
def fetch_data():
    query = "SELECT created_at, heart_rate, bp, risk_label FROM patients"
    with engine.connect() as conn:
        data = pd.read_sql(query, conn)
    data["created_at"] = pd.to_datetime(data["created_at"])
    data["systolic_bp"] = data["bp"].str.split("/").str[0].astype(int)
    return data


# Callback to update the graph based on the selected metric
@app.callback(Output("metric-graph", "figure"), [Input("metric-selector", "value")])
def update_graph(selected_metric):
    data = fetch_data()
    figure = {}

    if selected_metric == "heart_rate_trend":
        # Aggregate daily average heart rate
        avg_heart_rate = data.groupby(data["created_at"].dt.date)["heart_rate"].mean()

        # Create the figure
        figure = {
            "data": [
                {
                    "x": avg_heart_rate.index,
                    "y": avg_heart_rate.values,
                    "type": "line",
                    "name": "Average Heart Rate",
                }
            ],
            "layout": {
                "title": "Daily Average Heart Rate Over Time",
                "xaxis": {
                    "title": "Date",
                    "tickvals": list(
                        avg_heart_rate.index
                    ),  # Explicitly specify all dates
                    "ticktext": [
                        date.strftime("%b %d") for date in avg_heart_rate.index
                    ],  # Format dates for better readability
                    "tickangle": -45,  # Rotate labels for better fit
                },
                "yaxis": {"title": "Heart Rate (BPM)"},
            },
        }

    elif selected_metric == "risk_dist":
        # Risk Distribution (Bar Chart)
        risk_counts = data["risk_label"].value_counts()
        figure = {
            "data": [{"x": ["Low Risk", "High Risk"], "y": risk_counts, "type": "bar"}],
            "layout": {"title": "Risk Distribution"},
        }

    elif selected_metric == "avg_bp":
        # Average Blood Pressure (Line Chart)
        avg_bp = data.groupby(data["created_at"].dt.date)["systolic_bp"].mean()
        figure = {
            "data": [
                {
                    "x": avg_bp.index,
                    "y": avg_bp.values,
                    "type": "line",
                    "name": "Average Systolic BP",
                }
            ],
            "layout": {
                "title": "Average Blood Pressure Over Time",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Systolic Blood Pressure (mmHg)"},
            },
        }

    return figure


# Run the Dash app
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
