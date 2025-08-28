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
        enrolldate DATE NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY (studentid) REFERENCES Students(id),
        FOREIGN KEY (courseid) REFERENCES Courses(id)
    );
    """)

    conn.commit()
    quickClose(cursor, conn)

    print(f"Database made")

def populateDB():
    cursor, conn = quickOpen()

    quickClose(cursor, conn)