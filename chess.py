import pygame
pygame.init()

##################
# Initialization #
##################

scr_width = 900
scr_height = 700
scr_size = (scr_width,scr_height)
scr_center = (scr_width / 2, scr_height / 2)
white = (255,255,255)
black = (0,0,0)
lime = (0,255,0)
green = (50,205,50)
red = (255,0,0)
blue = (0,0,255)
pink = (225,105,180)
skyblue = (100,210,255)
brown = (160,120,60)
cream = (235, 208, 129)

grid_font = 'Charlemagne Std'
display_font = 'Cochin'

# set screen size
screen = pygame.display.set_mode(scr_size)
# set screen name
pygame.display.set_caption("Chess")
# initialize clock
clock = pygame.time.Clock()

running = True
FPS = 60
playtime = 0.0
# white's total playtime
tot_time_w = 0.0
# black's total playtime
tot_time_b = 0.0
# white's current turn playtime
time_w = 0.0
# black's current turn playtime
time_b = 0.0
# the board's dimensions
dimensions = (8,8)
# who wins the game (0: game not over, 1: white wins, 2: black wins)
winner = 0
# load piece images
w_king_img = pygame.image.load('data/w_king.png').convert_alpha()
w_queen_img = pygame.image.load('data/w_queen.png').convert_alpha()
w_rook_img = pygame.image.load('data/w_rook.png').convert_alpha()
w_bishop_img = pygame.image.load('data/w_bishop.png').convert_alpha()
w_knight_img = pygame.image.load('data/w_knight.png').convert_alpha()
w_pawn_img = pygame.image.load('data/w_pawn.png').convert_alpha()
b_king_img = pygame.image.load('data/b_king.png').convert_alpha()
b_queen_img = pygame.image.load('data/b_queen.png').convert_alpha()
b_rook_img = pygame.image.load('data/b_rook.png').convert_alpha()
b_bishop_img = pygame.image.load('data/b_bishop.png').convert_alpha()
b_knight_img = pygame.image.load('data/b_knight.png').convert_alpha()
b_pawn_img = pygame.image.load('data/b_pawn.png').convert_alpha()
# store movements for pieces that can only move a finite number of spaces each turn
king_moves = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]
knight_moves = [(1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)]
w_pawn_moves = [(0,1)]
b_pawn_moves = [(0,-1)]
w_pawn_capture_moves = [(-1,1), (1,1)]
b_pawn_capture_moves = [(-1,-1), (1,-1)]
w_pawn_first_moves = [(0, 2)]
b_pawn_first_moves = [(0,-2)]


class Player(object):
    """ There are two players, black and white. Each has a certain set of pieces left. """

    def __init__(self, color, turn):
        self.color = color
        # is it currently this player's turn?
        self.turn = turn
        self.opponent = None
        self.pieces = None
        self.pawns = None
        # is this player's king checked?
        self.check = False

    def take_turn(self, piece, space):
        """ The player takes their turn, moving PIECE to SPACE and/or capturing an opposing piece if possible. """
        assert piece.player == self, "This is not your piece."
        # check if this is a valid move
        piece.valid_move(space)
        piece.move(space)
        self.turn = False
        self.opponent.turn = True

    def __str__(self):
        return self.color


class Space(object):
    """ A space on the board. It may be inhabited by a Piece. Spaces are 1-indexed. """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.piece = None

    def __str__(self):
        """ A space is represented by a letter (A-H) and a number (1-8). """
        return '{0}{1}'.format(chr(self.x + 64), self.y)


# create a board such that board[x][y] = Space(x, y)
board = [None, None, None, None, None, None, None, None, None]
for x in range(1, dimensions[0] + 1):
    row = [None, None, None, None, None, None, None, None, None]
    for y in range(1, dimensions[0] + 1):
        row[y] = Space(x, y)
    board[x] = row


class Piece(object):
    """ Pieces move to different spaces and capture opposing pieces. """

    def __init__(self, player, name, img, x_pos, y_pos):
        self.player = player
        self.name = name
        self.img = img
        # the space attribute is either a Space object or None (if the piece has been captured)
        self.space = Space(x_pos, y_pos)
        self.space.piece = self
        self.captured = False

    def move(self, space):
        """ Move the piece to the given SPACE. """
        if space.piece:
            self.capture(space.piece)
        self.space.piece = None
        self.space = space
        space.piece = self

    def capture(self, opponent):
        """ Capture the opposing piece OPPONENT, removing it from its space and the opposing player's pieces. """
        opponent.space = None
        opponent.captured = True
        opponent.player.pieces -= opponent

    def valid_move(self, space):
        """ Assert that the move to SPACE is a valid move for this piece.
            All pieces share that they can't move to a space that is inhabited by a friendly piece. """
        friendly = space.piece and space.piece.player == self.player
        assert not friendly, "There's a friendly piece in that space."

    def valid_vertical(self, space):
        """ Assert that the vertical move to SPACE is not obstructed by another piece. """
        start = min(self.space.y, space.y) + 1  # don't want to check the current space or target space
        stop = max(self.space.y, space.y)
        for y in range(start, stop):
            assert not board[self.space.x][y].piece, "There's a piece in the way."

    def valid_horizontal(self, space):
        """ Assert that the horizontal move to SPACE is not obstructed by another piece. """
        start = min(self.space.x, space.x) + 1  # don't want to check the current space or target space
        stop = max(self.space.x, space.x)
        for x in range(start, stop):
            assert not board[x][self.space.y].piece, "There's a piece in the way."

    def valid_diagonal(self, space):
        """ Assert that the diagonal move to SPACE is not obstructed by another piece. """
        x = min(self.space.x, space.x) + 1  # don't want to check the current space or target space
        y = min(self.space.y, space.y) + 1
        x_stop = max(self.space.x, space.x)
        y_stop = max(self.space.y, space.y)
        while x != x_stop and y != y_stop:
            assert not board[x][y].piece, "There's a piece in the way."
            x += 1
            y += 1

    def __str__(self):
        return '{0} {1}'.format(self.player.color, self.name)


class Finite(Piece):
    """ A Finite is a Piece that can only move a finite number of spaces each turn. """

    def __init__(self, player, name, img, x_pos, y_pos, movement):
        super().__init__(player, name, img, x_pos, y_pos)
        # the movement attribute is a list of two-value tuples that stores the possible x and y moves for a piece
        self.movement = movement

    def valid_move(self, space):
        """ Assert that the move to SPACE is a valid move for this piece.
            Finites can check if the move is in their movement attribute. """
        super().valid_move(space)
        assert (space.x - self.space.x, space.y - self.space.y) in self.movement,\
            "A {0} can't move this way.".format(self.name)


class King(Finite):
    """ Kings can move one space vertically, horizontally, or diagonally in any direction. """

    def __init__(self, player, name, img, x_pos, y_pos):
        super().__init__(player, name, img, x_pos, y_pos, king_moves)
        # is this king checked?
        self.check = False


class Queen(Piece):
    """ Queens can move unlimited spaces vertically, horizontally, or diagonally in any direction. """

    def valid_move(self, space):
        """ Assert that the move to SPACE is a vertical, horizontal, or diagonal move
            and that there's no piece in the way. """
        super().valid_move(space)
        vertical = space.x == self.space.x
        horizontal = space.y == self.space.y
        diagonal = abs(space.x - self.space.x) == abs(space.y - self.space.y)
        assert vertical or horizontal or diagonal, "A queen can't move this way."
        # check if there's a piece in the line of movement
        if vertical:
            super().valid_vertical(space)
        elif horizontal:
            super().valid_horizontal(space)
        elif diagonal:
            super().valid_diagonal(space)


class Rook(Piece):
    """ Rooks can move unlimited spaces vertically or horizontally in any direction. """

    def valid_move(self, space):
        """ Assert that the move to SPACE is a vertical or horizontal move
            and that there's no piece in the way. """
        super().valid_move(space)
        vertical = space.x == self.space.x
        horizontal = space.y == self.space.y
        assert vertical or horizontal, "A rook can't move this way."
        # check if there's a piece in the line of movement
        if vertical:
            super().valid_vertical(space)
        elif horizontal:
            super().valid_vertical(space)


class Bishop(Piece):
    """ Bishops can move unlimited spaces diagonally in any direction. """

    def valid_move(self, space):
        """ Assert that the move to SPACE is a diagonal move and that there's no piece in the way. """
        super().valid_move(space)
        diagonal = abs(space.x - self.space.x) == abs(space.y - self.space.y)
        assert diagonal, "A bishop can't move this way."
        # check if there's a piece in the line of movement
        super().valid_diagonal(space)


class Knight(Finite):
    """ Knights can move one space either vertically or horizontally and two spaces in the other direction.
        They can also jump over other pieces. """

    def __init__(self, player, name, img, x_pos, y_pos):
        super().__init__(player, name, img, x_pos, y_pos, knight_moves)


class Pawn(Finite):
    """ The pawn is the most unique character in chess, having different mechanics for capturing and moving
        and having the ability to move twice on its first move. """

    def __init__(self, player, name, img, x_pos, y_pos, movement):
        super().__init__(player, name, img, x_pos, y_pos, movement)
        if player.color == "white":
            self.capture_moves = w_pawn_capture_moves
            self.first_moves = w_pawn_first_moves
        else:
            self.capture_moves = b_pawn_capture_moves
            self.first_moves = b_pawn_first_moves
        self.movement += self.first_moves
        # has the pawn made its first move yet? (to determine if it can move 2 spaces)
        self.moved = False

    def move(self, space):
        super().move(space)
        if not self.moved:
            self.movement -= self.first_moves
            self.moved = True

    def valid_move(self, space):
        """ A pawn's valid moves depend on whether or not it is capturing another piece. """
        if space.piece and space.piece.player == self.player.opponent and\
          not (space.x - self.space.x, space.y - self.space.y) in self.capture_moves:
            assert (space.x - self.space.x, space.y - self.space.y) in self.capture_moves, "A pawn can't move this way."
        super().valid_move(space)


w = Player("white", True)
b = Player("black", False)
w.opponent = b
b.opponent = w

w_king = King(w, "king", w_king_img, 5, 1)
w_queen = Queen(w, "queen", w_queen_img, 4, 1)
w_l_rook = Rook(w, "left rook", w_rook_img, 1, 1)
w_r_rook = Rook(w, "right rook", w_rook_img, 8, 1)
w_l_bishop = Bishop(w, "left bishop", w_bishop_img, 3, 1)
w_r_bishop = Bishop(w, "right bishop", w_bishop_img, 6, 1)
w_l_knight = Knight(w, "left knight", w_knight_img, 2, 1)
w_r_knight = Knight(w, "left knight", w_knight_img, 7, 1)
w_pawns = []
for x in range(1, 9):
    w_pawns.append(Pawn(w, "pawn {0}".format(x), w_pawn_img, x, 2, w_pawn_moves))
w.pieces = [w_king, w_queen, w_l_rook, w_r_rook, w_l_bishop, w_r_bishop, w_l_knight, w_r_knight]
w.pawns = w_pawns

b_king = King(b, "king", b_king_img, 5, 8)
b_queen = Queen(b, "queen", b_queen_img, 4, 8)
b_l_rook = Rook(b, "left rook", b_rook_img, 1, 8)
b_r_rook = Rook(b, "right rook", b_rook_img, 8, 8)
b_l_bishop = Bishop(b, "left bishop", b_bishop_img, 3, 8)
b_r_bishop = Bishop(b, "right bishop", b_bishop_img, 6, 8)
b_l_knight = Knight(b, "left knight", b_knight_img, 2, 8)
b_r_knight = Knight(b, "left knight", b_knight_img, 7, 8)
b_pawns = []
for x in range(1, 9):
    b_pawns.append(Pawn(b, "pawn {0}".format(x), b_pawn_img, x, 7, b_pawn_moves))
b.pieces = [b_king, b_queen, b_l_rook, b_r_rook, b_l_bishop, b_r_bishop, b_l_knight, b_r_knight]
b.pawns = b_pawns


def background():
    """ Returns the gamescreen visual surface. """
    # the board itself (the screen contains other sections)
    board = pygame.image.load('data/board.jpg').convert_alpha()
    board_size = board.get_rect().size
    board_width = board_size[0]
    board_height = board_size[1]
    board = pygame.transform.rotozoom(board, 0, (scr_height * 7 / 8) / board_height)
    board_size = board.get_rect().size
    board_width = board_size[0]
    board_height = board_size[1]

    # write the numbers and letters at the edge of the board
    x_start = board_width / 10
    y_start = board_height / 10
    y_inc = board_height / 9
    x_inc = board_height * 0.1085
    for i in range(1, 9):
        write(board, str(i), cream, (board_width / 55, y_start + (i - 1) * y_inc), grid_font)

    for i in range(1, 9):
        write(board, chr(i + 64), cream, (x_start + (i - 1) * x_inc, board_height * 21 / 22), grid_font)

    return board


def write(surface, msg, color, pos, face=display_font, size=scr_height // 30):
    """ Write MSG on SURFACE at position POS. """
    font = pygame.font.SysFont(face, size)
    text = font.render(msg, True, color).convert_alpha()
    surface.blit(text, pos)


background = background()


############
# Gameplay #
############

while running:

    # blank the screen
    screen.blit(background, (0,0))

    # while there is no winner
    if winner == 0:

        # get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.display.flip()
