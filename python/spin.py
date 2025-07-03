import numpy as np
import cv2 as cv
import pick_color
import rectan

if __name__ == '__main__':
    # 示例使用
    capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
    ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
    image = pick_color.pick_red(image)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edged = cv.Canny(blurred, 30, 150)
    # cv.imshow('edged', edged)
    contours, hierarchy = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)  # 寻找轮廓点
    x_pre = 0
    y_pre = 0
    square_centers = []
    square_corners = []
    for obj in contours:
        area = cv.contourArea(obj)  # 计算轮廓内区域的面积
        perimeter = cv.arcLength(obj, True)  # 计算轮廓周长
        approx = cv.approxPolyDP(obj, 0.02 * perimeter, True)  # 获取轮廓角点坐标
        cv.drawContours(image, obj, -1, (255, 0, 0), 2)  # 绘制轮廓线
        CornerNum = len(approx)  # 轮廓角点的数量
        x, y, w, h = cv.boundingRect(approx)  # 获取坐标值和宽度、高度

        # 轮廓对象分类
        if CornerNum == 4:
            if w >= 0.9 * h and w <= 1.1 * h:
                objType = "Square"
            else:
                objType = "Rectangle"
        else:
            objType = "N"

        if objType == "Square" and 1000 < area < 40000:
            square_corners.append(approx)
            # 避免重复点位，打印的是左上角的点，设计一个数据结构，存放正方形的中心点
            if abs(x - x_pre) > 5 or abs(y - y_pre) > 5:
                x_pre = x
                y_pre = y
                # print(x,y)
                square_centers.append((x + (w // 2), y + (h // 2)))
                cv.putText(image, objType, (x + (w // 2), y + (h // 2)), cv.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0),
                            1)  # 绘制文字
    square_centers.reverse()
    print(square_centers)

    cv.waitKey(0)
