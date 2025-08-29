import sqlite3

def quickOpen():
    connection = sqlite3.connect("DBMSGP.db")
    cursor = connection.cursor()
    return cursor, connection

def quickClose(cursor, connection):
    cursor.close()
    connection.close()
#quickly opens and closes sqlite3 cursors

def dbstartup():
    cursor, conn = quickOpen()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Majors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subjects (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teachers (
        id INTEGER PRIMARY KEY,
        fname TEXT NOT NULL,
        lname TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY,
        fname TEXT NOT NULL,
        lname TEXT NOT NULL,
        email TEXT NOT NULL,
        majorid INTEGER,
        enrollyear INTEGER NOT NULL,
        FOREIGN KEY (majorid) REFERENCES Majors(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        code TEXT NOT NULL,
        teacherid INTEGER,
        subjectid INTEGER,
        credits INTEGER NOT NULL,
        FOREIGN KEY (teacherid) REFERENCES Teachers(id),
        FOREIGN KEY (subjectid) REFERENCES Subjects(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Enrollments (
        id INTEGER PRIMARY KEY,
        studentid INTEGER NOT NULL,
        courseid INTEGER NOT NULL,
        enrollyear INTERGER NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY (studentid) REFERENCES Students(id),
        FOREIGN KEY (courseid) REFERENCES Courses(id)
    );
    """)

    conn.commit()
    quickClose(cursor, conn)

    print(f"Database made")

def unpopulateDB():
    cursor, conn = quickOpen()
    cursor.execute("""DELETE from Students""")
    cursor.execute("""DELETE from Teachers""")
    cursor.execute("""DELETE from Courses""")
    cursor.execute("""DELETE from Enrollments""")
    cursor.execute("""DELETE from Majors""")
    cursor.execute("""DELETE from Subjects""")
    conn.commit()
    quickClose(cursor, conn)

def populateDB():
    cursor, conn = quickOpen()
    for i in range(1, 10):
        fname = f"Test{i}"
        lname = f"Test{i}"
        email = f"Test{i}@lamar.edu"
        name = f"Test{i}"
        password = f"Test{i}"
        enrollyear = 2000+i
        code = f"Test{i}"
        #enrolldate = None
        grade = f"A"
        cursor.execute("""
            INSERT INTO Majors (id, name)
            VALUES (?, ?)
        """, (i, name))
        cursor.execute("""
            INSERT INTO Subjects (id, name)
            VALUES (?, ?)
        """, (i, name))
        cursor.execute("""
            INSERT INTO Teachers (id, fname, lname, email, password)
            VALUES (?, ?, ?, ?, ?)
        """, (i, fname, lname, email, password))
        cursor.execute("""
            INSERT INTO Students (id, fname, lname, email, majorid, enrollyear)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (i, fname, lname, email, i, enrollyear))
        cursor.execute("""
            INSERT INTO Courses (id, name, code, teacherid, subjectid, credits)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (i, name, code, i, i, i))
        cursor.execute("""
            INSERT INTO Enrollments (id, studentid, courseid, enrolldate, grade)
            VALUES (?, ?, ?, ?, ?)
        """, (i, i, i, enrollyear ,grade))
    quickClose(cursor, conn)