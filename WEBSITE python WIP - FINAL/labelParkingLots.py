import cv2


img = cv2.imread("parking_lot.png")

file = open("CarParkLotLabels.txt", "r+")

file.truncate(0)

file.close()

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

for i in range(len(parking_lot_coords)):

    if i > 0:
        cv2.rectangle(img=img,
                      pt1=(parking_lot_coords[i][0], parking_lot_coords[i][1]),
                      pt2=(parking_lot_coords[i][2], parking_lot_coords[i][-1]),
                      color=(0, 255, 255),
                      thickness=2)

        cv2.rectangle(img=img,
                      pt1=(parking_lot_coords[i - 1][0], parking_lot_coords[i - 1][1]),
                      pt2=(parking_lot_coords[i - 1][2], parking_lot_coords[i - 1][-1]),
                      color=(0, 255, 0),
                      thickness=2)

    if i == 0:
        cv2.rectangle(img=img,
                      pt1=(parking_lot_coords[i][0], parking_lot_coords[i][1]),
                      pt2=(parking_lot_coords[i][2], parking_lot_coords[i][-1]),
                      color=(0, 255, 255),
                      thickness=2)

    cv2.imshow("Parking lot", img)

    # Textbox sa flask para marecieve, probably a separate function tapos iincrement natin
    cv2.waitKey(10)

    parking_label = input("Enter this parking label: ")

    with open('CarParkLotLabels.txt', 'a') as file:

        file.write("{}\n".format(parking_label))

        print("[INFO] Parking {} is saved!".format(parking_label))

        continue
