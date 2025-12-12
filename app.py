from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load city dataset
cities = pd.read_excel("cities.xlsx")

# ✅ NEW ROUTE FOR EXPLORE PAGE (GET ALL CITIES)
@app.route("/all", methods=["GET"])
def get_all_cities():
    df = cities.copy()

    result = df[[
        "City",
        "State",
        "Avg Budget per Day (INR)",
        "Avg Tourist Rating",
        "Best Visiting Season",
        "Climate Type",
        "Speciality"
    ]]

    return jsonify(result.to_dict(orient="records"))

# ✅ EXISTING RECOMMEND ROUTE (FOR HOME PAGE)
@app.route("/", methods=["POST"])
def recommend():
    data = request.json

    climate = data.get("climate")
    budget = data.get("budget")

    df = cities.copy()
    df["score"] = 0

    df.loc[df["Climate Type"].str.contains(climate, case=False, na=False), "score"] += 3
    df.loc[df["Avg Tourist Rating"] >= 4.0, "score"] += 2
    df.loc[df["Avg Budget per Day (INR)"] <= budget, "score"] += 2

    result = df.sort_values(by="score", ascending=False).head(6)

    output = result[[
        "City",
        "State",
        "Avg Budget per Day (INR)",
        "Avg Tourist Rating",
        "Best Visiting Season",
        "Speciality"
    ]].to_dict(orient="records")

    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
