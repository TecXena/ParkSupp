#content of admin

import cv2
import glob
import os


def TakePhoto(frame):
    # set up clean slate
    removeOldPhotos = glob.glob('parkingLots/*.jpg')
    for i in removeOldPhotos:
        os.remove(i)
    if os.path.exists("carParkImg.png") and os.path.exists("parking_lot.png"):
        os.remove("carParkImg.png")
        os.remove("parking_lot.png")

    cv2.putText(img=frame,
                text="Press space to save a photo of your parking lot",
                org=(10, 430),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(0, 255, 0),
                thickness=1)
    cv2.putText(img=frame,
                text="Press ESC to exit the program",
                org=(10, 450),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(0, 255, 0),
                thickness=1)
