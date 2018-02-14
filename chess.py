import pygame
pygame.init()

##################
# Initialization #
##################

scr_width = 600
scr_height = 600
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
        self.pieces_left = ["king", "queen", "rook", "rook", "bishop", "bishop", "knight", "knight",
                            "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]

    def take_turn(self, piece, space):
        """ The player takes their turn, moving PIECE to SPACE and/or capturing an opposing piece if possible. """
        assert piece.player == self, "This is not your piece."
        if piece.valid_move(space):
            if space.piece and space.piece.player == self.opponent:
                piece.capture(space.piece)
            piece.move(space)

    def __repr__(self):
        return self.color


class Space(object):
    """ A space on the board. It may be inhabited by a Piece. """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.piece = None

    def __repr__(self):
        """ A space is represented by a letter (A-H) and a number (1-8). """
        return '{0}{1}'.format(chr(self.x + 96), self.y)


class Piece(object):
    """ Pieces move to different spaces and capture opposing pieces. """

    def __init__(self, player, name, img, x_pos, y_pos):
        self.player = player
        self.name = name
        self.img = img
        # the space attribute is either a Space object or None (if the piece has been captured)
        self.space = Space(x_pos, y_pos)
        self.space.piece = self
        self.movement = None
        self.captured = False

    def move(self, space):
        """ Move the piece to the given SPACE. """
        self.space.piece = None
        self.space = space
        space.piece = self

    def capture(self, opponent):
        """ Capture the opposing piece OPPONENT, removing it from its space and the opposing player's pieces_left. """
        opponent.space = None
        opponent.captured = True
        opponent.player.pieces_left -= opponent.name

    def valid_move(self, space):
        """ Check if the move to SPACE is a valid move for this piece. """
        return (space.x - self.space.x, space.y - self.space.y) in self.movement

    def __repr__(self):
        return '{0} {1}'.format(self.player.color, self.name)


class Finite(Piece):
    """ A Finite is a Piece that can only move a finite number of spaces each turn. """

    def __init__(self, player, name, img, x_pos, y_pos, movement):
        super().__init__(player, name, img, x_pos, y_pos)
        # the movement attribute is a list of two-value tuples that stores the possible x and y moves for a piece
        self.movement = movement


class Pawn(Finite):
    """ The pawn is the most unique character in chess, having different mechanics for capturing and moving
    and being able to move twice on its first move. """

    def __init__(self, player, img, x_pos, y_pos, movement):
        super().__init__(player, "pawn", img, x_pos, y_pos, movement)
        if player.name == "white":
            self.capture_moves = w_pawn_capture_moves
            first_moves = w_pawn_first_moves
        else:
            self.capture_moves = b_pawn_capture_moves
            first_moves = b_pawn_first_moves
        self.first_moves = self.movement + first_moves
        # has the pawn made its first move yet? (to determine if it can move 2 spaces)
        self.moved = False

    def move(self, space):
        super().move(space)
        self.moved = True

    def valid_move(self, space):
        """ A pawn's valid moves depend on whether or not it is capturing another piece. """
        move = (space.x - self.space.x, space.y - self.space.y) in self.movement
        if space.piece and space.piece.player == self.player.opponent:
            capture = (space.x - self.space.x, space.y - self.space.y) in self.capture_moves
        return move or capture


white = Player("white", True)
black = Player("black", False)
white.opponent = black
black.opponent = white
w_king = Finite(white, "king", w_king_img, 5, 1, king_moves)

############
# Gameplay #
############

while running:

    # while there is no winner
    if winner == 0:

        # get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False