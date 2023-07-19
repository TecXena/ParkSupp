from lotAvailability import parking_availability
#import lotCreator
import cv2

def importCarParkCoords():
    file = open("CarParkCoords.txt")

    lines = file.readlines()

    lines = [line.strip() for line in lines]

    total_parking_lots = len(lines)

    parking_lot_coords = list()

    for i in range(len(lines)):
        coords = lines[i].split()

        left = int(coords[0])

        top = int(coords[1])

        right = int(coords[2])

        bottom = int(coords[3])

        coords = [left, top, right, bottom]

        parking_lot_coords.append(coords)
    return parking_lot_coords


def importCarParkCoordsLoc():
    file = open("CarParkCoordsLoc.txt")
    lines = file.readlines()

    lines = [line.strip() for line in lines]

    parking_lot_startLoc = []
    for i in range(len(lines)):
        locations = lines[i].strip()
        parking_lot_startLoc.append(locations)

    return parking_lot_startLoc

def mainCamera(parking_lot_coords,parking_lot_startLoc,frame, userType):
    print("telo")
    textUserType = ""
    # region loading the parking lots
    for i in range(len(parking_lot_coords)):
        if parking_lot_startLoc[i] == "Up-L":
            parking_lot = frame[parking_lot_coords[i][1]: parking_lot_coords[i][-1],
                          parking_lot_coords[i][0]: parking_lot_coords[i][2]]
            cv2.imwrite("parkingLots/{}.jpg".format(i), img=parking_lot)
        elif parking_lot_startLoc[i] == "Up-R":
            parking_lot = frame[parking_lot_coords[i][1]: parking_lot_coords[i][-1],
                          parking_lot_coords[i][2]: parking_lot_coords[i][0]]
            cv2.imwrite("parkingLots/{}.jpg".format(i), img=parking_lot)
        elif parking_lot_startLoc[i] == "Bot-R":
            parking_lot = frame[parking_lot_coords[i][-1]: parking_lot_coords[i][1],
                          parking_lot_coords[i][2]: parking_lot_coords[i][0]]
            cv2.imwrite("parkingLots/{}.jpg".format(i), img=parking_lot)
        elif parking_lot_startLoc[i] == "Bot-L":
            parking_lot = frame[parking_lot_coords[i][-1]: parking_lot_coords[i][1],
                          parking_lot_coords[i][0]: parking_lot_coords[i][2]]
            cv2.imwrite("parkingLots/{}.jpg".format(i), img=parking_lot)
        # Creates the frame for the parking lot
        cv2.rectangle(img=frame,
                      pt1=(parking_lot_coords[i][0], parking_lot_coords[i][1]),
                      pt2=(parking_lot_coords[i][2], parking_lot_coords[i][-1]),
                      color=(255, 0, 0),
                      thickness=1)

    parking_lots = parking_availability()

    available_parking_lot = parking_lots[0]

    unavailable_parking_lot = parking_lots[1]

    #print("Available:", available_parking_lot)
    #print("Unavailable:", unavailable_parking_lot)



    # FUCKING TEXT
    if userType == 1:
        textUserType = "USER MODE"
    elif userType == 2:
        textUserType = "ADMIN MODE"
    else:
        textUserType = "APESHIT MODE"
    cv2.putText(img=frame,
                text=textUserType,
                org=(10, 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(0, 255, 0),
                thickness=1)


    if len(unavailable_parking_lot) > 0:

        for i in range(len(unavailable_parking_lot)):
            cv2.rectangle(img=frame,
                          pt1=(unavailable_parking_lot[i][0], unavailable_parking_lot[i][1]),
                          pt2=(unavailable_parking_lot[i][2], unavailable_parking_lot[i][-1]),
                          color=(0, 0, 255),
                          thickness=1)
    if len(available_parking_lot) > 0:
        for i in range(len(available_parking_lot)):
            cv2.rectangle(img=frame,
                          pt1=(available_parking_lot[i][0], available_parking_lot[i][1]),
                          pt2=(available_parking_lot[i][2], available_parking_lot[i][-1]),
                          color=(0, 255, 0),
                          thickness=1)

    # endregion
