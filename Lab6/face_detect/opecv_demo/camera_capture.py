#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# camera_capture.py
# Usage: python3 camera_capture.py

import cv2
import time
import imutils

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, 320)
        cv2.imshow("preview", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.imwrite("capture.jpg", frame)
            break

        time.sleep(0.01)

finally:
    cap.release()
    cv2.destroyAllWindows()


