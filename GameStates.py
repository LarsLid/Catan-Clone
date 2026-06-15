import pygame
import sys
import math
import numpy as np
import random as rd

#Game States
Menu = True
FirstRound = False
ReadyToRoll = False
PlayerTurn = False
Trade = False
Victory = False

GameStates = {"Menu":Menu, "FirstRound":FirstRound, "ReadyToRoll":ReadyToRoll, "PlayerTurn":PlayerTurn, "Trade(?)":Trade, "Victory":Victory}
cur_game_state = "Menu"
print(cur_game_state)