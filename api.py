from flask import Flask, render_template, jsonify, request, session, Response
from dbmgr import quickOpen, quickClose, dbstartup, populateDB, unpopulateDB

#TODOS: streamline, fix cascase delete

app = Flask(__name__)
app.secret_key = "DBMSGP"

#renders index page
@app.route("/")
def index():
    return render_template("index.html")

#renders student page
@app.route("/students")
def students():
    return render_template("students.html")

@app.route("/professors")
def professors():
    return render_template("professors.html")

@app.route("/departments")
def departments():
    return render_template("departments.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/sections")
def sections():
    return render_template("sections.html")

@app.route("/enrollments")
def enrollments():
    return render_template("enrollments.html")

#Sends list of tuples to frontend
@app.route("/get/students", methods=["GET"])
def getstudents():
    cursor, conn = quickOpen()
    cursor.execute("SELECT * FROM Students")
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

#adds student from api json
@app.route("/api/students", methods=["POST"]) 
def addstudent():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO Students (name, email, enrollmentyear)
            VALUES (?, ?, ?)
        """, (
            data["name"],
            data["email"],
            int(data["enrollmentyear"])
        ))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 201

    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

#updates student entry based on restful url /id and json
@app.route("/api/students/<int:id>", methods=["PUT"])
def modifystudent(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE Students
            SET name = ?, email = ?, enrollmentyear = ?
            WHERE id = ?
        """, (
            data["name"],
            data["email"],
            int(data["enrollmentyear"]),
            id
        ))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

#deletes students and enrollments with student based off /id and json
@app.route("/api/students/<int:id>", methods=["DELETE"])
def deletestudent(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM Students WHERE id = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

#Department Methods

@app.route("/get/departments", methods=["GET"])
def getdepartments():
    cursor, conn = quickOpen()
    cursor.execute("SELECT * FROM Departments")
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/departments", methods=["POST"])
def adddepartment():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO Departments (name, code)
            VALUES (?, ?)
        """, (data["name"], data["code"]))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/departments/<int:id>", methods=["PUT"])
def modifydepartment(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE Departments SET name = ?, code = ? WHERE id = ?
        """, (data["name"], data["code"], id))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/departments/<int:id>", methods=["DELETE"])
def deletedepartment(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM Departments WHERE id = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

#Professor Methods

@app.route("/get/professors", methods=["GET"])
def getprofessors():
    cursor, conn = quickOpen()
    cursor.execute("SELECT Professors.id, Professors.name, Professors.email, Departments.name AS departmentname FROM Professors LEFT JOIN Departments ON Professors.departmentid = Departments.id")
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/professors", methods=["POST"])
def addprofessor():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO Professors (name, email, departmentid)
            VALUES (?, ?, ?)
        """, (data["name"], data["email"], int(data["departmentid"])))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/professors/<int:id>", methods=["PUT"])
def modifyprofessor(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE Professors SET name = ?, email = ?, departmentid = ?
            WHERE id = ?
        """, (data["name"], data["email"], int(data["departmentid"]), id))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/professors/<int:id>", methods=["DELETE"])
def deleteprofessor(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM Professors WHERE id = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

#Course functions

@app.route("/get/courses", methods=["GET"])
def getcourses():
    cursor, conn = quickOpen()
    cursor.execute("SELECT Courses.id, Courses.name, Courses.code, Courses.credits, Courses.description, Departments.name AS departmentname FROM Courses LEFT JOIN Departments ON Courses.departmentid = Departments.id")
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/courses", methods=["POST"])
def addcourse():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO Courses (name, code, credits, description, departmentid)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["name"], data["code"], int(data["credits"]),
            data["description"], int(data["departmentid"])
        ))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/courses/<int:id>", methods=["PUT"])
def modifycourse(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE Courses SET name = ?, code = ?, credits = ?, description = ?, departmentid = ?
            WHERE id = ?
        """, (
            data["name"], data["code"], int(data["credits"]),
            data["description"], int(data["departmentid"]), id
        ))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/courses/<int:id>", methods=["DELETE"])
def deletecourse(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM Courses WHERE id = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

#Section methods

@app.route("/get/sections", methods=["GET"])
def getsections():
    cursor, conn = quickOpen()
    cursor.execute("SELECT Sections.id, Professors.name AS professorname, Courses.name AS coursename, Sections.schedule FROM Sections LEFT JOIN Professors ON Sections.professorid = Professors.id LEFT JOIN Courses ON Sections.courseid = Courses.id")
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/sections", methods=["POST"])
def addsection():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO Sections (professorid, courseid, schedule)
            VALUES (?, ?, ?)
        """, (
            int(data["professorid"]), int(data["courseid"]), data["schedule"]
        ))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/sections/<int:id>", methods=["PUT"])
def modifysection(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE Sections
            SET professorid = ?, courseid = ?, schedule = ?
            WHERE id = ?
        """, (
            int(data["professorid"]), int(data["courseid"]),
            data["schedule"], id
        ))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/sections/<int:id>", methods=["DELETE"])
def deletesection(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM Sections WHERE id = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

#Enrollment functions

@app.route("/get/enrollments", methods=["GET"])
def getenrollments():
    cursor, conn = quickOpen()
    cursor.execute("SELECT Enrollments.id, Students.name AS studentname, Enrollments.sectionid, Enrollments.grade FROM Enrollments LEFT JOIN Students ON Enrollments.studentid = Students.id")
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/enrollments", methods=["POST"])
def addenrollment():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO Enrollments (studentid, sectionid, grade)
            VALUES (?, ?, ?)
        """, (
            int(data["studentid"]), int(data["sectionid"]),
            data["grade"]
        ))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/enrollments/<int:id>", methods=["PUT"])
def modifyenrollment(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE Enrollments
            SET studentid = ?, sectionid = ?, grade = ?
            WHERE id = ?
        """, (
            int(data["studentid"]), int(data["sectionid"]),
            data["grade"], id
        ))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/enrollments/<int:id>", methods=["DELETE"])
def deleteenrollment(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM Enrollments WHERE id = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

#initial db setup
cursor, conn = quickOpen()
try:
    dbstartup()
    conn.commit()
except Exception as e:
    print("Issue with making Schema")
    conn.rollback()
finally:
    quickClose(cursor, conn)

unpopulateDB()
populateDB()

#hosts website to port 3000 to show website
app.run(host='0.0.0.0', port=3000, debug=True)
