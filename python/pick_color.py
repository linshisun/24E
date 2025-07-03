#提取颜色的模块
import cv2
import numpy as np

#黄色: H:30~85
#红色: H:123~179  S:39~143  V:95~255
#白色: H:87~116   S:48~112  V:211~255
#黑色: H:89~110   S:116~255  V:58~255

def pick_yellow(image):
    image_resized = cv2.resize(image, None, fx=1, fy=1)
    # 将图像从 RGB 转换为 HSV
    image_hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)

    # 设置 HSV 的范围
    lower_bound = np.array([30, 0, 0])
    upper_bound = np.array([86, 255, 255])

    # 使用inRange方法提取图像在 HSV 范围内的部分
    mask = cv2.inRange(image_hsv, lower_bound, upper_bound)

    # 将 mask 应用于原图像，得到调整后的图像
    result = cv2.bitwise_and(image_resized, image_resized, mask=mask)

    return result

def pick_red(image):
    image_resized = cv2.resize(image, None, fx=1, fy=1)
    # 将图像从 RGB 转换为 HSV
    image_hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)

    # 设置 HSV 的范围
    lower_bound = np.array([122, 86, 112])
    upper_bound = np.array([179, 255, 255])

    # 使用inRange方法提取图像在 HSV 范围内的部分
    mask = cv2.inRange(image_hsv, lower_bound, upper_bound)

    # 将 mask 应用于原图像，得到调整后的图像
    result = cv2.bitwise_and(image_resized, image_resized, mask=mask)

    return result

def pick_white(image):
    image_resized = cv2.resize(image, None, fx=1, fy=1)
    # 将图像从 RGB 转换为 HSV
    image_hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)

    # 设置 HSV 的范围
    lower_bound = np.array([50, 16, 158])
    upper_bound = np.array([147, 107, 255])

    # 使用inRange方法提取图像在 HSV 范围内的部分
    mask = cv2.inRange(image_hsv, lower_bound, upper_bound)

    # 将 mask 应用于原图像，得到调整后的图像
    result = cv2.bitwise_and(image_resized, image_resized, mask=mask)

    return result

def pick_black(image):
    image_resized = cv2.resize(image, None, fx=1, fy=1)
    # 将图像从 RGB 转换为 HSV
    image_hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)

    # 设置 HSV 的范围
    lower_bound = np.array([43, 0, 0])
    upper_bound = np.array([177, 255, 150])

    # 使用inRange方法提取图像在 HSV 范围内的部分
    mask = cv2.inRange(image_hsv, lower_bound, upper_bound)

    white = np.ones_like(image_resized, dtype=np.uint8) * 255
    # 将 mask 应用于白色图像，得到调整后的图像
    result = cv2.bitwise_not(white, white, mask=mask)

    return result

#测试
if __name__ == '__main__':
    capture = cv2.VideoCapture(0)  # 0为电脑内置摄像头
    ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
    img = cv2.resize(image, None, fx=1, fy=1)

    yellow = pick_yellow(img)
    cv2.imshow("yellow", yellow)

    red = pick_red(img)
    cv2.imshow("red", red)

    white = pick_white(img)
    cv2.imshow("white", white)

    black = pick_black(img)
    cv2.imshow("black", black)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
