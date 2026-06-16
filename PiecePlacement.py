import pygame
import sys
import math
import numpy as np
import random as rd


#Team colors
color_team_1 = (209, 45, 0) #Red
color_team_2 = (255, 255, 255) #White
color_team_3 = (19, 62, 207) #Blue
color_team_4 = (43, 179, 20) #Green

color_team = [color_team_1, color_team_2, color_team_3, color_team_4]



def firstRound(num_players):
    print(f"firstRound called with {num_players} players")
    player_towns = []
    for i in range(num_players):
        player_towns.append([])

def placeTown(team, new_town, mouse_pos, screen, town_lockon):
    global isPlacing
    isPlacing = True
    new_town.pos = mouse_pos
    if town_lockon != (0,0):
        hoverCheck = pygame.Rect(town_lockon[0]-20, town_lockon[1]-20, 40, 40)
        if hoverCheck.collidepoint(mouse_pos):
            new_town.pos = town_lockon[0], town_lockon[1]-10
            print("hovertest")
    new_town.draw(mouse_pos, screen)




class Town:
    def __init__(self, team):
        self.pos = 0
        self.team = team
        self.color = color_team[self.team-1]
        self.level = 1 # 1 = Town, 2 = City
        self.adjacent = []
        self.size = 1
        self.placed = False
        

    def draw(self, mouse_pos, screen):
        x, y = self.pos
        w, h = 35, 25
        bg_w, bg_h = 42, 32

        self.rect_bg = pygame.Rect(x-bg_w//2, y-bg_h//2, bg_w*self.size, bg_h*self.size)
        self.rect_fg = pygame.Rect(x-w//2, y-h//2, w*self.size, h*self.size)
        pygame.draw.rect(screen, (0,0,0), self.rect_bg)
        pygame.draw.rect(screen, self.color, self.rect_fg)
        

        
    
