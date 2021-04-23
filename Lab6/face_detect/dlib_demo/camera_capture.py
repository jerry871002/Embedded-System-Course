#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# camera_capture.py
# Usage: python3 camera_capture.py

import cv2
import os
import time
import imutils

if not os.path.exists('images'):
    print('mkdir images')
    os.mkdir('images')

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, 640)
        cv2.putText(frame, "press 'c' to capture ", (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255))
        cv2.putText(frame, "press 'q' to quit ", (25, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255))
        cv2.imshow("preview", frame)

        if cv2.waitKey(1) & 0xFF == ord("c"):
            fn = str(int(time.time())) + ".jpg"
            print('save to ' + 'images/' + fn)
            cv2.imwrite('images/' + fn, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.01)

finally:
    cap.release()
    cv2.destroyAllWindows()


