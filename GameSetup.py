import pygame
import sys
import math
import numpy as np
import random as rd
from collections import defaultdict

r=50 #Hex radius (FUNKET MED 65)
bg_tile_pts = [(-math.sqrt(3)/2*r, -r/2), (0,-r), (math.sqrt(3)/2*r, -r/2),
               (math.sqrt(3)/2*r, r/2), (0,r), (-math.sqrt(3)/2*r, r/2)]

#BoardSetup
def BoardSetup(r):
    tile_centres = []
    s= math.sqrt(3)/2*r
    h= r/2
    board_height = 100
    board_padding_width = 120
    oy=board_height
    for i in range(3):
        ox=board_padding_width+2*s+2*s*i
        tile_centres.append((ox,oy))
    oy=board_height+(r+h)
    for i in range(4):
        ox=board_padding_width+s+2*s*i
        tile_centres.append((ox,oy))
    oy=board_height+2*(r+h)
    for i in range(5):
        ox=board_padding_width+2*s*i
        tile_centres.append((ox,oy))
    oy=board_height+3*(r+h)
    for i in range(4):
        ox=board_padding_width+s+2*s*i
        tile_centres.append((ox,oy))
    oy=board_height+4*(r+h)
    for i in range(3):
        ox=board_padding_width+2*s+2*s*i
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
        counter_sign+=1
        #Increase or decrease hexes in row:
        hexes_in_row+= -np.sign(counter_sign)
        oy += r + r/4 +(r//4.1)
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
    road_orientation = []
    road_centres = []
    for i in range(6):
        for j in range(hexes_in_row*2+1):
            x1_adj = x1+j*s
            y1_adj = y1+flipper*r/4
            if j<hexes_in_row*2:
                flipper *= -1
                road_centres.append((x1_adj+s/2, y1_adj+flipper*r/4))
                if flipper == 1:
                    road_orientation.append("leftup")
                else:
                    road_orientation.append("rightup")
                pygame.draw.line(screen, (255,0,0), (x1_adj, y1_adj), (x1_adj+s, y1_adj+flipper*r/2), 4)
            if j % 2 == odd_after_middle and i<5:
                road_centres.append((x1_adj, y1_adj+r/2))
                road_orientation.append("vert")
                pygame.draw.line(screen, (255,0,0), (x1_adj, y1_adj), (x1_adj, y1_adj+r), 4)

        
        counter_sign+=1
        #Increase or decrease hexes in row:
        hexes_in_row+= -np.sign(counter_sign)
        y1 += r + r/4 +(r//4.1)
        x1 += s*np.sign(counter_sign)
        if counter_sign == 0:
            flipper*=-1
            odd_after_middle = 1
    return road_centres, road_orientation






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

trade_costs = [["general", "general", "general", "general"],
       ["general", "general", "general"],
       ["ore", "ore"],
       ["sheep", "sheep"],
       ["brick", "brick"],
       ["wheat", "wheat"],
       ["timber", "timber"]
       ]

ALTERNATING_PORTS = True
def getRingOrder(town_spaces, tile_centres, r): #For ports
    tol = r * 0.1
    boundary_idx = []
    port_pairs = []

    for i, p in enumerate(town_spaces):
        touch_count = 0
        for c in tile_centres:
            d = math.sqrt((p[0]-c[0])**2 + (p[1]-c[1])**2)
            if abs(d - r) <= tol:
                touch_count += 1
        if touch_count < 3:
            boundary_idx.append(i) #The Outer ring town spaces can at most have 2 adjacent tile centres

    cx = sum(c[0] for c in tile_centres) / len(tile_centres)
    cy = sum(c[1] for c in tile_centres) / len(tile_centres)

    boundary_idx.sort(key=lambda i: math.atan2(
        town_spaces[i][1] - cy, town_spaces[i][0] - cx
    ))
    pair = 0
    port_status = []
    for i in range(len(boundary_idx)):
        if i % 10 in (0,1,3,4,6,7):
            port_status.append(True)
            port_pairs.append(pair)
        else:
            port_status.append(False)
            port_pairs.append(None)
            pair+=1
    



    #port_status = [i % 10 in (0, 1, 3, 4, 6, 7) for i in range(len(boundary_idx))] #Decides whether an outer ring space is a port

    return boundary_idx, port_status, port_pairs


def getOrientation(ring_spaces, port_pairs, tile_centres, r):
    tol = r // 4.1  # same tolerance pattern as getRingOrder

    pairs = defaultdict(list)
    for pair_number, space in zip(port_pairs, ring_spaces):
        if pair_number is not None:          # drop the non-port vertices
            pairs[pair_number].append(space)
    result = list(pairs.values())

    orientations = ["NE", "E", "SE", "SW", "W", "NW"]
    degs = [30, 90, 150, 210, 270, 330]

    port_orientations = []
    tile_debug_list = []
    for p1, p2 in result:
        # the one tile both pair positions are within reach of
        tile = next(c for c in tile_centres
                    if abs(math.dist(p1, c) - r) <= tol and abs(math.dist(p2, c) - r) <= tol)

        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 #Line midpoint
        angle = math.degrees(math.atan2(my - tile[1], mx - tile[0])) % 360 + 90

        best_deg = min(degs, key=lambda d: min(abs(d - angle), 360 - abs(d - angle)))
        orientation = orientations[degs.index(best_deg)]
        port_orientations.append(orientation)
        port_orientations.append(orientation)
        tile_debug_list.append(tile_centres.index(tile))
    print(tile_debug_list)

    return result, port_orientations



def generatePorts(ring_spaces, port_status, port_pairs, tile_centres,r):
    ports = []
    result, port_orientations = getOrientation(ring_spaces, port_pairs,tile_centres, r)
    i=0
    tilt = 15
    for pos in ring_spaces:
        if port_status[ring_spaces.index(pos)]:
            print(port_orientations[i])
            ports.append(Port(port_orientations[i], pos, ["Wheat","Wheat","Wheat"], tilt))
            i+=1
            tilt *= -1
    return ports

def generateTrades(alternatingPorts):
    trade_node_pool = [
        ["ore", "ore"],
        ["general", "general", "general"],
        ["sheep", "sheep"],
        ["general", "general", "general"],
        ["brick", "brick"],
        ["general", "general", "general"],
        ["wheat", "wheat"],
        ["general", "general", "general"],
        ["timber", "timber"]
    ]

    tradeNodes = []
    if alternatingPorts:
        nodeIndex = rd.randint(0,8)
        for i in range(9):
            tradeNodes.append(trade_node_pool[nodeIndex])
            if nodeIndex == 8:
                nodeIndex=0
            else:
                nodeIndex+=1
    else:
        for i in range(9):
            randomIndex = rd.randint(0,(len(trade_node_pool)-1))
            tradeNodes.append(trade_node_pool[randomIndex])
            trade_node_pool.pop(randomIndex)

    nodeIcons = []
    for node in tradeNodes:
        nodeIcons.append(node[0])

    
    
            
            
    return tradeNodes, nodeIcons




def offsetPolygon(pts, d): #Function made by claude, could probably be simplified
    #Moves every edge outward by d, then re-derives each corner as the
    #intersection of its two adjacent offset edges (a mitered outline)
    n = len(pts)
    normals = []
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        normals.append((dy / length, -dx / length))

    def lineIntersect(p1, d1, p2, d2):
        x1, y1 = p1
        dx1, dy1 = d1
        x2, y2 = p2
        dx2, dy2 = d2
        denom = dx1 * dy2 - dy1 * dx2
        t = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / denom
        return (x1 + t * dx1, y1 + t * dy1)

    offset_pts = []
    for i in range(n):
        prev_pt, curr_pt, next_pt = pts[(i - 1) % n], pts[i], pts[(i + 1) % n]
        prev_normal, curr_normal = normals[(i - 1) % n], normals[i]

        prev_edge_start = (prev_pt[0] + d * prev_normal[0], prev_pt[1] + d * prev_normal[1])
        curr_edge_start = (curr_pt[0] + d * curr_normal[0], curr_pt[1] + d * curr_normal[1])
        prev_edge_dir = (curr_pt[0] - prev_pt[0], curr_pt[1] - prev_pt[1])
        curr_edge_dir = (next_pt[0] - curr_pt[0], next_pt[1] - curr_pt[1])

        offset_pts.append(lineIntersect(prev_edge_start, prev_edge_dir, curr_edge_start, curr_edge_dir))
    return offset_pts


class Port():
    def __init__(self, orientation, pos, trade, tilt):
        start_deg = 330 #SW 
        orientations = ["NE", "E", "SE", "SW", "W", "NW"]
        degs = [30, 90, 150, 210, 270, 330]
        self.orientation = orientation
        self.deg = degs[orientations.index(self.orientation)]
        self.tilt = tilt
        self.pos = pos
        self.color = (173, 102, 14)
        self.pts = [(2,0), (14,0), (16,50), (0, 50)]
        self.trade = trade

    def draw(self, screen,r): #Made with claude
        #Black background: same shape as the port, offset outward by a uniform distance
        border = 4
        outline_pts = offsetPolygon(self.pts, border)

        offset_r = r*0.25
        offset_x = offset_r*math.sin(math.radians(self.deg))
        offset_y = -offset_r*math.cos(math.radians(self.deg))

        pad = 2
        min_x = min(x for x, y in outline_pts) - pad
        min_y = min(y for x, y in outline_pts) - pad
        max_x = max(x for x, y in outline_pts) + pad
        max_y = max(y for x, y in outline_pts) + pad
        w, h = int(max_x - min_x), int(max_y - min_y)

        shifted_pts = [(x - min_x, y - min_y) for x, y in self.pts]
        shifted_outline_pts = [(x - min_x, y - min_y) for x, y in outline_pts]

        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.polygon(surf, (0, 0, 0), shifted_outline_pts)
        pygame.draw.polygon(surf, self.color, shifted_pts)

        rotated_surf = pygame.transform.rotate(surf, self.deg)
        rotozoomed_surf = pygame.transform.rotozoom(surf, -(self.deg+self.tilt), 0.8)
        
        rect = rotozoomed_surf.get_rect(center=(self.pos[0] +offset_x, self.pos[1] +offset_y))
        screen.blit(rotozoomed_surf, rect)

