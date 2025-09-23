from flask import Flask, render_template, jsonify, request, session, Response
from dbmgr import quickOpen, quickClose, dbstartup, populateDB, unpopulateDB

app = Flask(__name__)
app.secret_key = "DBMSGP"

@app.route("/")
def index():
    return render_template("index.html")

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

@app.route("/get/students", methods=["GET"])
def getstudents():
    cursor, conn = quickOpen()
    cursor.execute("SELECT * FROM STUDENTS")
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/students", methods=["POST"]) 
def addstudent():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO STUDENTS (name, email, enrollmentyear)
            VALUES (?, ?, ?)
        """, (
            data["name"],
            data["email"],
            int(data["enrollmentyear"])
        ))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/students/<int:id>", methods=["PUT"])
def modifystudent(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE STUDENTS
            SET name = ?, email = ?, enrollmentyear = ?
            WHERE studentid = ?
        """, (
            data["name"],
            data["email"],
            int(data["enrollmentyear"]),
            id
        ))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/students/<int:id>", methods=["DELETE"])
def deletestudent(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM STUDENTS WHERE studentid = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/get/departments", methods=["GET"])
def getdepartments():
    cursor, conn = quickOpen()
    cursor.execute("SELECT * FROM DEPARTMENTS")
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/departments", methods=["POST"])
def adddepartment():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO DEPARTMENTS (name, code)
            VALUES (?, ?)
        """, (data["name"], data["code"]))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/departments/<int:id>", methods=["PUT"])
def modifydepartment(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE DEPARTMENTS SET name = ?, code = ? WHERE departmentid = ?
        """, (data["name"], data["code"], id))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/departments/<int:id>", methods=["DELETE"])
def deletedepartment(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM DEPARTMENTS WHERE departmentid = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/get/professors", methods=["GET"])
def getprofessors():
    cursor, conn = quickOpen()
    cursor.execute("""
        SELECT PROFESSORS.professorid, PROFESSORS.name, PROFESSORS.email, PROFESSORS.departmentid, DEPARTMENTS.name AS departmentname
        FROM PROFESSORS
        LEFT JOIN DEPARTMENTS ON PROFESSORS.departmentid = DEPARTMENTS.departmentid
    """)
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/professors", methods=["POST"])
def addprofessor():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO PROFESSORS (name, email, departmentid)
            VALUES (?, ?, ?)
        """, (data["name"], data["email"], int(data["departmentid"])))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/professors/<int:id>", methods=["PUT"])
def modifyprofessor(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE PROFESSORS SET name = ?, email = ?, departmentid = ?
            WHERE professorid = ?
        """, (data["name"], data["email"], int(data["departmentid"]), id))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/professors/<int:id>", methods=["DELETE"])
def deleteprofessor(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM PROFESSORS WHERE professorid = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/get/courses", methods=["GET"])
def getcourses():
    cursor, conn = quickOpen()
    cursor.execute("""
        SELECT COURSES.courseid, COURSES.name, COURSES.code, COURSES.credits, COURSES.description, COURSES.departmentid, DEPARTMENTS.name AS departmentname
        FROM COURSES
        LEFT JOIN DEPARTMENTS ON COURSES.departmentid = DEPARTMENTS.departmentid
    """)
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/courses", methods=["POST"])
def addcourse():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO COURSES (name, code, credits, description, departmentid)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["name"], data["code"], int(data["credits"]),
            data["description"], int(data["departmentid"])
        ))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/courses/<int:id>", methods=["PUT"])
def modifycourse(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE COURSES SET name = ?, code = ?, credits = ?, description = ?, departmentid = ?
            WHERE courseid = ?
        """, (
            data["name"], data["code"], int(data["credits"]),
            data["description"], int(data["departmentid"]), id
        ))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/courses/<int:id>", methods=["DELETE"])
def deletecourse(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM COURSES WHERE courseid = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/get/sections", methods=["GET"])
def getsections():
    cursor, conn = quickOpen()
    cursor.execute("""
        SELECT SECTIONS.courseid, COURSES.name AS coursename, SECTIONS.sectionid, SECTIONS.professorid, PROFESSORS.name AS professorname, SECTIONS.schedule
        FROM SECTIONS
        LEFT JOIN PROFESSORS ON SECTIONS.professorid = PROFESSORS.professorid
        LEFT JOIN COURSES ON SECTIONS.courseid = COURSES.courseid
    """)
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/sections", methods=["POST"])
def addsection():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO SECTIONS (courseid, sectionid, professorid, schedule)
            VALUES (?, ?, ?, ?)
        """, (
            int(data["courseid"]), int(data["sectionid"]),
            int(data["professorid"]), data["schedule"]
        ))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/sections/<int:courseid>/<int:sectionid>", methods=["PUT"])
def modifysection(courseid, sectionid):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE SECTIONS
            SET professorid = ?, schedule = ?
            WHERE courseid = ? AND sectionid = ?
        """, (
            int(data["professorid"]), data["schedule"],
            courseid, sectionid
        ))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except Exception:
        quickClose(cursor, conn)
        return "Failed", 400


@app.route("/api/sections/<int:courseid>/<int:sectionid>", methods=["DELETE"])
def deletesection(courseid, sectionid):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM SECTIONS WHERE courseid = ? AND sectionid = ?", (
            courseid, sectionid
        ))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/get/enrollments", methods=["GET"])
def getenrollments():
    cursor, conn = quickOpen()
    cursor.execute("""
        SELECT 
            ENROLLMENTS.enrollmentid, 
            ENROLLMENTS.studentid, 
            STUDENTS.name AS studentname,
            ENROLLMENTS.courseid, 
            COURSES.name AS coursename,
            ENROLLMENTS.sectionid, 
            ENROLLMENTS.grade
        FROM ENROLLMENTS
        LEFT JOIN STUDENTS ON ENROLLMENTS.studentid = STUDENTS.studentid
        LEFT JOIN COURSES ON ENROLLMENTS.courseid = COURSES.courseid
    """)
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/enrollments", methods=["POST"])
def addenrollment():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO ENROLLMENTS (studentid, courseid, sectionid, grade)
            VALUES (?, ?, ?, ?)
        """, (
            int(data["studentid"]), int(data["courseid"]),
            int(data["sectionid"]), data["grade"]
        ))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/enrollments/<int:id>", methods=["PUT"])
def modifyenrollment(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE ENROLLMENTS
            SET studentid = ?, courseid = ?, sectionid = ?, grade = ?
            WHERE enrollmentid = ?
        """, (
            int(data["studentid"]), int(data["courseid"]),
            int(data["sectionid"]), data["grade"], id
        ))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except:
        quickClose(cursor, conn)
        return "Failed", 400

@app.route("/api/enrollments/<int:id>", methods=["DELETE"])
def deleteenrollment(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM ENROLLMENTS WHERE enrollmentid = ?", (id,))
        conn.commit()
        quickClose(cursor, conn)
        return "Complete", 200
    except:
        quickClose(cursor, conn)
        return "Failed", 400

cursor, conn = quickOpen()
try:
    dbstartup()
    conn.commit()
except:
    print("Issue with making Schema")
    conn.rollback()
finally:
    quickClose(cursor, conn)

unpopulateDB()
populateDB()

app.run(host='0.0.0.0', port=3000, debug=True)