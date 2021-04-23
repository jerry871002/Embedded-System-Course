#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# image_face_detect_run.py
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

detector = dlib.get_frontal_face_detector()
faces, scores, idx = detector.run(image, 0, 0)

print("Found {0} faces!".format(len(faces)))

for i, face in enumerate(faces):
    x1 = face.left() 
    y1 = face.top() 
    x2 = face.right() 
    y2 = face.bottom() 

    text = "%2.2f(%d)" % (scores[i], idx[i])
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 
          0.7, (0, 255, 0), 1)

cv2.imshow("preview", image)
cv2.waitKey(0)

cv2.destroyAllWindows()
