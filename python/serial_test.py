import serial
import cv2
import numpy as np
import perspectiveTransform

def mouse_callback(event, x, y, flags, userdata):
    # 如果鼠标左键点击，则输出横坐标和纵坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        Circle_perspective = perspectiveTransform.cvt_pos((x,y), M)
        print(Circle_perspective)

pts1 = np.float32([[156, 175], [450, 178], [154, 466], [445, 470]])
pts2 = np.float32([[174, 16], [78, 16], [174, 112], [78, 112]])
M = cv2.getPerspectiveTransform(pts1, pts2)
M_inv = np.linalg.inv(M)
# 串口输出。
capture = cv2.VideoCapture(0)  # 0为电脑内置摄像头
ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
image = cv2.resize(image, None, fx=1, fy=1)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)
cv2.setMouseCallback('gray', mouse_callback)
cv2.waitKey(0)

