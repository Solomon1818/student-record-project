import os
from flask import Flask, request, jsonify,  render_template
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False
CORS(app)

#MongoDB connection (client)
client = MongoClient("mongodb+srv://solomonking:Solomon%4018@cluster0.kxn98mx.mongodb.net/?appName=Cluster0")

#Database name (from Compass)
db = client["StudentDb"]

#Collection name (from Compass)
students = db["StudentDetails"]

@app.route('/')
def home():
    return render_template('login.html')



@app.route("/search", methods=["GET"])
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
    else:
        return jsonify({"error": "Student not found"})

@app.route("/marks", methods=["GET"])
def get_marks():
    rollno = request.args.get("rollno")
    sem = request.args.get("sem")

    print("DEBUG rollno:", rollno)
    print("DEBUG sem:", sem)

    student = students.find_one({
        "rollno": {"$regex": f"^{rollno}$", "$options": "i"}
    })

    if not student:
        return jsonify({"error": "Student not found"})

    semesters = student.get("semesters", {})
    sem_key = f"sem{sem}"

    if sem_key not in semesters:
        return jsonify({"error": "Semester data not available"})

    return jsonify(semesters[sem_key])

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))



