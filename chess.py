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

class Player(object):

    def __init__(self, color):
        self.color = color
        self.pieces_left = ["king", "queen", "rook", "rook", "bishop", "bishop", "knight", "knight",
                            "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]


class Piece(object):

    def __init__(self, color, name, img, x_pos, y_pos, movement):
        self.color = color
        self.name = name
        self.img = img
        self.x_pos = x_pos
        self.y_pos = y_pos
        # the movement attribute is a list of two-value tuples that stores the possible x and y moves for a piece
        self.movement = movement


white = Player("white")
black = Player("black")
w_king = Piece("white", "king", w_king_img, 5, 1, [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)])

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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False