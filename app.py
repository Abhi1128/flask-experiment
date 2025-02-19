from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Load words from JSON file (Limit to 5 words for testing)
with open("words.json", "r", encoding="utf-8") as file:
    words_data = json.load(file)
    words = words_data["words"]

@app.route("/", methods=["GET", "POST"])
def enter_name():
    if request.method == "POST":
        session["subject_name"] = request.form["name"]  # Store name in session
        return redirect(url_for("experiment"))  # Redirect to experiment

    return render_template("name.html")  # Show name input page

@app.route("/experiment")
def experiment():
    if "subject_name" not in session:
        return redirect(url_for("enter_name"))  # If no name, go back to name page

    return render_template("index.html", words=words)

@app.route("/submit", methods=["POST"])
def submit():
    if "subject_name" not in session:
        return jsonify({"error": "No subject name provided!"}), 400

    data = request.json  # Get JSON data from frontend
    df = pd.DataFrame(data)

    # Get subject name and create a filename
    subject_name = session["subject_name"].replace(" ", "_")  # Replace spaces with underscores
    filename = f"{subject_name}.csv"

    # Save data with proper encoding
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    return jsonify({"message": f"Data saved successfully as {filename}"})

if __name__ == "__main__":
    app.run(debug=True)
