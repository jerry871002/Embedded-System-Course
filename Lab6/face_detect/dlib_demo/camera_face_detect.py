#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# camera_face_detect.py
# Face detect from camera
#
# Date   : 2021/04/15
# Origin : https://github.com/davisking/dlib/blob/master/python_examples/face_detector.py

import cv2
import dlib
import time
import imutils

detector = dlib.get_frontal_face_detector()
cap = cv2.VideoCapture(0)

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = imutils.resize(frame, 320)

        faces, scores, idx = detector.run(frame, 0, 0)

        print("Found {0} faces!".format(len(faces)))

        for i, face in enumerate(faces):
            x1 = face.left() 
            y1 = face.top() 
            x2 = face.right() 
            y2 = face.bottom() 

            text = "%2.2f(%d)" % (scores[i], idx[i])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 
                  0.7, (0, 255, 0), 1)

        # Display the resulting frame
        cv2.imshow("preview", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.01)

finally:
    cap.release()
    cv2.destroyAllWindows()

