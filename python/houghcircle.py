import cv2 as cv
import pick_color

def hough_circle(image):
    img = image.copy()
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 进行中值滤波
    dst_img = cv.medianBlur(img_gray, 7)

    # 霍夫圆检测
    circle = cv.HoughCircles(dst_img, cv.HOUGH_GRADIENT, 1, 20,
                             param1=100, param2=14, minRadius=15, maxRadius=40)

    # 将检测结果绘制在图像上
    for i in circle[0, :]:  # 遍历矩阵的每一行的数据
        # 绘制圆形
        cv.circle(img, (int(i[0]), int(i[1])), int(i[2]), (255, 0, 0), 2)
        # 绘制圆心
        cv.circle(img, (int(i[0]), int(i[1])), 2, (255, 0, 0), -1)
    return img, circle

if __name__ == '__main__':
    capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
    ret, img = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
    img = pick_color.pick_white(img)
    cv.imshow('img', img)
    image,circle = hough_circle(img)
    cv.imshow('circle', image)
    print(circle)
    cv.waitKey(0)
    cv.destroyAllWindows()