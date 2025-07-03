import cv2
import numpy as np

capture = cv2.VideoCapture(0)#0为电脑内置摄像头
ret, frame = capture.read()         #摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
# 加载图像
image = frame
image_resized = cv2.resize(image, None, fx=1, fy=1)
# 将图像从 RGB 转换为 HSV
image_hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)

# 创建一个窗口q
cv2.namedWindow("Image with HSV Adjustments")

# 设置滑条的初始值范围 (0-255)
def nothing(x):
    pass

# 创建三个滑条，分别对应 HSV 的三个通道：H, S, V
cv2.createTrackbar('H_lower', 'Image with HSV Adjustments', 0, 179, nothing)
cv2.createTrackbar('H_upper', 'Image with HSV Adjustments', 179, 179, nothing)
cv2.createTrackbar('S_lower', 'Image with HSV Adjustments', 0, 255, nothing)
cv2.createTrackbar('S_upper', 'Image with HSV Adjustments', 255, 255, nothing)
cv2.createTrackbar('V_lower', 'Image with HSV Adjustments', 0, 255, nothing)
cv2.createTrackbar('V_upper', 'Image with HSV Adjustments', 255, 255, nothing)

while True:
    # 获取滑条的当前值
    h_lower = cv2.getTrackbarPos('H_lower', 'Image with HSV Adjustments')
    h_upper = cv2.getTrackbarPos('H_upper', 'Image with HSV Adjustments')
    s_lower = cv2.getTrackbarPos('S_lower', 'Image with HSV Adjustments')
    s_upper = cv2.getTrackbarPos('S_upper', 'Image with HSV Adjustments')
    v_lower = cv2.getTrackbarPos('V_lower', 'Image with HSV Adjustments')
    v_upper = cv2.getTrackbarPos('V_upper', 'Image with HSV Adjustments')

    # 设置 HSV 的范围
    lower_bound = np.array([h_lower, s_lower, v_lower])
    upper_bound = np.array([h_upper, s_upper, v_upper])

    # 使用inRange方法提取图像在 HSV 范围内的部分
    mask = cv2.inRange(image_hsv, lower_bound, upper_bound)

    # 将 mask 应用于原图像，得到调整后的图像
    result = cv2.bitwise_and(image_resized, image_resized, mask=mask)

    # 显示处理后的图像
    cv2.imshow("Image with HSV Adjustments", result)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关闭所有OpenCV窗口
cv2.destroyAllWindows()
