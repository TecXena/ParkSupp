import threading

from flask import Flask, render_template, Response, request

import entraceCreator
from lotAvailability import parking_availability
import entraceCreator as entrance
#import lotCreator
import cv2
import viewParking_ForTest3 as view
import adminParking as admin
import dotenv
import time



app=Flask(__name__)
camera = cv2.VideoCapture(0)

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
                entraceCreator.drawEntrance()
            if (adminLabelLots):
                print("prototype")
            if (adminLotCreator):
                print("prototype")
            if (adminCapture):
                capture = 0
                cv2.imwrite("carParkImg.png", frame)
            if (adminAssignLot):
                print("prototype")

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


@app.route('/')
def index():
    return render_template('index.html')


# Video feeds for the website
@app.route('/video_feed_user')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests', methods=['POST', 'GET'])

def adminFunctions():
    if request.method == 'POST':
        allFunctions = {}
        currentMode = ""
        if request.form.get('adminEntrance') == 'Create parking entrance':
            global adminEntranceCreate
            adminEntranceCreate = not adminEntranceCreate
            currentMode = "adminEntrance"
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
            #this is a true and false, a boolean if you would call it
        elif request.form.get('admin') == 'Admin View':
            global adminView
            adminView = not adminView
            currentMode = "adminView"

            currentMode = "adminCapture"
        # extra function that automatically turns off the list of all functions? or maybe the previously sent one
        #allFunctions['userView'] = userView
        #allFunctions['adminView']= adminView
        #allFunctions['adminEntranceCreate'] = adminEntranceCreate
        #allFunctions['adminLotCreator'] = adminLotCreator
        #allFunctions['adminAssignLot'] = adminAssignLot
        #print(allFunctions)
        #allFunctKeys = allFunctions.keys()
        #allFunctValues = allFunctions.values()
        print(currentMode)
        # first, append the current states of the functions
        # then, save the current mode
        # now use a for loop to turn off all other modes except the same one

        for key, value in allFunctions.items():
            print(f'{key} and {value}')
            if key != currentMode:
                value = False
            print(f'{threading.current_thread()} while {key} and {value}')

    elif request.method == 'GET':
        return render_template('index.html')
    # refreshes the index.html
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)