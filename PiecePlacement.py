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
Costs=[["brick", "wood"],
       ["brick", "wood", "wheat", "sheep"],
       ["wheat", "wheat", "ore", "ore", "ore"],
       ["wheat", "sheep", "ore"]
       ]



def firstRound(num_players):
    print(f"firstRound called with {num_players} players")
    player_towns = []
    player_roads = []
    placed_first_town_road = []
    player_resources = []
    for i in range(num_players):
        player_towns.append([])
        player_roads.append([])
        placed_first_town_road.append(0)
        player_resources.append({"ore":0, "sheep":0, "brick":0, "wheat":0, "timber":0})

    return player_towns, player_roads, placed_first_town_road, player_resources
"""


def placeBuilding(team, new_building, mouse_pos, screen, building_lockon):
    if not new_building.placed:
        if building_lockon != (0,0):
            new_building.pos = building_lockon
        else:
            new_building.pos = mouse_pos
    new_building.draw(mouse_pos, screen) #TROR DENNE BLIR OVERSKREVET

"""
def placeBuilding(team, new_building,r, mouse_pos, screen, building_lockon, placingWhat, 
                  road_centres=None, road_orientation=None):
    if not new_building.placed:
        if building_lockon != (0,0):
            new_building.pos = building_lockon
        else:
            new_building.pos = mouse_pos
    if placingWhat == "road":
        new_building.draw(mouse_pos, screen,r, road_centres, road_orientation, building_lockon)
    elif placingWhat == "town":
        new_building.draw(mouse_pos, screen)


def canPlaceCheck (new_building, screen, primary_list, secondary_list, r, placingWhat, player, cur_game_state, placed_first_town_road):
    x,y = new_building.pos
    if placingWhat == "town":
        if cur_game_state == "FirstRound":
            if placed_first_town_road[player-1] in [0,3]:
                notStranded = True
            else:
                return False #Town road town road placed order on first round
        else:
            notStranded = False
            for lists in secondary_list:
                for road in secondary_list[player-1]: #Next to road from same player?
                    dx = x-road.pos[0]
                    dy = y-road.pos[1]
                    d=math.sqrt(dx**2+dy**2)
                    if d <= r*1.2:
                        notStranded = True
        for lists in primary_list:
            for town in lists:
                dx = x-town.pos[0]
                dy = y-town.pos[1]
                d=math.sqrt(dx**2+dy**2)
                if d <= r*1.2:
                    return False
        if notStranded:
            return True
    elif placingWhat == "road":
        if cur_game_state == "FirstRound":
            if placed_first_town_road[player-1] in [1,4]:
                pass
            else:
                return False #Town road town road placed order on first round
        notStranded = False
        for road in primary_list[player-1]: #Next to road from same player?
            dx = x-road.pos[0]
            dy = y-road.pos[1]
            d=math.sqrt(dx**2+dy**2)
            if d <= r*1.2:
                notStranded = True
        for town in secondary_list[player-1]: #Next to town from same player?
            dx = x-town.pos[0]
            dy = y-town.pos[1]
            d=math.sqrt(dx**2+dy**2)
            if d <= r*1.2:
                notStranded = True
        for players in primary_list: #On any existing road?
                for road in players:
                    if math.isclose(road.pos[0], x) and math.isclose(road.pos[1], y):
                        return False
        return notStranded

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

    def draw(self, mouse_pos, screen, r=None):
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
        self.orientation = "hor"
        

    
    def draw(self, mouse_pos, screen,r, road_centres=None, road_orientation=None, road_lockon=None):
        x, y = self.pos
        r1=r*0.8
        s1=math.sqrt(3)/2*r1
        r2=r1*0.8
        s2=s1*0.8

        if self.placed:
            pass
        else:
            if road_lockon != (0,0):
                if self.team == 5:
                    self.orientation = "hor"
                elif road_centres is not None:
                    index = road_centres.index(self.pos)
                    self.orientation = road_orientation[index]
            else:
                self.orientation = "hor"

        if self.orientation == "leftup":
            pygame.draw.line(screen, (0,0,0), (x-s1/2,y-r1/4), (x+s1/2,y+r1/4), 12)
            pygame.draw.line(screen, self.color, (x-s2/2,y-r2/4), (x+s2/2,y+r2/4), 8)
        elif self.orientation == "rightup":
            pygame.draw.line(screen, (0,0,0), (x-s1/2,y+r1/4), (x+s1/2,y-r1/4), 12)
            pygame.draw.line(screen, self.color, (x-s2/2,y+r2/4), (x+s2/2,y-r2/4), 8)
        elif self.orientation == "vert":
            pygame.draw.line(screen, (0,0,0), (x,y+r1/2), (x,y-r1/2), 12)
            pygame.draw.line(screen, self.color, (x,y+r2/2), (x,y-r2/2), 8)
        elif self.orientation == "hor":
            pygame.draw.line(screen, (0,0,0), (x-r1/2,y), (x+r1/2,y), 12)
            pygame.draw.line(screen, self.color, (x-r2/2,y), (x+r2/2,y), 8)
                 
                  
        
        #GJØR TEGNING AVHENGIG AV ORIENTATION

     