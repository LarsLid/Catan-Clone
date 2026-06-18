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
    if not new_town.placed:
        if town_lockon != (0,0):
            new_town.pos = town_lockon
        else:
            new_town.pos = mouse_pos
    new_town.draw(mouse_pos, screen)

def findAdjacent(new_town, tile_centres, number_on_tile, r):
    s = math.sqrt(3)/2*r
    adjacent = []
    for centre in tile_centres:
                    index = None
                    if math.isclose(centre[0], new_town.pos[0], abs_tol=5) and math.isclose(centre[1], new_town.pos[1]-r, abs_tol=5):
                        index = tile_centres.index(centre)
                    elif math.isclose(centre[0], new_town.pos[0]+s, abs_tol=5) and math.isclose(centre[1], new_town.pos[1]-r/2, abs_tol=5):
                        index = tile_centres.index(centre)
                    elif math.isclose(centre[0], new_town.pos[0]+s, abs_tol=5) and math.isclose(centre[1], new_town.pos[1]+r/2, abs_tol=5):
                        index = tile_centres.index(centre)
                    elif math.isclose(centre[0], new_town.pos[0], abs_tol=5) and math.isclose(centre[1], new_town.pos[1]+r, abs_tol=5):
                        index = tile_centres.index(centre)
                    elif math.isclose(centre[0], new_town.pos[0]-s, abs_tol=5) and math.isclose(centre[1], new_town.pos[1]+r/2, abs_tol=5):
                        index = tile_centres.index(centre)
                    elif math.isclose(centre[0], new_town.pos[0]-s, abs_tol=5) and math.isclose(centre[1], new_town.pos[1]-r/2, abs_tol=5):
                        index = tile_centres.index(centre)
                    if index != None:
                        adjacent.append(number_on_tile[index])
    return adjacent
                    
            





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
        #The (y-10) draws the town slightly above the town space center
        self.rect_bg = pygame.Rect(x-bg_w//2, (y-10)-bg_h//2, bg_w*self.size, bg_h*self.size)
        self.rect_fg = pygame.Rect(x-w//2, (y-10)-h//2, w*self.size, h*self.size)
        pygame.draw.rect(screen, (0,0,0), self.rect_bg)
        pygame.draw.rect(screen, self.color, self.rect_fg)
        print(f"tile {self.adjacent} adjacent")
        

        
    
