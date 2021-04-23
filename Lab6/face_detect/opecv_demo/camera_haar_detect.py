#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# camera_haar_detect.py
# Object detect from camera by haar classifier

import cv2
import sys
import time
import imutils

def nothing(x):
    pass

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

cv2.namedWindow('haar')
cv2.createTrackbar('minNeib', 'haar', 0, 50, nothing)
cv2.createTrackbar('minSize', 'haar', 0, 100, nothing)

cap = cv2.VideoCapture(0)

try:
    while True:
        minNeib = cv2.getTrackbarPos('minNeib', 'haar')
        minSize = cv2.getTrackbarPos('minSize', 'haar')

        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = imutils.resize(frame, 320)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=minNeib,
            minSize=(minSize, minSize),
            flags = cv2.CASCADE_SCALE_IMAGE,      # OpenCV3
            #flags = cv2.CV_FEATURE_PARAMS_HAAR,  # OpenCV4
        )

        print("Found {0} objects!".format(len(objects)))

        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow("haar", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.01)

finally:
    cap.release()
    cv2.destroyAllWindows()

