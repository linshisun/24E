import serial
import perspectiveTransform
import numpy as np
import cv2 as cv

pts1 = np.float32([[156, 175], [450, 178], [154, 466], [445, 470]])
pts2 = np.float32([[174, 16], [78, 16], [174, 112], [78, 112]])
M = cv.getPerspectiveTransform(pts1, pts2)
M_inv = np.linalg.inv(M)

newpoint = perspectiveTransform.cvt_pos([332,149], M)
print(newpoint)