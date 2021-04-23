#!/usr/bin/python3

import numpy as np
import cv2
import sys
import time

drawing = False 
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1

# mouse callback function
def callback(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, img_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        print("Dn => ix=",ix,"iy=",iy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(img, (ix,iy), (x,y), (0,255,255), 0)
            print("Up => ix=",x,"iy=",y)
            crop = img[iy:y, ix:x]
            cv2.imwrite("sample.jpg", crop)


if __name__ == "__main__":
    try:
        imagePath = sys.argv[1]
    except:
        imagePath = "capture.jpg"

    img = cv2.imread(imagePath)
    img_copy = img.copy()

    cv2.namedWindow("sample")
    cv2.setMouseCallback("sample", callback)

    while True:
        #cv2.putText(img, "press 'q' to quit ", (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
        cv2.imshow("sample", img)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('m'):
            mode = not mode
        elif k == ord('q'):
            break

        time.sleep(0.01)

    cv2.destroyAllWindows()

