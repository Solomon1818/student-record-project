import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

CORS(app)

client = MongoClient(os.environ.get("MONGO_URI"))

db = client["StudentDb"]
students = db["StudentDetails"]

@app.route('/')
def home():
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/search")
def search_student():
    query = request.args.get("q")

    if not query:
        return jsonify({"error": "No search value provided"})

    student = students.find_one(
        {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"rollno": {"$regex": query, "$options": "i"}}
            ]
        },
        {"_id": 0}
    )

    if student:
        return jsonify(student)

    return jsonify({"error": "Student not found"})

@app.route("/marks")
def get_marks():
    rollno = request.args.get("rollno")
    sem = request.args.get("sem")

    if not rollno or not sem:
        return jsonify({"error": "Missing roll number or semester"})

    student = students.find_one(
        {"rollno": {"$regex": f"^{rollno}$", "$options": "i"}},
        {"_id": 0, "semesters": 1}
    )

    if not student:
        return jsonify({"error": "Student not found"})

    semesters = student.get("semesters", {})
    sem_key = f"sem{sem}"

    if sem_key not in semesters:
        return jsonify({"error": "Semester data not available"})

    return jsonify(semesters[sem_key])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))