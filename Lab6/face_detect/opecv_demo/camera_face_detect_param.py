#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# camera_face_detect.py
# Face detect from camera
#
# Author : Fletcher Heisler, Michael Herman, Jeremy Johnson
# Date   : 06/22/2014
# Origin : https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/
# Usage  : python3 camera_face_detect.py haarcascade_frontalface_default.xml

import cv2
import sys
import time
import imutils

def nothing(x):
    pass

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
cap = cv2.VideoCapture(0)

cv2.namedWindow('face_detect')
cv2.createTrackbar('scaleFactor', 'face_detect', 0, 10, nothing)
cv2.createTrackbar('minNeighbor', 'face_detect', 0, 10, nothing)
cv2.createTrackbar('minSize_n2',  'face_detect', 0, 10, nothing)

try:
    while True:
        scaleFactor = cv2.getTrackbarPos('scaleFactor', 'face_detect')
        minNeighbor = cv2.getTrackbarPos('minNeighbor', 'face_detect')
        minSize_n2  = cv2.getTrackbarPos('minSize_n2',  'face_detect')

        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = imutils.resize(frame, 320)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        print(1+(scaleFactor/10))
        print(1+minNeighbor)
        print((pow(1+minSize_n2, 2), pow(1+minSize_n2, 2)))

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1+((1+scaleFactor)/10),
            minNeighbors=1+minNeighbor,
            minSize=(pow(1+minSize_n2, 2), pow(1+minSize_n2, 2)),
            flags = cv2.CASCADE_SCALE_IMAGE,      # OpenCV3
            #flags = cv2.CV_FEATURE_PARAMS_HAAR,  # OpenCV4
        )

        print("Found {0} faces!".format(len(faces)))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow("face_detect", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.01)

finally:
    cap.release()
    cv2.destroyAllWindows()

