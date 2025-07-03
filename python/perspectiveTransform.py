import cv2 as cv
import numpy as np
import serial

def cvt_pos(pos, cvt_mat_t):
    u = pos[0]
    v = pos[1]
    x = (cvt_mat_t[0][0] * u + cvt_mat_t[0][1] * v + cvt_mat_t[0][2]) / (
                cvt_mat_t[2][0] * u + cvt_mat_t[2][1] * v + cvt_mat_t[2][2])
    y = (cvt_mat_t[1][0] * u + cvt_mat_t[1][1] * v + cvt_mat_t[1][2]) / (
                cvt_mat_t[2][0] * u + cvt_mat_t[2][1] * v + cvt_mat_t[2][2])
    return (round(x), round(y))

if __name__ == '__main__':
    pts1 = np.float32([[211, 119], [456, 118], [213, 365], [459, 365]])
    pts2 = np.float32([[40, 65], [-40, 65], [45, 155], [-45, 155]])

    M = cv.getPerspectiveTransform(pts1, pts2)
    M_inv = np.linalg.inv(M)  # 矩阵求逆
    newpoint = cvt_pos([122.5,368.5], M)
    print(newpoint)
