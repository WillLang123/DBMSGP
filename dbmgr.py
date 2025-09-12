import sqlite3

def quickOpen():
    connection = sqlite3.connect("DBMSGP.db")
    cursor = connection.cursor()
    return cursor, connection

def quickClose(cursor, connection):
    cursor.close()
    connection.close()

def dbstartup():
    cursor, conn = quickOpen()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Departments (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        code TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Professors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        departmentid INTEGER,
        FOREIGN KEY (departmentid) REFERENCES Departments(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        enrollmentyear INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Courses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        code TEXT NOT NULL UNIQUE,
        credits INTEGER NOT NULL,
        description TEXT,
        departmentid INTEGER,
        FOREIGN KEY (departmentid) REFERENCES Departments(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sections (
        id INTEGER PRIMARY KEY,
        professorid INTEGER NOT NULL,
        courseid INTEGER NOT NULL,
        schedule TEXT,
        FOREIGN KEY (professorid) REFERENCES Professors(id) ON DELETE CASCADE,
        FOREIGN KEY (courseid) REFERENCES Courses(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Enrollments (
        id INTEGER PRIMARY KEY,
        studentid INTEGER NOT NULL,
        sectionid INTEGER NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY (studentid) REFERENCES Students(id) ON DELETE CASCADE,
        FOREIGN KEY (sectionid) REFERENCES Sections(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    quickClose(cursor, conn)
    print("Schema created.")

def unpopulateDB():
    cursor, conn = quickOpen()
    cursor.execute("DELETE FROM Enrollments")
    cursor.execute("DELETE FROM Sections")
    cursor.execute("DELETE FROM Students")
    cursor.execute("DELETE FROM Professors")
    cursor.execute("DELETE FROM Courses")
    cursor.execute("DELETE FROM Departments")
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
        schedule = f"Mon/Wed {i}:00AM - {i}:15AM"
        enrollmentyear = 2000 + i
        grade = "A"

        cursor.execute("""
            INSERT INTO Departments (id, name, code)
            VALUES (?, ?, ?)
        """, (i, name, code))

        cursor.execute("""
            INSERT INTO Professors (id, name, email, departmentid)
            VALUES (?, ?, ?, ?)
        """, (i, name, email, i))

        cursor.execute("""
            INSERT INTO Students (id, email, name, enrollmentyear)
            VALUES (?, ?, ?, ?)
        """, (i, email, name, enrollmentyear))

        cursor.execute("""
            INSERT INTO Courses (id, name, code, credits, description, departmentid)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (i, name, code, credits, f"Description for {name}", i))

        cursor.execute("""
            INSERT INTO Sections (id, professorid, courseid, schedule)
            VALUES (?, ?, ?, ?)
        """, (i, i, i, schedule))

        cursor.execute("""
            INSERT INTO Enrollments (id, studentid, sectionid, grade)
            VALUES (?, ?, ?, ?)
        """, (i, i, i, grade))

    conn.commit()
    quickClose(cursor, conn)
    print("DB populated.")