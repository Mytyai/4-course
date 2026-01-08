from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "history.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            city TEXT
        )
    """)
    conn.commit()
    conn.close()


@app.route("/history", methods=["POST"])
def save_history():
    city = request.json.get("city")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO history (city) VALUES (?)", (city,))
    conn.commit()
    conn.close()
    return jsonify({"status": "saved"})


@app.route("/stats", methods=["GET"])
def stats():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT city, COUNT(*) as count
        FROM history
        GROUP BY city
        ORDER BY count DESC
    """)
    rows = c.fetchall()
    conn.close()

    return jsonify(rows)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5002)
