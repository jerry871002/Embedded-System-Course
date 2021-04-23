#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# test_object_detector.py
#
# Date   : 2021/04/15
# Origin : http://dlib.net/train_object_detector.py.html

import imutils
import dlib
import cv2

# Now let's use the detector as you would in a normal application.  First we
# will load it from disk.
detector = dlib.simple_object_detector("detector.svm")

# Video capture source
cap = cv2.VideoCapture(0)

# We can look at the HOG filter we learned.  It should look like a face.  Neat!
win_det = dlib.image_window()
win_det.set_image(detector)

try:
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, 320)

        rects = detector(frame)

        for k, d in enumerate(rects):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
            cv2.rectangle(frame,(d.left(), d.top()),(d.right(), d.bottom()),(0,255,0), 2 )

        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()


