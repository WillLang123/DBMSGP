import sqlite3

def quickOpen():
    connection = sqlite3.connect("DBMSGP.db")
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    return cursor, connection

def quickClose(cursor, connection):
    cursor.close()
    connection.close()

def dbstartup():
    cursor, conn = quickOpen()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DEPARTMENTS (
        departmentid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        code TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PROFESSORS (
        professorid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        departmentid INTEGER,
        FOREIGN KEY (departmentid) REFERENCES DEPARTMENTS(departmentid) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS STUDENTS (
        studentid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        enrollmentyear INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS COURSES (
        courseid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        code TEXT NOT NULL UNIQUE,
        credits INTEGER NOT NULL,
        description TEXT,
        departmentid INTEGER,
        FOREIGN KEY (departmentid) REFERENCES DEPARTMENTS(departmentid) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sections (
        courseid INTEGER NOT NULL,
        sectionid INTEGER NOT NULL,
        professorid INTEGER NOT NULL,
        schedule TEXT,
        PRIMARY KEY (courseid, sectionid),
        FOREIGN KEY (professorid) REFERENCES PROFESSORS(professorid) ON DELETE CASCADE,
        FOREIGN KEY (courseid) REFERENCES COURSES(courseid) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ENROLLMENTS (
        enrollmentid INTEGER PRIMARY KEY,
        studentid INTEGER NOT NULL,
        courseid INTEGER NOT NULL,
        sectionid INTEGER NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY (studentid) REFERENCES STUDENTS(studentid) ON DELETE CASCADE,
        FOREIGN KEY (courseid, sectionid) REFERENCES SECTIONS(courseid, sectionid) ON DELETE CASCADE
    );
    """)

    conn.commit()
    quickClose(cursor, conn)
    print("Schema created.")

def unpopulateDB():
    cursor, conn = quickOpen()
    cursor.execute("DELETE FROM ENROLLMENTS")
    cursor.execute("DELETE FROM SECTIONS")
    cursor.execute("DELETE FROM STUDENTS")
    cursor.execute("DELETE FROM PROFESSORS")
    cursor.execute("DELETE FROM COURSES")
    cursor.execute("DELETE FROM DEPARTMENTS")
    conn.commit()
    quickClose(cursor, conn)
    print("DB cleaned.")

def populateDB():
    cursor, conn = quickOpen()

    for i in range(1, 11):
        name = f"Test{i}"
        email = f"test{i}@lamar.edu"
        code = f"COSC{i}"
        credits = i
        schedule = f"Mon {i}:00AM"
        enrollmentyear = 2000 + i
        grade = "A"

        cursor.execute("""
            INSERT INTO DEPARTMENTS (departmentid, name, code)
            VALUES (?, ?, ?)
        """, (i, name, code))

        cursor.execute("""
            INSERT INTO PROFESSORS (professorid, name, email, departmentid)
            VALUES (?, ?, ?, ?)
        """, (i, name, email, i))

        cursor.execute("""
            INSERT INTO STUDENTS (studentid, name, email, enrollmentyear)
            VALUES (?, ?, ?, ?)
        """, (i, name, email, enrollmentyear))

        cursor.execute("""
            INSERT INTO COURSES (courseid, name, code, credits, description, departmentid)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (i, name, code, credits, f"Description for {name}", i))

        cursor.execute("""
            INSERT INTO SECTIONS (courseid, sectionid, professorid, schedule)
            VALUES (?, ?, ?, ?)
        """, (i, i, i, schedule))

        cursor.execute("""
            INSERT INTO ENROLLMENTS (enrollmentid, studentid, courseid, sectionid, grade)
            VALUES (?, ?, ?, ?, ?)
        """, (i, i, i, i, grade))

    conn.commit()
    quickClose(cursor, conn)
    print("DB populated.")
