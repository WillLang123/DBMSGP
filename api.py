from flask import Flask, render_template, jsonify, request, session, Response
import dbmgr

app = Flask(__name__)
app.secret_key = "DBMSGP"

#renders index page
@app.route('/')
def index():
    return render_template('index.html')

app.run(host='0.0.0.0', port=3000, debug=True)