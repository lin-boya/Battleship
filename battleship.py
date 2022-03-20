import random


def check_diag(p1=[0, 0], p2=[0, 0]):
    # that means not diag
    if p1[0] == p2[0] or p1[1] == p2[1]:
        return False
    return True


def check_cross(p11=[0, 0], p12=[0, 0], p21=[0, 0], p22=[0, 0]):
    px11 = p11[0]
    py11 = p11[1]

    px12 = p12[0]
    py12 = p12[1]

    px21 = p21[0]
    py21 = p21[1]

    px22 = p22[0]
    py22 = p22[1]

    if px12 >= px21 >= px11 and py22 >= py11 >= py21:
        print("There is already a ship at location %d, %d. Terminating game." % (px21, py11))
        return True

    if px22 >= px11 >= px21 and py12 >= py21 >= py11:
        print("There is already a ship at location %d, %d. Terminating game." % (px11, py21))
        return True

    return False


def check_out_board(p1=[0, 0], p2=[0, 0], height=0, width=0):
    px = p1[0]
    py = p1[1]

    px1 = p2[0]
    py1 = p2[1]

    if max([px, px1]) >= height or max([py, py1]) >= width or min([px, px1]) < 0 or min([py, py1]) < 0:
        return True
    return False


def get_placements(filename, height, width):
    file = open(filename, "r")
    placements = {}
    ships = []

    for line in file:
        ls = line.split()
        if ls[0] in placements.keys() or ls[0] in ['x', 'X', 'o', 'O', '*']:
            print("Error symbol %s is already in use. Terminating game" % ls[0])
            exit(0)
        else:
            ships.append(ls[0])
            placements[ls[0]] = []
            p1 = [int(ls[1]), int(ls[2])]
            p2 = [int(ls[3]), int(ls[4])]

            if check_out_board(p1, p2, height, width):
                print("Error %s is placed outside of the board. Terminating game." % ls[0])
                exit(0)

            if check_diag(p1, p2):
                print("Ships cannot be placed diagonally. Terminating game.")
                exit(0)

            for k, v in placements.items():
                if placements[k] == []:
                    continue
                if check_cross(p1, p2, v[0], v[1]):
                    exit(0)

            if p1[0] == p2[0]:
                if p1[1] > p2[1]:
                    placements[ls[0]].append(p2)
                    placements[ls[0]].append(p1)
                    continue
            if p1[1] == p2[1]:
                if p1[0] > p1[0]:
                    placements[ls[0]].append(p2)
                    placements[ls[0]].append(p1)
                    continue
            placements[ls[0]].append(p1)
            placements[ls[0]].append(p2)

    return placements


def get_directioin_between_2_points(p1=[0, 0], p2=[0, 0]):
    px = p1[0]
    py = p1[1]

    px1 = p2[0]
    py1 = p2[1]

    if px == px1:
        return 'horz'

    if py == py1:
        return 'vert'


def get_len_between_2_points(p1=[0, 0], p2=[0, 0]):
    px = p1[0]
    py = p1[1]

    px1 = p2[0]
    py1 = p2[1]

    leng = max([abs(py-py1), abs(px-px1)]) + 1

    return leng


def print_all_board(ai_board=[[]], player_board=[[]]):
    height = len(ai_board)
    width = len(ai_board[0])

    print("Scanning Board")

    temp_index = [' ']
    temp_index.extend([str(i) for i in range(width)])
    print(' '.join(temp_index))

    for i in range(height):
        temp = [str(i)]
        for j in range(width):
            if ai_board[i][j] not in ['o', 'O', 'X', 'x']:
                temp.append('*')
            else:
                temp.append(ai_board[i][j])
        print(' '.join(temp))

    print("\nMy Board")
    print(' '.join(temp_index))
    for i in range(height):
        temp = [str(i)]
        for j in range(width):
            temp.append(player_board[i][j])
        print(' '.join(temp))
    print()


def construct_user_board(placements, height, width):
    board = [['*' for i in range(width)] for j in range(height)]
    for k, v in placements.items():
        leng = get_len_between_2_points(v[0], v[1])
        direction = get_directioin_between_2_points(v[0], v[1])
        p1 = v[0]
        p2 = v[1]

        if direction == 'vert':
            for i in range(leng):
                board[p1[0]+i][p1[1]] = k
        if direction == 'horz':
            for i in range(leng):
                board[p1[0]][p1[1]+i] = k
    return board


def place_ship(symbol, leng, direction, board=[[]]):
    height = len(board)
    width = len(board[0])

    if direction == 'horz':

        start_x = random.randint(0, height - 1)
        start_y = random.randint(0, width - leng)

        for i in range(leng):
            if board[start_x][start_y + i] != '*':
                return False
        for i in range(leng):
            board[start_x][start_y + i] = symbol
        print("Placing ship from %d,%d to %d,%d." % (start_x, start_y, start_x, start_y + leng - 1))
        return True

    if direction == 'vert':
        start_x = random.randint(0, height-leng)
        start_y = random.randint(0, width - 1)

        for i in range(leng):
            if board[start_x + i][start_y] != '*':
                return False
        for i in range(leng):
            board[start_x + i][start_y] = symbol
        print("Placing ship from %d,%d to %d,%d." % (start_x, start_y, start_x + leng - 1, start_y))
        return True


def construct_ai_board(placements, height, width):
    board = [['*' for i in range(width)] for j in range(height)]

    lens = []
    ships = sorted(placements.keys())
    for i in ships:
        lens.append(get_len_between_2_points(placements[i][0], placements[i][1]))

    for i in range(len(ships)):
        while True:
            direction = random.choice(['vert', 'horz'])
            flg = place_ship(ships[i], lens[i], direction, board)
            if flg == False:
                continue
            else:
                break
    return board


def valid_pos(board=[[]], x=0, y=0):

    if x >= len(board) or y >= len(board[0]):
        return False

    if board[x][y] in ['x', 'X', 'o', 'O']:
        return False

    return True


class User(object):
    def __init__(self, board):
        self.height = len(board)
        self.width = len(board[0])

        self.board = board

    def player_select(self, board=[[]]):
        while True:
            pos = input("Enter row and column to fire on separated by a space: ")
            ps = pos.strip().split()
            if len(ps) > 2 or len(ps) == 1:
                continue

            if not ps[0].isdigit() or not ps[1].isdigit():
                continue

            x, y = int(ps[0]), int(ps[1])

            if not valid_pos(board, x, y):
                continue

            return x, y

    def fire(self, pos, board):

        if board[pos[0]][pos[1]] == '*':
            board[pos[0]][pos[1]] = 'O'
            print("Miss!")
        else:
            p = board[pos[0]][pos[1]]
            board[pos[0]][pos[1]] = 'X'

            flg = 0
            for i in range(self.height):
                for j in range(self.width):
                    if board[i][j] == p:
                        flg = 1

            if flg == 1:
                print("Hit!")
            else:
                print("You sunk my "+p)


class RandomAI(object):
    def __init__(self, board):
        self.board = board
        self.locations=[]
        self.model = ''
        self.pos = []

        self.height = len(board)
        self.width = len(board[0])

        for i in range(self.height):
            for j in range(self.width):
                self.locations.append((i, j))

    def select_pos(self, board):
        while True:
            pos = random.choice(self.locations)
            x, y = pos[0], pos[1]

            self.locations.remove(pos)

            if not valid_pos(board, x, y):
                continue

            print("The AI fires at location (%d, %d)" %(x, y))

            return x, y

    def fire(self, pos, board):

        p = board[pos[0]][pos[1]]

        if p == '*':
            board[pos[0]][pos[1]] = 'O'
            print("Miss!")
        else:
            board[pos[0]][pos[1]] = 'X'

            flg = 0
            for i in range(self.height):
                for j in range(self.width):
                    if board[i][j] == p:
                        flg = 1

            if flg == 1:
                print("Hit!")
            else:
                print("You sunk my " + p)


class SmartAI(object):
    def __init__(self, board):
        self.mode = 'Hunt'
        self.pos = []
        self.board = board
        self.destory_pos =[]

        self.locations=[]
        self.height = len(board)
        self.width = len(board[0])

        for i in range(self.height):
            for j in range(self.width):
                self.locations.append((i, j))

    def select_pos(self, board):
        while True:

            if self.mode == 'Hunt':
                while True:
                    pos = random.choice(self.locations)
                    self.locations.remove(pos)

                    if pos in self.destory_pos:
                        self.destory_pos.remove(pos)
                        exit(0)

                    if not valid_pos(board, pos[0], pos[1]):
                        continue

                    print("The AI fires at location (%d, %d)" % (pos[0], pos[1]))
                    self.pos = pos

                    return pos
            else:
                while True:
                    if len(self.destory_pos) != 0:
                        pos = self.destory_pos[0]

                        self.destory_pos.remove(pos)

                        if pos in self.locations:
                            self.locations.remove(pos)

                        if not valid_pos(board, pos[0], pos[1]):
                            continue
                        print("The AI fires at location (%d, %d)" % (pos[0], pos[1]))
                        self.pos = pos
                        return pos
                    else:
                        self.mode = 'Hunt'
                        break

    def fire(self, pos, board):
        if board[pos[0]][pos[1]] == '*':
            board[pos[0]][pos[1]] = 'O'
            print("Miss!")
        else:
            p = board[pos[0]][pos[1]]
            board[pos[0]][pos[1]] = 'X'

            flg = 0
            for i in range(self.height):
                for j in range(self.width):
                    if board[i][j] == p:
                        flg = 1
            self.pos = pos
            # up
            if pos[0]-1 >= 0 and (pos[0]-1, pos[1]) in self.locations:
                self.destory_pos.append((pos[0]-1, pos[1]))
            # down
            if pos[0]+1 < self.height and (pos[0]+1, pos[1]) in self.locations:
                self.destory_pos.append((pos[0]+1, pos[1]))
            # left
            if pos[1]-1 >= 0 and (pos[0], pos[1]-1) in self.locations:
                self.destory_pos.append((pos[0], pos[1]-1))
            # right
            if pos[1] + 1 < self.width and (pos[0], pos[1] + 1) in self.locations:
                self.destory_pos.append((pos[0], pos[1] + 1))

            self.mode = 'Destory'

            if flg == 1:
                print("Hit!")
            else:
                print("You sunk my " + p)


class CheatingAI(object):
    def __init__(self, board):
        self.height = len(board)
        self.width = len(board[0])
        self.board = board

    def select_pos(self, board):
        for i in range(self.height):
            for j in range(self.width):
                if board[i][j] not in ['*', 'o', 'O', 'x', 'X']:
                    print("The AI fires at location (%d, %d)" % (i, j))
                    return i, j
        return -1, -1

    def fire(self, pos, board):

        if board[pos[0]][pos[1]] == '*':
            board[pos[0]][pos[1]] = 'O'
            print("Miss!")
        else:
            p = board[pos[0]][pos[1]]
            board[pos[0]][pos[1]] = 'X'

            flg = 0
            for i in range(self.height):
                for j in range(self.width):
                    if board[i][j] == p:
                        flg = 1
            if flg == 1:
                print("Hit!")
            else:
                print("You sunk my " + p)


def generate_AI(ai_type, board):
    if ai_type == '1':
        return RandomAI(board)
    elif ai_type == '2':
        return SmartAI(board)
    elif ai_type == '3':
        return CheatingAI(board)


def check_win(board):
    height = len(board)
    width = len(board[0])
    flg = 0
    for i in range(height):
        for j in range(width):
           if board[i][j] not in ['*', 'o', 'O', 'x', 'X']:
               flg = 1
    if flg == 0:
        return True
    else:
        return False


def setup():

    while True:
        seed = input("Enter the seed: ").strip()
        try:
            seed = int(seed)
            break
        except Exception as e:
            continue
    while True:
        width = input("Enter the width of the board: ").strip()
        try:
            width = int(width)
            if width > 0:
                break
            else:
                continue
        except Exception as e:
            continue

    while True:
        height = input("Enter the height of the board: ").strip()
        try:
            height = int(height)
            if height > 0:
                break
            else:
                continue
        except Exception as e:
            continue

    file = input("Enter the name of the file containing your ship placements: ").strip()
    while True:
        print("Choose your AI.")
        print("1. Random")
        print("2. Smart")
        print("3. Cheater")
        ai_id = input(" Your choice: ").strip()
        if ai_id in ['1', '2', '3']:
            break

    placements = get_placements(file, height, width)

    random.seed(seed)

    user_board = construct_user_board(placements, height, width)

    ai_board = construct_ai_board(placements, height, width)

    first = random.randint(0, 1)

    user = User(user_board)

    AI = generate_AI(ai_id, ai_board)

    # 0 for user
    # 1 for ai
    player = 'user' if first == 0 else 'ai'

    count =0
    while True:
        # for user

        if player == 'user':
            if count % 2 == 0:
                print_all_board(AI.board, user_board)
            pos = user.player_select(AI.board)
            user.fire(pos, AI.board)
            if check_win(AI.board):
                print_all_board(AI.board, user_board)
                print("You win!")
                return
        else:
            pos = AI.select_pos(user_board)
            AI.fire(pos, user_board)

            if check_win(user_board):
                print_all_board(AI.board, user_board)
                print("The AI wins.")
                return
            if count % 2 == 0:
                print_all_board(AI.board, user_board)

        player = 'ai' if player == 'user' else 'user'
        count += 1


if __name__ == "__main__":
    setup()

