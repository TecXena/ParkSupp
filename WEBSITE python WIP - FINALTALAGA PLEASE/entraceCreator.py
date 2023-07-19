import cv2

global image, img, a, b,c,d
image = None
img = None
a = 0
b = 0
c =0
d = 0

def initializeEntrance():
    print("[INFO] Loading parking lot image ...")

    global image, img, a, b, c, d
    image = "carParkImg.png"

    img = cv2.imread(image)

    file = open("CarParkEntryCoords.txt", "r+")

    file.truncate(0)

    file.close()

    ix = -1
    iy = -1
    drawing = False

    a = 0
    b = 0
    c = 0
    d = 0


def draw_reactangle_with_drag(event, x, y, flags, param):
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

def drawEntrance():
    initializeEntrance()
    while True:
        intro = "Click and drag to draw parking entrance."
        instrucEnter = "Press ENTER to save."
        instructDone= "Image saved!Press ESC to exit"
        #bottom rec
        cv2.rectangle(img, (0, 410), (800, 460), (33, 33, 33), -1)
        #upper rec
        cv2.rectangle(img, (0, 10), (800, 50), (33, 33, 33), -1)
        cv2.putText(img=img,
                    text="",
                    org=(10, 430),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(0, 255, 0),
                    thickness=1)
        cv2.putText(img=img,
                    text="",
                    org=(10, 450),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(0, 255, 0),
                    thickness=1)
        cv2.imshow("Parking entrance", img)

        cv2.setMouseCallback("Parking entrance", draw_reactangle_with_drag)

        if cv2.waitKey(5) == 13:
            #Enter
            print("TEST")
            cv2.imwrite("carParkImg.png", img)

            with open('CarParkEntryCoords.txt', 'a') as file:
                file.write("{} {} {} {}\n".format(a, b, c, d))
            break

        if cv2.waitKey(5) == 27:
            # esc
            print("[INFO] Exit drawing parking entrance.")
            cv2.destroyAllWindows()
            break


