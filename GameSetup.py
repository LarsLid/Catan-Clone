import pygame
import sys
import math
import numpy as np
import random as rd

r=65 #Hex radius
bg_tile_pts = [(-math.sqrt(3)/2*r, -r/2), (0,-r), (math.sqrt(3)/2*r, -r/2),
               (math.sqrt(3)/2*r, r/2), (0,r), (-math.sqrt(3)/2*r, r/2)]

#BoardSetup
def BoardSetup(r):
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

def generateTownSpaces(tile_centres, r):
    cx, cy = tile_centres[0]
    cx -= math.sqrt(3)/2*r
    cy -= r/2-5
    ox, oy = cx, cy - r/4
    ox_adj, oy_adj = ox, oy
    counter_sign = -3 #Ensures hex increases for three lines, then decreases
    hexes_in_row = 3
    flipper = 1
    town_spaces =[]
    for i in range(6):
        for j in range(hexes_in_row*2+1):
            
            ox_adj = ox+j*math.sqrt(3)/2*r
            oy_adj = oy+flipper*r/4
            flipper *= -1
            town_spaces.append((ox_adj,oy_adj))
        print(hexes_in_row)
        counter_sign+=1
        #Increase or decrease hexes in row:
        hexes_in_row+= -np.sign(counter_sign)
        oy += r + r/4 +15
        ox += math.sqrt(3)/2*r*np.sign(counter_sign)
        if counter_sign == 0: 
            flipper*=-1
        flipper*=-1
    return town_spaces
        

def generateRoadSpaces(tile_centres,screen, r):
    s = math.sqrt(3)/2*r
    x1, y1 = tile_centres[0]
    x1 -= math.sqrt(3)/2*r
    y1 -= 3*r/4
    counter_sign = -3 #Ensures hex increases for three lines, then decreases
    hexes_in_row = 3
    flipper = 1
    odd_after_middle = 0
    road_centres = []
    for i in range(6):
        for j in range(hexes_in_row*2+1):
            x1_adj = x1+j*s
            y1_adj = y1+flipper*r/4
            if j<hexes_in_row*2:
                flipper *= -1
                road_centres.append((x1_adj+s/2, y1_adj+flipper*r/4))
                pygame.draw.line(screen, (255,0,0), (x1_adj, y1_adj), (x1_adj+s, y1_adj+flipper*r/2), 4)
            if j % 2 == odd_after_middle and i<5:
                road_centres.append((x1_adj, y1_adj+r/2))
                pygame.draw.line(screen, (255,0,0), (x1_adj, y1_adj), (x1_adj, y1_adj+r), 4)

        
        counter_sign+=1
        #Increase or decrease hexes in row:
        hexes_in_row+= -np.sign(counter_sign)
        y1 += r + r/4 +16
        x1 += s*np.sign(counter_sign)
        if counter_sign == 0:
            flipper*=-1
            odd_after_middle = 1
    print(f"len: {len(road_centres)}")
    return road_centres
        
    
        




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