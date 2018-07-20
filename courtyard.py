
import sys

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
black_pieces = []
white_pieces = []

class King:
    def __init__(self, x, y, c):
        self.color = c
        self.position = [x, y]
    def possible_moves(x, y):
        moves = [[x+1, y+1], [x-1, y+1], [x+1, y-1], [x-1, y-1]]
        kmoves = []
        for arr in moves:
            if check_location(arr[0], arr[1]) and isinstance(board[x][y], King):
                kmoves.append(arr)
        return kmoves

class Guard:
    def __init__(self, x, y, c):
        self.color = c
        self.position = [x, y]
    def possible_moves(x, y):
        moves = [[x+1, y+1], [x-1, y+1], [x+1, y-1], [x-1, y-1], [x+2, y+2], [x-2, y+2], [x+2, y-2], [x-2, y-2]]
        gmoves = []
        for arr in moves:
            if check_location(arr[0], arr[1]) and isinstance(board[x][y], Guard):
                gmoves.append(arr)
        return gmoves

class Serf:
    def __init__(self, x, y, c):
        self.color = c
        self.position = [x, y]
    def possible_moves(x, y):
        bmoves = [[x+1, y+1], [x-1, y+1]]
        wmoves = [[x+1, y-1], [x-1, y-1]]
        smoves = []
        if Serf.color is 'Black':
            for arr in bmoves:
                if check_location(arr[0], arr[1]) and isinstance(board[x][y], Serf):
                    smoves.append(arr)
        elif Serf.color is 'White':
            for arr in wmoves:
                if check_location(arr[0], arr[1]) and isinstance(board[x][y], Serf):
                    smoves.append(arr)
        return smoves


"""
class Serf:
    position (x,y)
    color

have the def possible_moves(): a function outside of class
variables of each array of moves specific to a piece
"""

def check_location(x, y):
    return board[x][y] is not ' ' and 0 <= x <= (len(board[0])-1) and 0 <= y <= (len(board)-1)

def move_piece(x, y):
    if board[x][y] is 'S':
        print(Serf.possible_moves(x, y, 'White'))
    elif board[x][y] is '$':
        print(Serf.possible_moves(x, y, 'Black'))
    elif board[x][y]
        piece = board[x][y]
        board[x][y] = ' '
        board[arr[0]][arr[1]] = piece
    else:
        print(False)

def capture():
    pass

def print_board():
    for x in range(len(board)-1):
        sys.stdout.write(' ')
        for y in range(len(board[0])-1):
            sys.stdout.write(board[x][y] + ' # ')
        print(board[x][9] + '\n#######################################')
    sys.stdout.write(' ')
    for y in range(len(board[0])-1):
        sys.stdout.write(board[9][y] + ' # ')
    print(board[9][9] + '\n')

"""
for y in range(3):
    for x in range(len(board[0])-1):
        if board[x][y] is '$':
            black_pieces.append(Serf(x, y, 'Black'))
        elif board[x][y] is 'g':
            black_pieces.append(Guard(x, y, 'Black'))
        elif board[x][y] is 'B':
            black_pieces.append(King(x, y, 'Black'))
print(black_pieces[5].position)
for y in range(7,10):
    for x in range(len(board[0])-1):
        if board[x][y] is 'S':
            white_pieces.append(Serf(x, y, 'White'))
        elif board[x][y] is 'G':
            white_pieces.append(Guard(x, y, 'White'))
        elif board[x][y] is 'W':
            white_pieces.append(King(x, y, 'White'))
print(white_pieces[0].color)
"""
"""
while not winner:
    pass
"""
print(board[0][0])
print(Serf(0,0,'Black').position)
print(Serf(0,0,'White').color)

#unicode = {White: {King:'♔', Guard: '♘', Serf: '♙'}, Black: {King: '♚', Guard: '♞', Serf: '♟'}}
