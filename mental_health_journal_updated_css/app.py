from flask import Flask, render_template, request
from textblob import TextBlob
import json
import datetime

app = Flask(__name__)

def analyze_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        entry = request.form["entry"]
        mood = analyze_mood(entry)
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Save entry to JSON
        with open("entries.json", "r+") as f:
            data = json.load(f)
            data.append({"date": date, "entry": entry, "mood": mood})
            f.seek(0)
            json.dump(data, f, indent=4)

        return render_template("result.html", mood=mood, entry=entry)
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    with open("entries.json") as f:
        data = json.load(f)
    return render_template("dashboard.html", entries=data)

if __name__ == "__main__":
    app.run(debug=True)
