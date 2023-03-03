import cv2
import numpy as np
from PyQt5.QtGui import *
import math

def cvimg_to_qtimg(cvimg):
    cvimg = cvimg.astype(np.uint8)
    height, width, channels = cvimg.shape[:3]
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    cvimg = QImage(cvimg.data, width, height, width * channels, QImage.Format_RGB888)

    return cvimg

def resize_picture(img,width,height):
    w = np.array(img).shape[1]
    h = np.array(img).shape[0]

    if w / width >= h / height:
        ratio = w / width
    else:
        ratio = h / height
    new_width = int(w / ratio)
    new_height = int(h / ratio)

    return new_width,new_height
