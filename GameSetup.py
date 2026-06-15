import pygame
import sys
import math
import numpy as np
import random as rd

r=65 #Hex radius
bg_tile_pts = [(-math.sqrt(3)/2*r, -r/2), (0,-r), (math.sqrt(3)/2*r, -r/2),
               (math.sqrt(3)/2*r, r/2), (0,r), (-math.sqrt(3)/2*r, r/2)]

#BoardSetup
def BoardSetup(r=65):
    tile_centres = []
    s= math.sqrt(3)/2*r
    h= r/2
    board_height = 100
    oy=board_height
    for i in range(3):
        ox=100+2*s+2*s*i
        tile_centres.append((ox,oy))
    oy=board_height+(r+h)
    for i in range(4):
        ox=100+s+2*s*i
        tile_centres.append((ox,oy))
    oy=board_height+2*(r+h)
    for i in range(5):
        ox=100+2*s*i
        tile_centres.append((ox,oy))
    oy=board_height+3*(r+h)
    for i in range(4):
        ox=100+s+2*s*i
        tile_centres.append((ox,oy))
    oy=board_height+4*(r+h)
    for i in range(3):
        ox=100+2*s+2*s*i
        tile_centres.append((ox,oy))
    
    return tile_centres

mapseed = [rd.randint(0,4) for i in range(19)] #Not MapGen, just placeholder list
number_on_tile = [1 for i in range(19)] # Placeholder number placement
CENTER_DESERT = True #cd
def mapGen(mapseed, number_on_tile, cd):
    allowed_tiles = [0,0,0, 1,1,1,1, 2,2,2, 3,3,3,3, 4,4,4,4, 5] #weighted odds
    numbers = [2,3,3,4,4,5,5,6,6,7,8,8,9,9,10,10,11,11,12] #Resource numbers
    if cd:
        allowed_tiles.pop(-1)
        j=0
        for i in range(19):
            if i == 9:
                continue
  
            else:
                j+=1
                allowed_tile_index =rd.randint(0,18-j)
                mapseed[i]=allowed_tiles[allowed_tile_index]
                allowed_tiles.pop(allowed_tile_index)
        mapseed[9]=5
    else:
        for i in range(19):
            allowed_tile_index =rd.randint(0,18-i)
            mapseed[i]=allowed_tiles[allowed_tile_index]
            allowed_tiles.pop(allowed_tile_index)

    #Placing numbers
    desertIndex = mapseed.index(5)
    number_on_tile[desertIndex]=7
    numbers.pop(9) #number 7 has index 9
    j=0
    for i in range(19):
        if i ==desertIndex:
            continue #skip desert (always 7)
        else:
            j+=1
            number_index =rd.randint(0,18-j)
            number_on_tile[i]=numbers[number_index]
            numbers.pop(number_index)

print(mapseed)