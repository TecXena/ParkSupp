import cv2


cap = cv2.VideoCapture(0)
cap.read
print(cap.isOpened())
while True:
    ret,img=cap.read()
    cv2.imshow('a', cap)


cap.release()
cv2.destroyAllWindows()