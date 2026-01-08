from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    weather = data["weather"][0]["main"].lower()
    temp = data["main"]["temp"]

    recommendations = []

    if "rain" in weather:
        recommendations.append("Возьмите зонт")
    if temp < 5:
        recommendations.append("Оденьтесь теплее")
    if temp > 25:
        recommendations.append("Пейте больше воды")

    return jsonify({
        "recommendations": recommendations
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
