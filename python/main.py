import cv2 as cv
import numpy as np
import pick_color
import sort
import serial
import perspectiveTransform
import play
import rectan

all_count = 1

# 放置一个黑子
def task_1():
    capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
    ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
    sorted_xy, img = sort.Squre_sort(image)
    white_unset, black_unset, board = sort.Circle_sort(image)

    Circle = black_unset[2]
    Square = sorted_xy[1][1]

    Circle_perspective = perspectiveTransform.cvt_pos(Circle,M)
    Square_perspective = perspectiveTransform.cvt_pos(Square,M)

    Circle_x = round(Circle_perspective[0])
    Circle_y = round(Circle_perspective[1])
    Square_x = round(Square_perspective[0])
    Square_y = round(Square_perspective[1])
    print(Square_x, Square_y)
    print(Circle_x, Circle_y)
    command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)

    # 打开串口
    ser = serial.Serial('COM3', 9600, timeout=1)
    while True:
        Read = ser.readline()  # 接收一行数据
        if Read == b'OK':
            # 发送数据
            ser.write(command.encode('utf-8'))
            ser.close()
            print(all_count)
            capture.release()
            break

# 放置四个棋子
def task_2():
    count_2 = 0

    # 打开串口
    ser = serial.Serial('COM3', 9600, timeout=0.1)
    while True:
        Read = ser.readline().decode('utf-8').strip()  # 接收一行数据
        if Read != '' and count_2 < 2:
            print('Read',Read)
            count_2 += 1
            capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
            ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
            sorted_xy, img = sort.Squre_sort(image)
            white_unset, black_unset, board = sort.Circle_sort(image)
            k = int(Read)
            print(k)
            rol = k // 3
            col = k % 3
            Circle_perspective = perspectiveTransform.cvt_pos(black_unset[0], M)
            Square_perspective = perspectiveTransform.cvt_pos(sorted_xy[rol][col], M)
            print(Circle_perspective)
            print(Square_perspective)
            Circle_x = round(Circle_perspective[0])
            Circle_y = round(Circle_perspective[1])
            Square_x = round(Square_perspective[0])
            Square_y = round(Square_perspective[1])
            command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)
            ser.write(command.encode('utf-8'))
            Read = ''
            capture.release()
        if Read != '' and 2<= count_2 < 4:
            print('Read', Read)
            count_2 += 1
            capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
            ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
            sorted_xy, img = sort.Squre_sort(image)
            white_unset, black_unset, board = sort.Circle_sort(image)
            k = int(Read)
            print(k)
            rol = k // 3
            col = k % 3
            Circle_perspective = perspectiveTransform.cvt_pos(white_unset[0], M)
            Square_perspective = perspectiveTransform.cvt_pos(sorted_xy[rol][col], M)
            print(Circle_perspective)
            print(Square_perspective)
            Circle_x = round(Circle_perspective[0])
            Circle_y = round(Circle_perspective[1])
            Square_x = round(Square_perspective[0])
            Square_y = round(Square_perspective[1])
            command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)
            ser.write(command.encode('utf-8'))
            Read = ''
            capture.release()
        if count_2 == 4:
            break

# 旋转棋盘后放置四个棋子
def task_3():
    count_3 = 0

    # 打开串口
    ser = serial.Serial('COM3', 9600, timeout=0.1)
    while True:
        Read = ser.readline().decode('utf-8').strip()  # 接收一行数据
        if Read != '' and count_3 < 2:
            count_3 += 1
            capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
            ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
            image = pick_color.pick_red(image)
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
            square_centers.reverse()
            white_unset, black_unset, board = sort.Circle_sort(image)
            k = int(Read)
            print(k)
            print(square_centers)
            Circle_perspective = perspectiveTransform.cvt_pos(black_unset[0], M)
            Square_perspective = perspectiveTransform.cvt_pos(square_centers[k], M)
            Circle_x = round(Circle_perspective[0])
            Circle_y = round(Circle_perspective[1])
            Square_x = round(Square_perspective[0])
            Square_y = round(Square_perspective[1])
            command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)
            ser.write(command.encode('utf-8'))
            Read = ''
            capture.release()
        if Read != '' and 2 <= count_3 < 4:
            count_3 += 1
            capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
            ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
            image = pick_color.pick_red(image)
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
            square_centers.reverse()
            white_unset, black_unset, board = sort.Circle_sort(image)
            k = int(Read)
            print(k)
            print(square_centers)
            Circle_perspective = perspectiveTransform.cvt_pos(black_unset[0], M)
            Square_perspective = perspectiveTransform.cvt_pos(square_centers[k], M)
            Circle_x = round(Circle_perspective[0])
            Circle_y = round(Circle_perspective[1])
            Square_x = round(Square_perspective[0])
            Square_y = round(Square_perspective[1])
            command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)
            ser.write(command.encode('utf-8'))
            Read = ''
            capture.release()
        if count_3 == 4:
            break


# 人机对弈,机器执黑棋
def task_4():
    count = 0
    board_vector = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    result = None
    pre_board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    changed_piece = (0,0)
    unchanged_piece = (0,0)

    # 打开串口
    ser = serial.Serial('COM3', 9600, timeout=0.1)
    while True:
        Read = ser.readline().decode('utf-8').strip()  # 接收一行数据
        if Read != 'OK' and Read != '':
            k = int(Read)
            capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
            ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
            sorted_xy, img = sort.Squre_sort(image)
            white_unset, black_unset, board = sort.Circle_sort(image)

            rows = len(sorted_xy)
            cols = len(sorted_xy[0]) if rows > 0 else 0
            row = k // cols
            col = k % cols

            Circle = black_unset[0]
            Square = sorted_xy[row][col]
            pre_board[row][col] = 1
            # print(pre_board)
            Circle_perspective = perspectiveTransform.cvt_pos(Circle, M)
            Square_perspective = perspectiveTransform.cvt_pos(Square, M)

            Circle_x = round(Circle_perspective[0])
            Circle_y = round(Circle_perspective[1])
            Square_x = round(Square_perspective[0])
            Square_y = round(Square_perspective[1])
            command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)
            ser.write(command.encode('utf-8'))
            capture.release()

        if Read == 'OK':
            capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
            ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
            sorted_xy, img = sort.Squre_sort(image)
            white_unset, black_unset, board = sort.Circle_sort(image)

            for row in board.cells:  # 遍历每一行
                for cell in row:  # 遍历行中的每个格子
                    board_vector[cell.row][cell.column] = cell.color

            # print(pre_board)
            # print(board_vector)
            # 检查格子的不同，如果有一次不同，则正常，两次不同，说明移过棋子
            for i in range(3):  # 遍历每一行
                for j in range(3):  # 遍历行中的每个格子
                    if pre_board[i][j] != board_vector[i][j]:
                        count = count + 1

            # 正常下棋
            if count == 1:
                print(66)
                pre_board, ai_move = play.play_game(board_vector)
                print('ai决策',ai_move)
                Circle_perspective = perspectiveTransform.cvt_pos(black_unset[0], M)
                Square_perspective = perspectiveTransform.cvt_pos(sorted_xy[ai_move[0]][ai_move[1]], M)
                print(sorted_xy[ai_move[0]][ai_move[1]])
                Circle_x = round(Circle_perspective[0])
                Circle_y = round(Circle_perspective[1])
                Square_x = round(Square_perspective[0])
                Square_y = round(Square_perspective[1])
                command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)
                ser.write(command.encode('utf-8'))

            # 进行反作弊
            if count == 2:
                print(666)
                for i in range(3):  # 遍历每一行
                    for j in range(3):  # 遍历行中的每个格子
                        if pre_board[i][j] != board_vector[i][j]:
                            if board_vector[i][j] == 0:
                                unchanged_piece = sorted_xy[i][j]
                                # print(i,j)
                            elif board_vector[i][j] != 0:
                                changed_piece = sorted_xy[i][j]
                                # print(i,j)
                changed_piece = perspectiveTransform.cvt_pos(changed_piece, M)
                unchanged_piece = perspectiveTransform.cvt_pos(unchanged_piece, M)
                Circle_x = round(changed_piece[0])
                Circle_y = round(changed_piece[1])
                Square_x = round(unchanged_piece[0])
                Square_y = round(unchanged_piece[1])
                # print(Square_x, Square_y)
                command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)
                ser.write(command.encode('utf-8'))
            count = 0
            result = play.check_winner(pre_board)
            capture.release()
        if result is not None:
            break

# 人机对弈，机器后手白棋
def task_5():
    count = 0
    board_vector = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    pre_board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    changed_piece = (0,0)
    unchanged_piece = (0,0)

    # 打开串口
    ser = serial.Serial('COM3', 9600, timeout=0.1)
    while True:
        Read = ser.readline().decode('utf-8').strip()  # 接收一行数据
        if Read == 'OK':
            capture = cv.VideoCapture(0)  # 0为电脑内置摄像头
            ret, image = capture.read()  # 摄像头读取,ret为是否成功打开摄像头,true,false。frame为视频的每一帧图像
            sorted_xy, img = sort.Squre_sort(image)
            white_unset, black_unset, board = sort.Circle_sort(image)

            for row in board.cells:  # 遍历每一行
                for cell in row:  # 遍历行中的每个格子
                    board_vector[cell.row][cell.column] = -cell.color

            # 检查格子的不同，如果有一次不同，则正常，两次不同，说明移过棋子
            for i in range(3):  # 遍历每一行
                for j in range(3):  # 遍历行中的每个格子
                    if pre_board[i][j] != board_vector[i][j]:
                        count = count + 1

            # 正常下棋
            if count == 1:
                print(66)
                pre_board, ai_move = play.play_game(board_vector)
                print(ai_move)
                Circle_perspective = perspectiveTransform.cvt_pos(white_unset[0], M)
                Square_perspective = perspectiveTransform.cvt_pos(sorted_xy[ai_move[0]][ai_move[1]], M)
                Circle_x = round(Circle_perspective[0])
                Circle_y = round(Circle_perspective[1])
                Square_x = round(Square_perspective[0])
                Square_y = round(Square_perspective[1])
                command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)
                ser.write(command.encode('utf-8'))

            # 进行反作弊
            if count == 2:
                print(666)
                for i in range(3):  # 遍历每一行
                    for j in range(3):  # 遍历行中的每个格子
                        if pre_board[i][j] != board_vector[i][j]:
                            if board_vector[i][j] == 0:
                                unchanged_piece = sorted_xy[i][j]
                                print(i,j)
                            elif board_vector[i][j] != 0:
                                changed_piece = sorted_xy[i][j]
                                print(i,j)
                changed_piece = perspectiveTransform.cvt_pos(changed_piece, M)
                unchanged_piece = perspectiveTransform.cvt_pos(unchanged_piece, M)
                Circle_x = round(changed_piece[0])
                Circle_y = round(changed_piece[1])
                Square_x = round(unchanged_piece[0])
                Square_y = round(unchanged_piece[1])
                command = "@X%d,Y%d,XX%d,YY%d\r\n" % (Circle_x, Circle_y, Square_x, Square_y)
                ser.write(command.encode('utf-8'))
                capture.release()
            count = 0
            result = play.check_winner(board_vector)
            if result is not None:
                break

pts1 = np.float32([[150, 112], [446, 112], [150, 410], [445, 410]])
pts2 = np.float32([[174, 16], [78, 16], [174, 112], [78, 112]])
M = cv.getPerspectiveTransform(pts1, pts2)
M_inv = np.linalg.inv(M)

while True:
    if all_count == 1:
        task_1()
        all_count = 2
    elif all_count == 2:
        task_2()
        all_count = 3
    elif all_count == 3:
        task_3()
        all_count = 4
    elif all_count == 4:
        task_4()
        all_count = 5
    elif all_count == 5:
        task_5()
        break
