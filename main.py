import requests
import os
from datetime import datetime

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
TOKEN = os.environ.get("TOKEN")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
exercise_config = {
    "query": input("Tell me which exercises you did: ")
}
response = requests.post(url=exercise_endpoint, json=exercise_config, headers=headers)

today = datetime.now()
today_date = today.strftime("%m/%d/%Y")
today_time = today.strftime("%X")

sheet_headers = {
    "Authorization": f"Bearer {TOKEN}"
}

for exercise in response.json()["exercises"]:
    sheets_config = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    sheet_response = requests.post(url=SHEET_ENDPOINT, json=sheets_config, headers=sheet_headers)
    sheet_response.raise_for_status()
