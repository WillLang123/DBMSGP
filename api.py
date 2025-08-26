from flask import Flask, render_template, jsonify, request, session, Response
from dbmgr import quickOpen, quickClose

app = Flask(__name__)
app.secret_key = "DBMSGP"

#renders index page
@app.route('/')
def index():
    return render_template('index.html')

cursor, conn = quickOpen()
try:
    #Create tables here
    conn.commit()
    print("Databases created")
except Exception as e:
    print("Issue with making database")
    conn.rollback()
finally:
    quickClose(cursor,conn)
    #hosts website to port 3000 to show website
app.run(host='0.0.0.0', port=3000, debug=True)