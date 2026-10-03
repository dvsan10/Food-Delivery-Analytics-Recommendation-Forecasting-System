from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI(
    title="Food Delivery Recommendation API",
    description="Food recommendation API using Apriori association rules",
    version="1.0"
)


# --------------------------------------------------
# Locate recommendations.csv
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# When running normally from VS Code
local_file = os.path.join(
    BASE_DIR,
    "..",
    "Outputs",
    "recommendations.csv"
)

# When running inside Docker
docker_file = os.path.join(
    BASE_DIR,
    "Outputs",
    "recommendations.csv"
)


if os.path.exists(local_file):
    RECOMMENDATION_FILE = local_file

elif os.path.exists(docker_file):
    RECOMMENDATION_FILE = docker_file

else:
    RECOMMENDATION_FILE = None


# --------------------------------------------------
# Load recommendation data
# --------------------------------------------------

if RECOMMENDATION_FILE:

    recommendations_df = pd.read_csv(
        RECOMMENDATION_FILE
    )

else:

    recommendations_df = pd.DataFrame(
        columns=[
            "FoodItem",
            "Recommendations"
        ]
    )


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Food Delivery Recommendation API is running",
        "status": "success"
    }


# --------------------------------------------------
# Recommendation endpoint
# --------------------------------------------------

@app.get("/recommend/{food_item}")
def recommend(food_item: str):

    food_item = food_item.strip()

    result = recommendations_df[
        recommendations_df["FoodItem"]
        .str.lower()
        == food_item.lower()
    ]

    if result.empty:

        raise HTTPException(
            status_code=404,
            detail=f"No recommendations found for '{food_item}'"
        )

    recommendations = result.iloc[0]["Recommendations"]

    if pd.isna(recommendations) or not str(recommendations).strip():

        return {
            "food_item": result.iloc[0]["FoodItem"],
            "recommendations": []
        }

    recommendation_list = [
        item.strip()
        for item in str(recommendations).split(",")
        if item.strip()
    ]

    return {
        "food_item": result.iloc[0]["FoodItem"],
        "recommendations": recommendation_list
    }