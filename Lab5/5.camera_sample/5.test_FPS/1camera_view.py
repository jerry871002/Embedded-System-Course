# import the necessary packages
from __future__ import print_function
from imutils.video import FPS

import imutils
import time
import cv2

try:
    # grab a pointer to the video stream 
    # and initialize the FPS counter
    print("[INFO] sampling frames from webcam...")
    vs = cv2.VideoCapture(0)
    time.sleep(2.0)
    fps = FPS().start()

    # loop over some frames
    while True:
        # grab the frame from the stream and resize it to have a maximum
        # width of 400 pixels
        (grabbed, frame) = vs.read()
        frame = imutils.resize(frame, width=400)

        # update the FPS counter
        fps.update()

        # Display image
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break # press q to quit without calculating
            
except KeyboardInterrupt:
    # Use ctrl + c to stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    vs.release()
    cv2.destroyAllWindows()
