#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2017, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# resize.py
#
# Author : sosorry
# Date   : 2017/07/27
# Usage  : python3 resize.py

import cv2
import numpy as np
import sys

try:
    imagePath = sys.argv[1]
except:
    imagePath = "lena256rgb.jpg"

image = cv2.imread(imagePath)
rows, cols = image.shape[:2]

cv2.imshow('Resize', image)
cv2.waitKey(0)

resize = cv2.resize(image, (24, 24), interpolation = cv2.INTER_CUBIC)
cv2.imshow('Resize', resize)
cv2.waitKey(0)
cv2.imwrite("resized.jpg", resize)

cv2.destroyAllWindows()

