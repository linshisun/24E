# 先定义 Cell 类
class Cell:
    def __init__(self, row, column, color=0):
        self.row = row
        self.column = column
        self.is_occupied = 0
        self.color = color  # 颜色属性
        self.piece = None

# 再定义 Board 类
class Board:
    def __init__(self):
        self.size = 3
        # 创建 3x3 的棋盘格子，显式传递 color 参数
        self.cells = [[Cell(r, c, 0) for c in range(self.size)] for r in range(self.size)]


def check_winner(board):
    # 检查行/列
    for i in range(3):
        if abs(sum(board[i])) == 3:  # 行判断
            return board[i][0]
        if abs(board[0][i] + board[1][i] + board[2][i]) == 3:  # 列判断
            return board[0][i]

    # 检查对角线
    if abs(board[0][0] + board[1][1] + board[2][2]) == 3:
        return board[0][0]
    if abs(board[0][2] + board[1][1] + board[2][0]) == 3:
        return board[0][2]

    # 平局判断
    if all(cell != 0 for row in board for cell in row):
        return 0
    return None  # 游戏继续

def minimax(board, depth, is_maximizing, alpha, beta):
    result = check_winner(board)

    # 终局条件
    if result is not None:
        return result * (1 + depth / 10)  # 深度加权评分

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1  # AI落子
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = 0
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = -1  # 玩家落子
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = 0
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

def find_best_move(board):
    best_val = -float('inf')
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 1  # 模拟AI落子
                move_val = minimax(board, 0, False, -float('inf'), float('inf'))
                board[i][j] = 0  # 回溯

                # 优先选择立即胜利的走法
                if move_val == 1:
                    return (i, j)
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    # 防守策略：优先阻止玩家胜利
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = -1  # 模拟玩家落子
                if check_winner(board) == -1:
                    board[i][j] = 0
                    return (i, j)
                board[i][j] = 0

    return best_move  # 默认返回最佳评估位置

# ai执子为1
def play_game(initial_board):
    board = [row[:] for row in initial_board]  # 深拷贝棋盘
    # print("AI正在思考...")
    ai_move = find_best_move(board)
    board[ai_move[0]][ai_move[1]] = 1

    # # 输出当前棋盘
    # print(f"AI落子位置: {ai_move}")
    # for row in board:
    #     print("|".join(map(str, row)))
    #
    # # 检查游戏结果
    # result = check_winner(board)
    # if result is not None:
    #     if result == 1:
    #         print("AI获胜！")
    #     elif result == -1:
    #         print("玩家获胜！")
    #     else:
    #         print("平局！")

    return board, ai_move


if __name__ == "__main__":
    initial_board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    board, ai_move = play_game(initial_board)
    print(board)
    print(ai_move)