import cv2
import os.path
#saves position of parking spaces and brings to main code


try:
    file = open("CarParkCoords.txt")
    lines = file.readlines()

    lines = [line.strip() for line in lines]

    parking_lot_coords = []

    for i in range(len(lines)):
        coords = lines[i].split()

        left = int(coords[0])

        top = int(coords[1])

        right = int(coords[2])

        bottom = int(coords[3])

        coords = [left, top, right, bottom]

        parking_lot_coords.append(coords)

    file = open("CarParkCoordsStartLoc.txt")
    lines = file.readlines()

    lines = [line.strip() for line in lines]

    parking_lot_startLoc = []
    for i in range(len(lines)):
        locations = lines[i].split()
        parking_lot_startLoc.append(locations)

except:
    #create a new posList
    parking_lot_coords = []
    parking_lot_startLoc = []


ix = -1
iy = -1
drawing = False

a = 0
b = 0
c = 0
d = 0
parking_lot = 0
image = 'carParkImg.png'
img = cv2.imread(image)


def draw_rectangle_with_drag(event, x, y, flags, param):
    global ix, iy, drawing, img, a, b, c, d
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y


    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img = cv2.imread(image)
            cv2.rectangle(img,
                          pt1=(ix, iy),
                          pt2=(x, y),
                          color=(0, 0, 255),
                          thickness=2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img = cv2.imread(image)
        cv2.rectangle(img,
                      pt1=(ix, iy),
                      pt2=(x, y),
                      color=(0, 0, 255),
                      thickness=2)

        a = ix
        b = iy
        c = x
        d = y
        parking_lot_coords.append((a, b,c,d))

        if a < c:
            print("1")
            if b > d:
                parking_lot_startLoc.append("Bot-L")
                print("Bot-L")
            elif b < d:
                parking_lot_startLoc.append("Up-L")
                print("Up-L")
        elif a > c:
            print("2")
            if b > d:
                parking_lot_startLoc.append("Bot-R")
                print("Bot-R")
            elif b < d:
                parking_lot_startLoc.append("Up-R")
                print("Up-R")

        print(parking_lot_coords)
        print(parking_lot_startLoc)

    elif event == cv2.EVENT_RBUTTONDOWN: # delete position to posList
        for i, pos in enumerate(parking_lot_coords):
            x1, y1,x2,y2 = pos  # get previous x & y of box
            width = abs(x1-x2)
            height = abs(y1-y2)
            print(parking_lot_coords)
            #starts at upper right

            if x1 > x > x1-width and y1 < y < y1+height:
                print("Up-R")
                parking_lot_startLoc.pop(i)
                parking_lot_coords.pop(i)
            # start at bottom right
            elif x1 > x > x1-width and y1 > y > y1-height:
                print("Bot-R")
                parking_lot_startLoc.pop(i)
                parking_lot_coords.pop(i)
            #starts at bottom left
            elif x1 < x < x1+width and y1 > y > y1-height:
                print("Bot-L")
                parking_lot_startLoc.pop(i)
                parking_lot_coords.pop(i)
            # start at upper left
            elif x1 < x < x1+width and y1 < y < y1+height:
                print("Up-L")
                parking_lot_startLoc.pop(i)
                parking_lot_coords.pop(i)
        img = cv2.imread('carParkImg.png')


while True:
    for lot in parking_lot_coords:
        cv2.rectangle(img, (lot[0],lot[1]), (lot[2], lot[3]), (255, 0, 255), 2)

    cv2.imshow("Parking area", img)# para palagi narerefresh at hindi static and image
    cv2.setMouseCallback("Parking area", draw_rectangle_with_drag)
    if cv2.waitKey(5) == 32:
        #space
        print("[INFO] SPACE pressed! New parking area/s saved.")
        parking_lot += 1
        cv2.imwrite("parking_lot.png", img)
        with open('CarParkCoords.txt', 'w') as file:
            file.truncate()
            i = 0
            while i < len(parking_lot_coords):
                file.write("{} {} {} {}\n".format(parking_lot_coords[i][0], parking_lot_coords[i][1], parking_lot_coords[i][2], parking_lot_coords[i][3]))
                i+=1

        with open('CarParkCoordsLoc.txt', 'w') as file:
            file.truncate()
            i = 0
            while i < len(parking_lot_startLoc):
                file.write("{}\n".format(parking_lot_startLoc[i]))
                i+=1
        continue


