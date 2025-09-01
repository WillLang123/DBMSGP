from flask import Flask, render_template, jsonify, request, session, Response
from dbmgr import quickOpen, quickClose, dbstartup, populateDB, unpopulateDB

#TODOS: make frontend nices, banner, student remove query, move some js functions with html file, prevent major/subject/teacher delete if used 
# select for all forms, id to text translate/grab, streamline, make modular.

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

#Sends list of tuples to frontend
@app.route("/get/students",methods=["GET"])
def getstudents():
    cursor, conn = quickOpen()
    cursor.execute("SELECT * from Students")
    data = cursor.fetchall()
    quickClose(cursor, conn)
    return jsonify(data)

@app.route("/api/students",methods=["POST"]) 
def addstudent():
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            INSERT INTO Students (fname, lname, email, majorid, enrollyear)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["fname"],
            data["lname"],
            data["email"],
            int(data["majorid"]),
            int(data["enrollyear"])
        ))

        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 201

    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/students/<int:id>",methods=["PUT"])
def modifystudent(id):
    cursor, conn = quickOpen()
    data = request.get_json()
    try:
        cursor.execute("""
            UPDATE Students
            SET fname = ?, lname = ?, email = ?, majorid = ?, enrollyear = ?
            WHERE id = ?
        """, (
            data["fname"],
            data["lname"],
            data["email"],
            int(data["majorid"]),
            int(data["enrollyear"]),
            id
        ))

        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400

@app.route("/api/students/<int:id>",methods=["DELETE"])
def deletestudent(id):
    cursor, conn = quickOpen()
    try:
        cursor.execute("DELETE FROM Students WHERE id = ?", (id,))
        #TODO remove all student enrollments
        conn.commit()
        quickClose(cursor, conn)
        return jsonify({"status": "deleted"}), 200
        
    except Exception as e:
        quickClose(cursor, conn)
        return jsonify({"error": str(e)}), 400


# FOR ANY API CALL
# dataFromAPI = request.get_json()
# name = dataFromAPI.get('name')
# cursor, conn = quickCursor()
# cursor.execute();
# result = cursor.fetchone()
# cursor.commit();
# curso.rollback();
# output = jsonify({"words": "Blah blag"})
# return output #so API knows what happened with transaction

# Use this for Major delete/ subject delete:
#cursor.execute("SELECT COUNT(*) FROM Students WHERE majorid = ?", (id))
#        count = cursor.fetchone()[0]
#        if count > 0:
#            quickClose(cursor, conn)
#            return jsonify({"error": str(e)}), 400
#        else:
#            cursor.execute("DELETE FROM Students WHERE id = ?", (id))
#            conn.commit()
#            quickClose(cursor, conn)
#            return jsonify({"status": "deleted"}), 200

cursor, conn = quickOpen()
try:
    dbstartup()
    conn.commit()
except Exception as e:
    print("Issue with making Schema")
    conn.rollback()
finally:
    quickClose(cursor,conn)

unpopulateDB()
populateDB()

app.run(host='0.0.0.0', port=3000, debug=True)
#hosts website to port 3000 to show website