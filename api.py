from flask import Flask, render_template, jsonify, request, session, Response
from dbmgr import quickOpen, quickClose, dbstartup, populateDB, unpopulateDB

app = Flask(__name__)
app.secret_key = "DBMSGP"

#renders index page
@app.route('/')
def index():
    return render_template('index.html')
#renders student page
@app.route('/students')
def students():
    return render_template('students.html')

# @app.route("/chatroom/<int:chatroomID>/send", methods=["POST"])
# def handleSendMessage(chatroomID):

# @app.route("/chatroom/<int:chatroomID>/stream")
# def streamMessages(chatroomID):

# @app.route("/createChatroom", methods=["POST"])
# def handleCreateChatroom():

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

cursor, conn = quickOpen()
try:
    #Create tables here
    conn.commit()
    print("Schema made")
except Exception as e:
    print("Issue with making Schema")
    conn.rollback()
finally:
    quickClose(cursor,conn)
    #hosts website to port 3000 to show website

unpopulateDB()
populateDB()
dbstartup()
app.run(host='0.0.0.0', port=3000, debug=True)