import pygame
from checkers.constants import BLACK,ROWS,RED,SQUARE_SIZE

class Board:
    def __init__(self):
       self.board = [ ]
       self.selected_piece = None # Have we or have we not selected a piece
       self.red_left = self.white_left = 12 # how many red and how many white pieces we have
       self.red_kings = self.white_kings = 0


    def draw_squares(self,win):
         #give me some surface which is gonna be our window
         win.fill(BLACK)
         for row in range(ROWS):
             for col in range(row % 2, ROWS, 2):
                 # we wanna draw a cheker board pattern, so when we start from column we have to start from column 1 or column 0
                 pygame.draw.rectangle(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE))
                 
                 # WHENEVER WE DRAW SOMETHING IN PYGAME WE START FROM TOPLEFT COORDINATE
