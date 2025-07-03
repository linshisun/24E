import cv2
import pick_color

# 回调函数：鼠标点击输出点击的坐标
# （事件（鼠标移动、左键、右键），横坐标，纵坐标，组合键，setMouseCallback的userdata用于传参）
def mouse_callback(event, x, y, flags, userdata):
    # 如果鼠标左键点击，则输出横坐标和纵坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'({x}, {y})')
        # 获取指定像素点的颜色
        pixel_color = gray[x, y]
        print("颜色值BGR：", pixel_color)

# 定义形状检测函数，主要用于矩形和正方形检测
def SqureDetection(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)  #寻找轮廓点
    x_pre = 0
    y_pre = 0
    square_centers = []
    for obj in contours:
        area = cv2.contourArea(obj)  #计算轮廓内区域的面积
        perimeter = cv2.arcLength(obj,True)  #计算轮廓周长
        approx = cv2.approxPolyDP(obj,0.02*perimeter,True)  #获取轮廓角点坐标
        cv2.drawContours(img, obj, -1, (255, 0, 0), 2)  # 绘制轮廓线
        CornerNum = len(approx)   #轮廓角点的数量
        x, y, w, h = cv2.boundingRect(approx)  #获取坐标值和宽度、高度

        #轮廓对象分类
        if CornerNum == 4:
            # print(1)
            if w >= 0.9*h and w <= 1.1*h:
                objType= "Square"
            else:objType="Rectangle"
        else:objType="N"

        if objType=="Square" and 500 < area < 40000:
            #避免重复点位，打印的是左上角的点，设计一个数据结构，存放正方形的中心点
            if abs(x - x_pre) > 5 or abs(y - y_pre) > 5:
                x_pre = x
                y_pre = y
                # print(x,y)
                square_centers.append((x+(w//2),y+(h//2)))
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)  #绘制边界框
                cv2.putText(img,objType,(x+(w//2),y+(h//2)),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)  #绘制文字
    return square_centers,img

# 定义形状检测函数，主要用于矩形和正方形检测
def RectanDetection(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)  #寻找轮廓点
    x_pre = 0
    y_pre = 0
    Rectangle = []
    for obj in contours:
        area = cv2.contourArea(obj)  #计算轮廓内区域的面积
        perimeter = cv2.arcLength(obj,True)  #计算轮廓周长
        approx = cv2.approxPolyDP(obj,0.02*perimeter,True)  #获取轮廓角点坐标
        cv2.drawContours(img, obj, -1, (255, 0, 0), 2)  # 绘制轮廓线
        CornerNum = len(approx)   #轮廓角点的数量
        x, y, w, h = cv2.boundingRect(approx)  #获取坐标值和宽度、高度

        #轮廓对象分类
        if CornerNum == 4:
            if w >= 0.9*h and w <= 1.1*h:
                objType= "Square"
            else:objType="Rectangle"
        else:objType="N"

        if objType=="Rectangle" and 1000 < area < 40000:
            #避免重复点位，打印的是左上角的点，设计一个数据结构，存放正方形的中心点
            if abs(x - x_pre) > 50 or abs(y - y_pre) > 50:
                x_pre = x
                y_pre = y
                # print(approx)
                Rectangle.append(approx)
    return Rectangle,img

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)#0为电脑内置摄像头
    ret, origin = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
    image = cv2.resize(origin, None, fx=1, fy=1)
    image = pick_color.pick_red(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    square_centers, img = SqureDetection(edged)

    cv2.imshow('shape Detection', img)
    cv2.imshow('gray', origin)
    print(square_centers)

    # Rectangle,img = RectanDetection(edged)
    # cv2.imshow('RectanDetection', img)
    # print(Rectangle[0])

    # 将回调函数绑定到窗口
    cv2.setMouseCallback('gray', mouse_callback)

    cv2.waitKey(0)



