import pygame
import sys
import math
import numpy as np
import random as rd

#Game States
"""
Menu = True
FirstRound = False
ReadyToRoll = False
PlayerTurn = False
Trade = False
Victory = False
"""


GameStates = ["Menu", "FirstRound", "ReadyToRoll", "PlayerTurn", "Trade(?)", "Victory"]
cur_game_state = "Menu"



def endTurn(player, playerCount, cur_game_state, placed_first_town_road, snakedraft):
    cur_dice_state = "Done"

    if cur_game_state == "FirstRound":
        if placed_first_town_road[player-1] in [2,5]:
            pass
        else:
            return player, cur_game_state, cur_dice_state, placed_first_town_road, snakedraft
        placed_first_town_road[player-1]+=1
        if player==playerCount and snakedraft==1:
            snakedraft = -1
            player+=1 #Last player gets two consecutive turns
        player+=snakedraft
        if player==0 and snakedraft == -1:
            cur_game_state = "ReadyToRoll"
            cur_dice_state = "Ready"
            player = 1

    else:
        cur_game_state = "ReadyToRoll"
        cur_dice_state = "Ready"
        if player< playerCount:
            player+=1
        else:
            player=1

    return player, cur_game_state, cur_dice_state, placed_first_town_road, snakedraft


#Resource collection
def collectCards(player_towns, player_resources, number_on_tile, roll, mapseed):
    for i in range(len(player_towns)):
        for town in player_towns[i]:
            for tile in town.adjacent:
                if roll == number_on_tile[tile]:
                    if mapseed[tile] == 0:
                        player_resources[i]["ore"]+=1
                    elif mapseed[tile] == 1:
                        player_resources[i]["sheep"]+=1
                    elif mapseed[tile] == 2:
                        player_resources[i]["brick"]+=1
                    elif mapseed[tile] == 3:
                        player_resources[i]["wheat"]+=1
                    elif mapseed[tile] == 4:
                        player_resources[i]["timber"]+=1
                    else:
                        pass
                    print(f"Tile {tile} has number {roll} and can be collected")
    print(f"Current resource hands:")
    for i in player_resources:
        print(i)




