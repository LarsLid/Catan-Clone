import pygame
import sys
import math
import numpy as np
import random as rd

FRAME_W, FRAME_H = 200, 120
NUM_FRAMES = 8
FRAME_DURATION = 120  # ms per frame (de første 6 raske, siste 2 rolige)

roll_spritesheet = pygame.image.load("images/dice_spritesheet.png").convert_alpha()
die_spritesheet  = pygame.image.load("images/die_sprites.png").convert_alpha()

# I game loopen:
current_frame = 0
dice_state = ["Ready", "Animating", "Done"]
cur_dice_state = "Ready"
last_frame_time = 0

def start_roll():
    global current_frame, cur_dice_state, last_frame_time


# Inne i loopen:


