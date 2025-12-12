import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
cities = pd.read_excel("cities.xlsx")
users = pd.read_excel("users.xlsx")

def recommend_cities(user_id, top_n=5):
    user = users[users["User ID"] == user_id].iloc[0]

    preferred_climate = user["Preferred Climate"]
    preferred_budget = user["Budget Range (₹)"]

    filtered = cities.copy()

    # Simple content filtering
    filtered["score"] = 0

    filtered.loc[
        filtered["Climate Type"].str.contains(preferred_climate, case=False, na=False),
        "score"
    ] += 3

    filtered.loc[
        filtered["Avg Tourist Rating"] >= 4.0,
        "score"
    ] += 2

    filtered.loc[
        filtered["Avg Budget per Day (INR)"] <= 3000,
        "score"
    ] += 2

    recommendations = filtered.sort_values(by="score", ascending=False)

    result = recommendations[[
        "City",
        "State",
        "Avg Budget per Day (INR)",
        "Avg Tourist Rating",
        "Best Visiting Season",
        "Speciality"
    ]].head(top_n)

    return result.to_dict(orient="records")
