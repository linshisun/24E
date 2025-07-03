import cv2 as cv
import numpy as np
import rectan
import pick_color
import spin
import houghcircle
import play

def sort_vertices(points):
    # 计算中心点
    center_x = sum(p[0] for p in points) / 4
    center_y = sum(p[1] for p in points) / 4

    # 分组并排序
    left = sorted([p for p in points if p[0] < center_x], key=lambda x: x[1])  # 左下→左上
    right = sorted([p for p in points if p[0] >= center_x], key=lambda x: x[1])  # 右上→右下

    return left + right

def Squre_sort(img):
    image = pick_color.pick_red(img)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edged = cv.Canny(blurred, 30, 150)
    square_centers, img = rectan.SqureDetection(edged)
    # 如果拍的不对就一直拍
    while len(square_centers) != 9:
        capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
        ret, img = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
        while ret == 0:
            capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
            ret, img = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
        image = pick_color.pick_red(img)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0)
        edged = cv.Canny(blurred, 30, 150)
        square_centers, img = rectan.SqureDetection(edged)
    print(square_centers)
    sorted_xy = [[(i, j) for j in range(3)] for i in range(3)]

    min_x = square_centers[0][0]
    min_y = square_centers[0][1]
    max_x = square_centers[0][0]
    max_y = square_centers[0][1]

    for x, y in square_centers:
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    # 这个算法的鲁棒性有待考察
    for i, j in square_centers:
        row = round((j - min_y) / ((max_y - min_y) / 2))
        col = round((i - min_x) / ((max_x - min_x) / 2))
        sorted_xy[row][col] = (i,j)

    return sorted_xy,img

def Circle_sort(img, Black = 1, White = -1, Unset = 0):
    white = pick_color.pick_white(img)
    white_img, white_centers =houghcircle.hough_circle(white)
    white_unset = []

    black = pick_color.pick_black(img)
    black_img, black_centers = houghcircle.hough_circle(black)
    black_unset = []

    while len(white_centers[0]) != 5 or len(black_centers[0]) != 5:
        capture = cv.VideoCapture(0, cv.CAP_DSHOW)  # 0为电脑内置摄像头
        ret, img = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
        while ret == 0:
            capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
            ret, img = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
        image = pick_color.pick_red(img)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0)
        edged = cv.Canny(blurred, 30, 150)
        square_centers, img = rectan.SqureDetection(edged)

    board = play.Board()

    red = pick_color.pick_red(img)
    gray = cv.cvtColor(red, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edged = cv.Canny(blurred, 30, 150)
    square_centers, img = rectan.SqureDetection(edged)

    min_x = square_centers[0][0]
    min_y = square_centers[0][1]
    max_x = square_centers[0][0]
    max_y = square_centers[0][1]

    for x, y in square_centers:
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    for i, j, k in white_centers[0]:
        if i > 520 :
            white_unset.append((round(i),round(j)))
        elif i < 520:
            row = round((j - min_y) / ((max_y - min_y) / 2))
            col = round((i - min_x) / ((max_x - min_x) / 2))
            board.cells[row][col].is_occupied = 1
            board.cells[row][col].color = White
            board.cells[row][col].piece = (i,j)

    for i, j, k in black_centers[0]:
        if i < 130:
            black_unset.append((round(i),round(j)))
        elif i > 130:
            row = round((j - min_y) / ((max_y - min_y) / 2))
            col = round((i - min_x) / ((max_x - min_x) / 2))
            board.cells[row][col].is_occupied = 1
            board.cells[row][col].color = Black
            board.cells[row][col].piece = (i, j)

    if white_unset != []:
        white_unset = sorted(white_unset, key=lambda x: x[1])
    if black_unset != []:
        black_unset = sorted(black_unset, key=lambda x: x[1])

    return white_unset, black_unset, board

if __name__ == '__main__':
    capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
    ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
    sorted_xy, img = Squre_sort(image)
    print(sorted_xy)
    white_unset, black_unset, board = Circle_sort(image)
    # board_vector = [
    #     [0, 0, 0],
    #     [0, 0, 0],
    #     [0, 0, 0]
    # ]
    # for row in board.cells:  # 遍历每一行
    #     for cell in row:  # 遍历行中的每个格子
    #         board_vector[cell.row][cell.column] = cell.color
    # print(board_vector)
    # print(board_vector)
    print(white_unset)
    print(black_unset)
    cv.waitKey(0)