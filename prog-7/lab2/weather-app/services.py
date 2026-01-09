from flask import Flask, request, jsonify
from multiprocessing import Process
import sqlite3
import requests
import os

# --------------------------
# Weather Service
# --------------------------

weather_app = Flask("weather_service")

API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@weather_app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(WEATHER_URL, params=params)
    return jsonify(response.json())


# --------------------------
# Recommendation Service
# --------------------------

recommendation_app = Flask("recommendation_service")


@recommendation_app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    temp = data["main"]["temp"]
    condition = data["weather"][0]["main"].lower()

    result = []

    if "rain" in condition:
        result.append("Возьмите зонт")
    if temp < 5:
        result.append("Наденьте куртку")
    if temp > 25:
        result.append("Пейте больше воды")

    return jsonify({"recommendations": result})


# --------------------------
# History Service
# --------------------------

history_app = Flask("history_service")
DB = "history.db"


@history_app.route("/history", methods=["POST"])
def save_history():
    city = request.json.get("city")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history (city TEXT)")
    cur.execute("INSERT INTO history VALUES (?)", (city,))
    conn.commit()
    conn.close()
    return jsonify({"status": "saved"})


@history_app.route("/stats", methods=["GET"])
def stats():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT city, COUNT(*) FROM history GROUP BY city")
    data = cur.fetchall()
    conn.close()
    return jsonify(data)


# --------------------------
# Multiprocess Launcher
# --------------------------

def run_weather():
    weather_app.run(port=5000)


def run_recommendation():
    recommendation_app.run(port=5001)


def run_history():
    history_app.run(port=5002)


if __name__ == "__main__":
    Process(target=run_weather).start()
    Process(target=run_recommendation).start()
    Process(target=run_history).start()
