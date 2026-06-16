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

roll_value = 0

def start_roll():
    pass
    #Not used atm

def calculateRoll():
    die1_value = rd.randint(1,6)
    die2_value = rd.randint(1,6)
    roll_value = die1_value+die2_value
    #The -0.75 part is kind of confusing, but centers each individual surface on the center of the die.
    die1_surf = die_spritesheet.subsurface(pygame.Rect((die1_value-0.75)*FRAME_W, 0, FRAME_W//2, FRAME_H))
    die2_surf = die_spritesheet.subsurface(pygame.Rect((die2_value-0.75)*FRAME_W, 0, FRAME_W//2, FRAME_H))
    combined_result_surf = pygame.Surface((FRAME_W, FRAME_H), pygame.SRCALPHA)
    combined_result_surf.blit(die1_surf, (0,0))
    combined_result_surf.blit(die2_surf, (FRAME_W//2,0))
    print(die1_value, die2_value)

    return roll_value, combined_result_surf
