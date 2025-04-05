from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
CORS(app)

def preprocess_csv():
    df = pd.read_csv("data.csv")
    df["Time"] = pd.to_datetime(df["Time"], errors='coerce')
    df.dropna(subset=["Time"], inplace=True)
    df["Year"] = df["Time"].dt.year

    language_trends = df.groupby(["Year", "Tag"]).size().unstack(fill_value=0)
    if language_trends.empty:
        return pd.DataFrame()

    latest_year = language_trends.index.max()
    top_languages = language_trends.loc[latest_year].nlargest(10).index.tolist()
    filtered_data = language_trends[top_languages]

    yearly_totals = filtered_data.sum(axis=1)
    normalized_data = filtered_data.div(yearly_totals, axis=0) * 100

    normalized_data.to_csv("normalized_data.csv")
    return normalized_data

if not os.path.exists("normalized_data.csv"):
    preprocess_csv()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/data')
def get_data():
    try:
        df = pd.read_csv("normalized_data.csv", index_col=0)
        return jsonify({
            "years": df.index.astype(str).tolist(),
            "languages": df.to_dict(orient="list")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
