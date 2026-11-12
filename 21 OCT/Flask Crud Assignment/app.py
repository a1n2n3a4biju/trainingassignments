
from flask import Flask, request, jsonify

app = Flask(__name__)

students = [
    {
        "id": 1,
        "name": "Rhea Kapoor",
        "course": "Python",
        "score": 82
    },
    {
        "id": 2,
        "name": "Zain Malik",
        "course": "SQL",
        "score": 76
    },
    {
        "id": 3,
        "name": "Devika Rao",
        "course": "Cloud",
        "score": 91
    }
]


# 1. GET all students
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students), 200


# 2. GET student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    for student in students:
        if student.get("id") == student_id:
            return jsonify(student), 200

    return jsonify({"message": "Student not found"}), 404


# 3. POST - Add a new student
@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    required_fields = ["id", "name", "course", "score"]

    if not all(field in data for field in required_fields):
        return jsonify({"message": "All fields are required"}), 400

    if any(student.get("id") == data["id"] for student in students):
        return jsonify({"message": "Student ID already exists"}), 409

    students.append(data)

    return jsonify({"message": "Student added successfully"}), 201


# 4. PUT - Update an existing student
@app.route("/students/<int:student_id>", methods=["PUT"])
def put_student(student_id):
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    for student in students:
        if student.get("id") == student_id:
            student["name"] = data.get("name", student["name"])
            student["course"] = data.get("course", student["course"])
            student["score"] = data.get("score", student["score"])

            return jsonify({
                "message": "Student updated successfully",
                "student": student
            }), 200

    return jsonify({"message": "Student not found"}), 404


# 5. DELETE - Delete a student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    for student in students:
        if student.get("id") == student_id:
            students.remove(student)

            return jsonify({
                "message": "Student removed successfully"
            }), 200

    return jsonify({"message": "Student not found"}), 404


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
