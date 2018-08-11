import sys
from random import randint

board = [['g', ' ', 'g', ' ', 'B', ' ', 'g', ' ', 'g', ' '],
         [' ', '$', ' ', '$', ' ', '$', ' ', '$', ' ', '$'],
         ['$', ' ', '$', ' ', '$', ' ', '$', ' ', '$', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', 'S', ' ', 'S', ' ', 'S', ' ', 'S', ' ', 'S'],
         ['S', ' ', 'S', ' ', 'S', ' ', 'S', ' ', 'S', ' '],
         [' ', 'G', ' ', 'G', ' ', 'W', ' ', 'G', ' ', 'G']]
turn = 'White'
winner = False
existing_move = True
existing_capture = False
chain_capture = False
capturer = 0
black_pieces = []
white_pieces = []
rand_bot = False

class King:
    def __init__(self, name, x = 0, y = 0, c = ''):
        self.color = c
        self.position = (x, y)
        self.name = name

    def __str__(self):
        if self.color is 'Black':
            return 'B'
        elif self.color is 'White':
            return 'W'

    def possible_moves(self):
        x = self.position[0]
        y = self.position[1]
        moves = [(x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1)]
        kmoves = []
        capture = []
        for arr in moves:
            if isinstance(board[x][y], King) and check_move(arr[0], arr[1]):
                kmoves.append(arr)
            direction = (arr[0] - x, arr[1] - y)
            if isinstance(board[x][y], King):
                if check_move(arr[0] + direction[0], arr[1] + direction[1]):
                    if board[arr[0]][arr[1]] != ' ':
                        if board[x][y].color == 'White' and board[arr[0]][arr[1]].color == 'Black':
                            kmoves.append((arr[0] + direction[0], arr[1] + direction[1]))
                            capture.append((arr[0] + direction[0], arr[1] + direction[1]))
                        elif board[x][y].color == 'Black' and board[arr[0]][arr[1]].color == 'White':
                            kmoves.append((arr[0] + direction[0], arr[1] + direction[1]))
                            capture.append((arr[0] + direction[0], arr[1] + direction[1]))
                elif 0 <= arr[0] <= (len(board[0])-1) and 0 <= arr[1] <= (len(board)-1):
                    if board[arr[0]][arr[1]] != ' ':
                        if board[x][y].color == 'White' and board[arr[0]][arr[1]].color == 'Black':
                            if (x == 2 and y == 2):
                                kmoves.append((2,2))
                                capture.append((2,2))
                            if (x == 2 and y == 6):
                                kmoves.append((2,6))
                                capture.append((2,6))
                        elif board[x][y].color == 'Black' and board[arr[0]][arr[1]].color == 'White':
                            if (x == 7 and y == 3):
                                kmoves.append((7,3))
                                capture.append((7,3))
                            if (x == 7 and y == 7):
                                kmoves.append((7,7))
                                capture.append((7,7))
        if board[x][y].color == 'White':
            if (x == 3 and y == 3) or (x == 3 and y == 5):
                kmoves.append((4,4))
        if board[x][y].color == 'Black':
            if (x == 6 and y == 4) or (x == 6 and y == 6):
                kmoves.append((5,5))
        if existing_capture:
            return (capture, capture)
        else:
            return (kmoves, capture)

class Guard:
    def __init__(self, name, x = 0, y = 0, c = ''):
        self.color = c
        self.position = (x, y)
        self.name = name
    """
    def __str__(self):
        if self.color is 'Black':
            return 'g'
        elif self.color is 'White':
            return 'G'
    """

    def possible_moves(self):
        x = self.position[0]
        y = self.position[1]
        one_moves = [(x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1)]
        two_moves = [(x+2, y+2), (x-2, y+2), (x+2, y-2), (x-2, y-2)]
        gmoves = []
        capture = []
        for i in range(len(one_moves)):
            one_x = one_moves[i][0]
            one_y = one_moves[i][1]
            two_x = two_moves[i][0]
            two_y = two_moves[i][1]
            if isinstance(board[x][y], Guard) and check_move(one_x, one_y):
                gmoves.append(one_moves[i])
                if check_move(two_x, two_y):
                    gmoves.append(two_moves[i])
            direction = (one_x - x, one_y - y)
            if isinstance(board[x][y], Guard) and check_move(one_x + direction[0], one_y + direction[1]):
                if board[one_x][one_y] != ' ':
                    if board[x][y].color == 'White' and board[one_x][one_y].color == 'Black':
                        gmoves.append((one_x + direction[0], one_y + direction[1]))
                        capture.append((one_x + direction[0], one_y + direction[1]))
                    elif board[x][y].color == 'Black' and board[one_x][one_y].color == 'White':
                        gmoves.append((one_x + direction[0], one_y + direction[1]))
                        capture.append((one_x + direction[0], one_y + direction[1]))
        if existing_capture:
            return (capture, capture)
        else:
            return (gmoves, capture)

class Serf:
    def __init__(self, name, x = 0, y = 0, c = ''):
        self.color = c
        self.position = (x, y)
        self.name = name

    """
    def __str__(self):
        if self.color is 'Black':
            return '$'
        elif self.color is 'White':
            return 'S'
    """

    def possible_moves(self):
        x = self.position[0]
        y = self.position[1]
        bmoves = [(x+1, y-1), (x+1, y+1)]
        wmoves = [(x-1, y-1), (x-1, y+1)]
        smoves = []
        capture = []
        if self.color is 'Black':
            for arr in bmoves:
                if isinstance(board[x][y], Serf) and check_move(arr[0], arr[1]):
                    smoves.append(arr)
                direction = (arr[0] - x, arr[1] - y)
                if isinstance(board[x][y], Serf) and check_move(arr[0] + direction[0], arr[1] + direction[1]):
                    if board[arr[0]][arr[1]] != ' ':
                        if board[arr[0]][arr[1]].color == 'White':
                            smoves.append((arr[0] + direction[0], arr[1] + direction[1]))
                            capture.append((arr[0] + direction[0], arr[1] + direction[1]))
            if x == 9:
                if board[2][0] == ' ':
                    smoves.append((2,0))
                if board[2][2] == ' ':
                    smoves.append((2,2))
                if board[2][4] == ' ':
                    smoves.append((2,4))
                if board[2][6] == ' ':
                    smoves.append((2,6))
                if board[2][8] == ' ':
                    smoves.append((2,8))
        elif self.color is 'White':
            for arr in wmoves:
                if isinstance(board[x][y], Serf) and check_move(arr[0], arr[1]):
                    smoves.append(arr)
                direction = (arr[0] -x, arr[1] - y)
                if isinstance(board[x][y], Serf) and check_move(arr[0] + direction[0], arr[1] + direction[1]):
                    if board[arr[0]][arr[1]] != ' ':
                        if board[arr[0]][arr[1]].color == 'Black':
                            smoves.append((arr[0] + direction[0], arr[1] + direction[1]))
                            capture.append((arr[0] + direction[0], arr[1] + direction[1]))
            if x == 0:
                if board[7][1] == ' ':
                    smoves.append((7,1))
                if board[7][3] == ' ':
                    smoves.append((7,3))
                if board[7][5] == ' ':
                    smoves.append((7,5))
                if board[7][7] == ' ':
                    smoves.append((7,7))
                if board[7][9] == ' ':
                    smoves.append((7,9))
        if existing_capture:
            return (capture, capture)
        else:
            return (smoves, capture)

def check_move(x, y):
    if (x == 5 and y == 5) or (x == 4 and y == 4):
        return False
    else:
        return 0 <= x <= (len(board[0])-1) and 0 <= y <= (len(board)-1) and board[x][y] is ' '

def check_valid_piece(x, y):
    if board[x][y] == ' ':
        print("There is no piece in that location")
        return False
    elif board[x][y].color != turn:
        print("You can't move the opponent's piece!")
        return False
    elif len(board[x][y].possible_moves()[0]) == 0:
        if existing_capture:
            print("Captures are mandatory")
        else:
            print("That piece has no valid moves this turn")
        return False
    return True

def select_move(list):
    print(list)
    num_moves = len(list)
    while True:
        print("Input your move as a # between 1 and {0}" .format(num_moves))
        try:
            input_move = int(input())
        except ValueError:
            print("Please input an integer")
            continue
        if 1 > input_move or input_move > num_moves:
            print("Please input an integer from 1 to {0}".format(num_moves))
            continue
        break
    return list[input_move-1]

def internal_move(x, y, selection):
    global turn
    global existing_capture
    global chain_capture
    global capturer
    global rand_bot
    if existing_capture:
        board[(x + (selection[0]))//2][(y + (selection[1]))//2] = ' '
        board[selection[0]][selection[1]] = board[x][y]
        board[x][y] = ' '
        board[selection[0]][selection[1]].position = selection
        if capturer == '':
            capturer = board[selection[0]][selection[1]]
        if len(board[selection[0]][selection[1]].possible_moves()[1]) > 0:
            chain_capture = True
        else:
            chain_capture = False
            capturer = ''
    else:
        capturer = ''
        board[selection[0]][selection[1]] = board[x][y]
        board[x][y] = ' '
        board[selection[0]][selection[1]].position = selection
    if not chain_capture:
        if turn == 'White':
            turn = 'Black'
            rand_bot = True
        else:
            turn = 'White'
            rand_bot = False
    existing_move, existing_capture = loop_board()

def check_winner():
    global existing_move
    if isinstance(board[4][4], King) or isinstance(board[5][5], King) or not existing_move:
        if turn == 'White':
            print('Black wins!')
        else:
            print('White wins!')
        return True
    else:
        return False

def loop_board():
    global existing_capture
    global existing_move
    existing_move = False
    existing_capture = False
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] != ' ':
                if board[r][c].color == turn:
                    if len(board[r][c].possible_moves()[0]) > 0:
                        existing_move = True
                        if len(board[r][c].possible_moves()[1]) > 0:
                            existing_capture = True
    return (existing_move, existing_capture)

def print_board():
    print('\n A | B | C | D | E | F | G | H | I | J ')
    print('---------------------------------------')
    for x in range(len(board)-1):
        sys.stdout.write(' ')
        for y in range(len(board[0])-1):
            sys.stdout.write(str(board[x][y]) + ' | ')
        print(str(board[x][9])  + ' | {0} ' .format(10 - x) + '\n-------------------------------------------')
    sys.stdout.write(' ')
    for y in range(len(board[0])-1):
        sys.stdout.write(str(board[9][y]) + ' | ')
    print(str(board[9][9]) + ' | 1  ' + '\n')

def initialize_pieces(board, gui, piece_imgs):
    serf_count = 0
    guard_count = 0
    for x in range(3):
        for y in range(len(board[0])):
            if board[x][y] is '$':
                name = "bs" + str(serf_count)
                board[x][y] = Serf(name, x, y, 'Black')
                gui.add_piece(name, piece_imgs['bs'], x, y)
                serf_count += 1
            elif board[x][y] is 'g':
                name = "bg" + str(guard_count)
                board[x][y] = Guard(name, x, y, 'Black')
                gui.add_piece(name, piece_imgs['bg'], x, y)
                guard_count += 1
            elif board[x][y] is 'B':
                board[x][y] = King('bk', x, y, 'Black')
                gui.add_piece('bk', piece_imgs['bk'], x, y)
    serf_count = 0
    guard_count = 0
    for x in range(7,10):
        for y in range(len(board[0])):
            if board[x][y] is 'S':
                name = "ws" + str(serf_count)
                board[x][y] = Serf(name, x, y, 'White')
                gui.add_piece(name, piece_imgs['ws'], x, y)
                serf_count += 1
            elif board[x][y] is 'G':
                name = "wg" + str(guard_count)
                board[x][y] = Guard(name, x, y, 'White')
                gui.add_piece(name, piece_imgs['wg'], x, y)
                guard_count += 1
            elif board[x][y] is 'W':
                board[x][y] = King('wk', x, y, 'White')
                gui.add_piece('wk', piece_imgs['wk'], x, y)

def random_bot(board):
    pieces = []
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] != ' ':
                if board[r][c].color == turn:
                    if len(board[r][c].possible_moves()[0]) > 0:
                        pieces.append((r, c))
    piece = randint(0, len(pieces)-1)
    x = pieces[piece][0]
    y = pieces[piece][1]
    move_list = board[x][y].possible_moves()[0]
    random_selection = randint(0, len(move_list)-1)
    random_move = move_list[random_selection]
    return ((x, y), random_move)

def minimax(board, depth, maximizing_player):
    if depth == 0: #or nodes == 1:
        return best
    elif maximizing_player:
        best = -9999
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] != ' ':
                    if board[r][c].color == turn:
                        for move in board[r][c].possible_moves()[0]:
                            copy_board = board[:]
                            internal_move(r, c, move)
                            best = max(best, minimax(board, depth-1, False))
                            board = copy_board
        return best
    else: #minimizing_player
        best = 9999
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] != ' ':
                    if board[r][c].color == turn:
                        for move in board[r][c].possible_moves()[0]:
                            copy_board = board[:]
                            internal_move(r, c, move)
                            best = min(best, minimax(board, depth-1, False))
                            board = copy_board
        return best

#assigns heuristic values to specific moves; how to incorporate this in minimax?
def evaluate(board):
    if board[4][4] != ' ':
        if board[4][4].color == 'White':
            return 9999
    if board[5][5] != ' ':
        if board[5][5].color == 'Black':
            return -9999
    for r in range(len(board)):
        for c in range(len(board[0])):
            if isinstance(board[r][c], Serf):
                if board[r][c].color == 'White':
                    return len(board[r][c].possible_move()[0])
                else:
                    return -1*len(board[r][c].possible_move()[0])
            if isinstance(board[r][c], Guard):
                if board[r][c].color == 'White':
                    return 5*len(board[r][c].possible_move()[0])
                else:
                    return -5*len(board[r][c].possible_move()[0])
            if isinstance(board[r][c], King):
                if board[r][c].color == 'White':
                    return 40*len(board[r][c].possible_move()[0])
                else:
                    return -40*len(board[r][c].possible_move()[0])

    # TO INCLUDE LATER:
    # proximity to courtyard?

def find_best_move(board):
    if turn == 'White':
        best = -9999
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] != ' ':
                    if board[r][c].color == turn:
                        for move in board[r][c].possible_moves()[0]:
                            copy_board = board[:]
                            internal_move(r, c, move)
                            value = minimax(board, 0, True)
                            board = copy_board
                            if value > best_move:
                                best_move = move

    else:
        best = 9999
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] != ' ':
                    if board[r][c].color == turn:
                        for move in board[r][c].possible_moves()[0]:
                            copy_board = board[:]
                            internal_move(r, c, move)
                            value = minimax(board, 0, False)
                            board = copy_board
                            if value < best_move:
                                best_move = move

import tkinter as tk

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=10, columns=10, size=32, color1="gray30", color2="white"):
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.canvas.bind("<Configure>", self.refresh)
        self.selected_piece = False
        self.canvas.bind("<Button 1>", self.make_move)

    def add_piece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        print(name)
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, row, column)

    def place_piece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def make_move(self, event):
        if rand_bot:
            bot = random_bot(board)
            x = bot[0][0]
            y = bot[0][1]
            selection = bot[1]
            r = selection[0]
            c = selection[1]
            self.orig_name = board[x][y].name
            self.orig_coord = (x,y)
            if existing_capture:
                print(10000, (r + self.orig_coord[0])//2, (c + self.orig_coord[1])//2)
                self.canvas.delete("{}".format(board[(r + self.orig_coord[0])//2][(c + self.orig_coord[1])//2].name))
                internal_move(x, y, selection)
                self.place_piece(self.orig_name, r, c)
            else:
                internal_move(x, y, selection)
                self.place_piece(self.orig_name, r, c)
        else:
            c, r = event.x//self.size, event.y//self.size
            if not self.selected_piece:
                if not check_valid_piece(r,c):
                    return
                if capturer:
                    self.poss_moves, self.capture = capturer.possible_moves()
                else:
                    self.poss_moves, self.capture = board[r][c].possible_moves()
                self.orig_name = board[r][c].name
                self.orig_coord = (r,c)
                self.dots = []
                offset = 0.3 * self.size
                for y,x in self.poss_moves:
                    x0 = x * self.size + offset
                    y0 = y * self.size + offset
                    x1 = x0 + self.size - 2*offset
                    y1 = y0 + self.size - 2*offset
                    if turn == 'White':
                        self.dots.append(self.canvas.create_oval(x0,y0,x1,y1,fill='orange',outline=''))
                    else:
                        self.dots.append(self.canvas.create_oval(x0,y0,x1,y1,fill='red',outline=''))
                self.selected_piece = True
            else:
                print(r,c)
                print(self.poss_moves)
                if (r,c) in self.poss_moves:
                    print("entered")
                    for dot in self.dots:
                        self.canvas.delete(dot)
                    self.place_piece(self.orig_name, r, c)
                    self.selected_piece = False
                    if (r,c) in self.capture:
                        self.canvas.delete("{}".format(board[(r + self.orig_coord[0])//2][(c + self.orig_coord[1])//2].name))
                    internal_move(self.orig_coord[0], self.orig_coord[1], (r,c))
                else:
                    for dot in self.dots:
                        self.canvas.delete(dot)
                    self.selected_piece = False
                    return
                if chain_capture:
                    self.make_move
            if check_winner():
                root.quit()

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        self.canvas.create_rectangle(5*self.size, 5*self.size, 5*self.size+self.size, 5*self.size+self.size, outline="black", fill="dark green", tags="square")
        self.canvas.create_rectangle(4*self.size, 4*self.size, 4*self.size+self.size, 4*self.size+self.size, outline="black", fill="dark green", tags="square")
        self.canvas.create_rectangle(5*self.size, 4*self.size, 5*self.size+self.size, 4*self.size+self.size, outline="green2", fill="white", tags="square")
        self.canvas.create_rectangle(4*self.size, 5*self.size, 4*self.size+self.size, 5*self.size+self.size, outline="green2", fill="white", tags="square")
        for name in self.pieces:
            self.place_piece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

if __name__ == "__main__":
    root = tk.Tk()
    #root.state('zoomed')
    gui = GameBoard(root)
    piece_imgs = {
        'ws' : tk.PhotoImage(file="wp.png"),
        'wg' : tk.PhotoImage(file="wn.png"),
        'wk' : tk.PhotoImage(file="wk.png"),
        'bs' : tk.PhotoImage(file="bp.png"),
        'bg' : tk.PhotoImage(file="bn.png"),
        'bk' : tk.PhotoImage(file="bk.png")
    }

    gui.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    initialize_pieces(board, gui, piece_imgs)
    root.mainloop()
