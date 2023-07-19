import threading

from flask import Flask, render_template, Response, request,make_response, send_from_directory
# forda register, notif and chatbox
import sqlite3
from pywebpush import webpush, WebPushException
from flask_socketio import SocketIO, send
import json
import itertools
import datetime

import entraceCreator
from lotAvailability import parking_availability
import entraceCreator as entrance
#import lotCreator
import cv2
import viewParking_ForTest3 as view
import adminParking as admin
import dotenv
import time
# okay ito ang maload ang  env file
from dotenv import load_dotenv
from os import environ
import os

import string
import random

#print(os.getenv('FUNCTION_SWITCH'))
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

app=Flask(__name__)


camIndex = int(os.environ["CAMERA"])
camera = cv2.VideoCapture(camIndex)

# forda register, notif
app.secret_key="__privatekey__"
VAPID_SUBJECT = "mailto:dipisoteta@gmail.com"
VAPID_PRIVATE = "3qnVrbOmGqIFvWZzYPYzP4B-MGamQMVhlcKCxg1Mng8"

# chatbox
app.config['SECRET'] ="secret!123"
socketio = SocketIO(app, cors_allowed_origins="*")



parking_lot_coords = view.importCarParkCoords()
parking_lot_startLoc = view.importCarParkCoordsLoc()

# global variables for envs

global userView, adminView, adminEntranceCreate, adminLabelLots, adminLotCreator, adminAssignLot, adminCapture
userView = False
adminView = False
adminEntranceCreate = False
adminLabelLots = False
adminLotCreator = False
adminAssignLot = False
adminCapture = False
switch = 1
capture = 0
def gen_frames():
    global capture
    while True:
        success, frame = camera.read()
        if success:
            if (userView):
                view.mainCamera(parking_lot_coords, parking_lot_startLoc, frame, 1)
            if (adminView):
                view.mainCamera(parking_lot_coords, parking_lot_startLoc, frame, 2)
            if (adminEntranceCreate):
                print("admin entrance create")
            if (adminLabelLots):
                print("admin label lots")
            if (adminLotCreator):
                print("admin create lots")
            if (adminAssignLot):
                print("admin assign lots")
            if (adminEntranceCreate):
                print("admin capture parking lot")
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print(e)
                pass
        else:
            pass

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



@socketio.on('message')
def handle_message(message):
    print("Received message: " + message)
    if message != "User conected!":
        send(message, broadcast=True)

@app.route('/')
def index():
    return render_template('UserLogin.html')

@app.route('/home')
def home():
    global userView, adminView
    userView = True
    adminView = False
    return render_template('Home.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/adminLogin')
def adminLogin():
    return render_template('AdminLogin.html')

@app.route('/userLogin',methods=['GET','POST'])
def userLogin():
    if request.method == 'POST':

        connection = sqlite3.connect('parkSupp_DATABASE.db')
        cursor = connection.cursor()

        username = request.form['username']
        password = request.form['password']

        print(username, password)

        query = "SELECT user_userName,user_password FROM user_Table WHERE user_userName ='" + username + "' and user_password='" + password +"'"

        cursor.execute(query)

        results = cursor.fetchall()

        # bale ang ano dito, kapag walang nabalik na name from the database sa paglogin, ibig sabihin di yun nakaregister
        if len(results) == 0:
            print("Sorry incorrect")
        else:
            print("lesgoo")
            return render_template("Home.html")
    return render_template('UserLogin.html')

@app.route('/userRegister',methods=['GET','POST'])
def userRegister():
    if request.method == 'POST':
        load_dotenv()

        connection = sqlite3.connect('parkSupp_DATABASE.db')
        cursor = connection.cursor()

        username = request.form['username']
        password = request.form['password']
        firstName = request.form['firstName']
        middleName = request.form['middleName']
        lastName = request.form['lastName']
        email = request.form['email']
        userType = request.form['userType']
        userValidID = request.form['validID']
        userRegistration = str(datetime.datetime.now())

        #generate both date and user ID
        increment = int(os.environ["USERID"])
        increment +=1
        userID = str(increment)
        os.environ["USERID"] = str(increment)
        dotenv.set_key(dotenv_file, "USERID", os.environ["USERID"])


        print(username, password, firstName, middleName, lastName,
              email, userType, userID, userRegistration, userValidID)

        #dadamihan pa ito
        queryInsert = "INSERT INTO user_Table VALUES ('"+userID+"', '"+firstName+"', '"+middleName+"', '" +lastName+"', '"+username+"','"+password+"', '"+userType+"', '"+userValidID+"', '"+email+"', '"+userRegistration+"')"
        print
        #validate if user exists in the database
        query = "SELECT user_id FROM user_Table WHERE user_id ='" + userID + "'"

        cursor.execute(query)

        results = cursor.fetchall()

        # kapag wala sa database, allow their data to be registered
        if len(results) == 0:
            cursor.execute(queryInsert)
            connection.commit()
            print("registered ka na boy")
        else:
            print("sorry nasa system ka na men")
            return render_template('register.html')

    return render_template('UserRegister.html')

@app.route('/userProfile')
def userProfile():
    return render_template('UserProfile.html')

@app.route('/verifyGuest')
def verifyGuest():
    return render_template('verifyGuest.html')

@app.route('/adminSetupParking')
def adminSetupPark():
    return render_template('adminSetupParking.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    global userView, adminView
    userView = False
    adminView = True
    return render_template('Admin.html')

# Video feeds for the website
@app.route('/video_feed_user')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



#FIX THIS MY MAN=========================================
@app.route('/requests', methods=['POST', 'GET'])
def functions():
    global camera, switch

    list = threading.enumerate()
    for t in list:
        print(f'{t} ello')

    if request.method == 'POST':
        allFunctions = {}
        currentMode = ""
        if request.form.get('user') == 'User View':
            global userView
            userView = not userView
            currentMode = "userView"
            return render_template('Home.html')
            #this is a true and false, a boolean if you would call it
        elif request.form.get('admin') == 'Admin View':
            global adminView
            adminView = not adminView
            currentMode = "adminView"
            return render_template('Admin.html')


        elif request.form.get('adminEntrance') == 'Create parking entrance':
            global adminEntranceCreate
            adminEntranceCreate = not adminEntranceCreate
            currentMode = "adminEntrance"
            return render_template('Admin.html')

        elif request.form.get('adminCreate') == 'Create parking slots':
            global adminLotCreator
            adminLotCreator = not adminLotCreator
            currentMode = "adminEntranceCreate"

        elif request.form.get('adminAssign') == 'Assign lot to user':
            global adminAssignLot
            adminAssignLot = not adminAssignLot
            currentMode = "adminAssignLot"

        elif request.form.get('adminSnap') == 'Capture parking lot':
            global adminCapture
            adminCapture = 1
            currentMode = "adminCapture"


        for key, value in allFunctions.items():
            print(f'{key} and {value}')
            if key != currentMode:
                value = False
            print(f'{threading.current_thread()} while {key} and {value}')

    elif request.method == 'GET':
        return render_template('Home.html')
    # refreshes the index.html

if __name__=='__main__':
    app.run(debug=True)