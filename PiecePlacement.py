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
store = (84,84,84) #Store

color_team = [color_team_1, color_team_2, color_team_3, color_team_4, store]



def firstRound(num_players):
    print(f"firstRound called with {num_players} players")
    player_towns = []
    for i in range(num_players):
        player_towns.append([])

    return player_towns

def placeTown(team, new_town, mouse_pos, screen, town_lockon):
    if not new_town.placed:
        if town_lockon != (0,0):
            new_town.pos = town_lockon
        else:
            new_town.pos = mouse_pos
    new_town.draw(mouse_pos, screen)

def canPlaceCheck (new_town, screen, player_towns, r):
    x,y = new_town.pos
    for lists in player_towns:
        for town in lists:
             dx = x-town.pos[0]
             dy = y-town.pos[1]
             d=math.sqrt(dx**2+dy**2)
             if d <= r*1.2:
                  return False
    return True

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
                        adjacent.append(index)
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
        oy = y - 12

        for color, w, h, roof_h, eave in [
            ((0,0,0),    20, 18, 19, 5),
            (self.color, 16, 14, 16, 2),
        ]:
            pts = [
                (x - w,        oy + h),
                (x + w,        oy + h),
                (x + w,        oy),
                (x + w + eave, oy),
                (x,            oy - roof_h),
                (x - w - eave, oy),
                (x - w,        oy),
            ]
            pygame.draw.polygon(screen, color, pts)
        

class Road:
     def __init__(self, team):
        self.pos = 0
        self.team = team
        self.color = color_team[self.team-1]
        self.size = 1
        self.placed = False
    
