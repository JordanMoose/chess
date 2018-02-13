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
# player 1's total playtime
tot_time_1 = 0.0
# player 2's total playtime
tot_time_2 = 0.0
# player 1's current turn playtime
time_1 = 0.0
# player 2's current turn playtime
time_2 = 0.0
# who wins the game (0: game not over, 1: player 1 wins, 2: player 2 wins)
winner = 0

class Player(object):

    def __init__(self, color):
        self.color = color
        self.pieces_left = ["king", "queen", "rook", "rook", "bishop", "bishop", "knight", "knight",
                            "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]

class Piece(object):

    def __init__(self, x_pos, y_pos, movement):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.movement = movement



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