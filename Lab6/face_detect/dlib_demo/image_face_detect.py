#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# image_face_detect.py
# Face detect from image
#
# Date   : 2021/04/15
# Origin : https://github.com/davisking/dlib/blob/master/python_examples/face_detector.py

import cv2
import dlib
import sys

try:
    imagePath = sys.argv[1]
except:
    # https://edition.cnn.com/2016/07/18/opinions/trump-family-production-dantonio/index.html
    imagePath = 'trump_family.jpg'

image = cv2.imread(imagePath)

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
faces = detector(image, 1)

print("Found {0} faces!".format(len(faces)))

for face in faces:
    x1 = face.left() # left point
    y1 = face.top() # top point
    x2 = face.right() # right point
    y2 = face.bottom() # bottom point
    # Draw a rectangle
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("preview", image)
cv2.waitKey(0)

cv2.destroyAllWindows()
