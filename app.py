from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

FILE = "reviews.json"

# create file if not exists
if not os.path.exists(FILE):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/addReview", methods=["POST"])
def add_review():
    data = request.get_json()

    # add timestamp
    data["time"] = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    with open(FILE, "r", encoding="utf-8") as f:
        reviews = json.load(f)

    # latest on top
    reviews.insert(0, data)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

    return jsonify({"message": "Review added"})

@app.route("/getReviews", methods=["GET"])
def get_reviews():
    with open(FILE, "r", encoding="utf-8") as f:
        reviews = json.load(f)

    return jsonify(reviews)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)