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
print(cur_game_state)


def endTurn(player, playerCount):
    cur_game_state = "ReadyToRoll"
    cur_dice_state = "Ready"
    if player< playerCount:
        player+=1
    else:
        player=1
    return player, cur_game_state, cur_dice_state


#Resource collection
def collectCards(towns, tiles, ):
    pass
