from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

def preprocess_csv():
    df = pd.read_csv("data.csv")
    df["Time"] = pd.to_datetime(df["Time"])
    df["Year"] = df["Time"].dt.year

    language_trends = df.groupby(["Year", "Tag"]).size().unstack(fill_value=0)
    latest_year = language_trends.index.max()
    top_languages = language_trends.loc[latest_year].nlargest(10).index.tolist()
    filtered_data = language_trends[top_languages]

    yearly_totals = filtered_data.sum(axis=1)
    normalized_data = filtered_data.div(yearly_totals, axis=0) * 100
    normalized_data.to_csv("normalized_data.csv")
    return normalized_data

preprocess_csv()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data')
def get_data():
    df = pd.read_csv("normalized_data.csv", index_col=0)
    return jsonify({
        "years": df.index.astype(str).tolist(),
        "languages": df.to_dict(orient="list")
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
