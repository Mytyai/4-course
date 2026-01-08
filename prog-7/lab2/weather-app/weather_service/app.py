from flask import Flask, request, jsonify
import requests
from multiprocessing import Process, Queue
import os

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY")
URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city, queue):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(URL, params=params)
    queue.put(response.json())


@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    queue = Queue()
    process = Process(target=fetch_weather, args=(city, queue))
    process.start()
    process.join()

    weather_data = queue.get()

    return jsonify(weather_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
