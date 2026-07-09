import pygame
import sys
import math
import numpy as np
import random as rd
pygame.init()
from UI import *
from GameSetup import *
from GameStates import *
from PiecePlacement import *
from DiceRoll import *


pygame.display.set_caption("Catan")

player = 0
tile_types = [ore_tile, sheep_tile, brick_tile, wheat_tile, timber_tile, desert_tile]
card_types = [ore_card, sheep_card, brick_card, wheat_card, timber_card]


#Numbers for resource yield
#numbers = [2,3,3,4,4,5,5,6,6,7,8,8,9,9,10,10,11,11,12]
class NumberPiece:
    def __init__(self, number, pos):
        self.number = number
        RED=False
        if self.number == 6 or self.number == 8:
            RED = True
        self.color = (247, 49, 42) if RED else (0,0,0)
        self.bg_color = (252, 221, 119)
        self.font = pygame.font.SysFont(None, 30)
        self.pos = pos
        self.text_top_corner_x = pos[0]-7
        self.text_top_corner_y = pos[1]-7
        self.r = 20
    def draw(self):
        self.border = pygame.draw.circle(screen, (0,0,0), self.pos, self.r+4)
        self.circle = pygame.draw.circle(screen, self.bg_color, self.pos, self.r)
        self.text = self.font.render(str(self.number), True, self.color)
        screen.blit(self.text, (self.text_top_corner_x,self.text_top_corner_y))


def placeTiles (tile_centres):
    if not tile_centres:
        return

    # maximum size to fit inside the hex (percentage of hex bounding box)
    max_w = int(math.sqrt(3) * r*0.98)
    max_h = int(2 * r*0.98)
    scaled_tiles = [None] * len(tile_types)
    #Numbers
    number_pieces = {} #dict for objects

    for i in range(len(tile_types)):
        iw, ih = tile_types[i].get_size()
        scale = min(max_w / iw, max_h / ih, 1)
        new_w = max(1, int(iw * scale))
        new_h = max(1, int(ih * scale))

        scaled_tiles[i] = pygame.transform.smoothscale(tile_types[i], (new_w, new_h))


    for i in range(len(tile_centres)):
        cx, cy = tile_centres[i]
        bg_tiles_adjusted = [(x + cx, y + cy) for x, y in bg_tile_pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=0)
        blit_pos = (int(cx - new_w // 2), int(cy - new_h // 2))
        screen.blit(scaled_tiles[mapseed[i]], blit_pos)
        
        #Place numbers
        number_piece = f"Number on tile {i}" #Name for objects in dict
        number_pieces[number_piece] = NumberPiece(number_on_tile[i], (cx,cy))
        number_pieces[number_piece].draw()

def findLockon (build_spaces, mouse_pos, screen):
    building_lockon = (0,0)
    for i in range(len(build_spaces)):
        hoverCheck = pygame.Rect(build_spaces[i][0]-20, build_spaces[i][1]-20, 40, 40)
        if hoverCheck.collidepoint(mouse_pos):
            pygame.draw.circle(screen, (0,255,0), build_spaces[i], 10)
            building_lockon = (build_spaces[i][0], build_spaces[i][1])
    return building_lockon

#BOOTUP CODE

tile_centres = BoardSetup(r)
road_centres, road_orientation = generateRoadSpaces(tile_centres, screen, r)
town_spaces_main = generateTownSpaces(tile_centres, r)
mapGen(mapseed, number_on_tile, CENTER_DESERT)
snakedraft = 1

player_towns = None
player_roads = None

#First dice image
frame_rect = pygame.Rect(current_frame * FRAME_W, 0, FRAME_W, FRAME_H)
frame_surf = roll_spritesheet.subsurface(frame_rect)

#Labels
placeTownInfo = InfoText(None,cx//0.7, cy//3.5, 580, 40, 1, ["FirstRound"])

#Town Icon for store
icon_town = Town(5)
icon_town.pos = (WIDTH //1.1, HEIGHT//4)
town_store_btn = Button(None,  icon_town.pos[0], icon_town.pos[1]-15, 90, 80, ["FirstRound", "ReadyToRoll", "PlayerTurn"])
#Price
price_label_town = PriceLabel(Costs[1],WIDTH //1.3, HEIGHT//4.1,["FirstRound", "ReadyToRoll", "PlayerTurn"])

icon_road = Road(5)
icon_road.pos = (WIDTH //1.1, HEIGHT//2.5)
road_store_btn = Button(None, icon_road.pos[0], icon_road.pos[1]-15, 90, 80, ["FirstRound", "ReadyToRoll", "PlayerTurn"])
#Price
price_label_road = PriceLabel(Costs[0],WIDTH //1.3, HEIGHT//2.6,["FirstRound", "ReadyToRoll", "PlayerTurn"])

isPlacingTown = False
isPlacingRoad = False
running = True


while running:
    mouse_pos = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if endturn_btn.is_clicked(mouse_pos):
                player, cur_game_state, cur_dice_state, placed_first_town_road, snakedraft = endTurn(player, playerCount, cur_game_state, placed_first_town_road, snakedraft)
                placeTownInfo = InfoText(None,cx//0.7, cy//3.5, 580, 40, player, ["FirstRound"])
            elif gen_btn.is_clicked(mouse_pos):
                mapGen(mapseed, number_on_tile, CENTER_DESERT)
            elif toggle_btn.is_clicked(mouse_pos):
                CENTER_DESERT = not CENTER_DESERT
            elif not show_player_selection and startgame_btn.is_clicked(mouse_pos):
                show_player_selection = True
            elif show_player_selection:
                for idx, btn in enumerate(player_btns):
                    if btn.is_clicked(mouse_pos):
                        playerCount = idx+2
                        player_towns, player_roads, placed_first_town_road, player_resources = firstRound(playerCount)
                        player = 1
                        print(f"PLAYER {player}'S TURN")
                        cur_game_state = "FirstRound"
                        building_lockon = (0,0)
                        show_player_selection = False
                        break
            elif throw_dice_btn.is_clicked(mouse_pos) and cur_dice_state=="Ready" and cur_game_state == "ReadyToRoll":
                current_frame = 0
                cur_dice_state = "Animating"
                last_frame_time = pygame.time.get_ticks()
                roll_value, frame_surf_result = calculateRoll()
                
            elif town_store_btn.is_clicked(mouse_pos) and cur_game_state in ["FirstRound","PlayerTurn"]:
                if isPlacingTown:
                    isPlacingTown = False
                elif isPlacingTown == False and isPlacingRoad == False:
                    isPlacingTown = True
                    new_town = Town(player)
            elif road_store_btn.is_clicked(mouse_pos) and cur_game_state in ["FirstRound","PlayerTurn"]:
                if isPlacingRoad:
                    isPlacingRoad = False
                elif isPlacingRoad == False and isPlacingTown == False:
                    isPlacingRoad = True
                    new_road = Road(player)
            elif isPlacingTown and building_lockon != (0,0) and canPlaceCheck(new_town, screen, player_towns, player_roads, r, "town", player, cur_game_state, placed_first_town_road):
                new_town.pos = building_lockon
                new_town.placed = True
                isPlacingTown = False
                new_town.adjacent = findAdjacent(new_town, tile_centres, number_on_tile, r)
                player_towns[player-1].append(new_town)
                placed_first_town_road[player-1]+=1
            elif isPlacingRoad and building_lockon != (0,0) and canPlaceCheck(new_road, screen, player_roads, player_towns, r, "road", player, cur_game_state, placed_first_town_road):
                new_road.pos = building_lockon
                new_road.placed = True
                isPlacingRoad = False
                player_roads[player-1].append(new_road)
                placed_first_town_road[player-1]+=1
    screen.fill(BG_COLOR)

    endturn_btn.draw(mouse_pos, cur_game_state)
    gen_btn.draw(mouse_pos, cur_game_state)
    toggle_btn.label = f"CENTER DESERT: {'ON' if CENTER_DESERT else 'OFF'}"
    toggle_btn.color = (120, 220, 120) if CENTER_DESERT else BTN_COLOR
    toggle_btn.draw(mouse_pos, cur_game_state)

    if show_player_selection:
        for btn in player_btns:
            btn.draw(mouse_pos, cur_game_state)
    else:
        startgame_btn.draw(mouse_pos, cur_game_state)

    #Draw Text
    if snakedraft == 1:
        placeTownInfo.label = f"PLAYER {placeTownInfo.player}'s TURN: PLACE 1 TOWN AND 1 ROAD"
    else:
        placeTownInfo.color = (255,0,0)
        placeTownInfo.label = f"PLAYER {placeTownInfo.player}'s TURN: PLACE 1 TOWN AND 1 ROAD AGAIN"
    placeTownInfo.draw(mouse_pos, cur_game_state)

    #Dice
    throw_dice_btn.draw(mouse_pos, cur_game_state)
    if cur_dice_state=="Animating":
        
        frame_rect = pygame.Rect(current_frame * FRAME_W, 0, FRAME_W, FRAME_H)
        frame_surf = roll_spritesheet.subsurface(frame_rect)

        now = pygame.time.get_ticks()
        if now - last_frame_time > FRAME_DURATION:
            current_frame += 1
            last_frame_time = now
            if current_frame >= NUM_FRAMES:
                current_frame = NUM_FRAMES - 1
                cur_dice_state = "Done"
                cur_game_state = "PlayerTurn"
                collectCards(player_towns, player_resources,number_on_tile , roll_value, mapseed)
                frame_surf = frame_surf_result

    
    




    placeTiles(tile_centres)
    if isPlacingTown:
        building_lockon = findLockon(town_spaces_main, mouse_pos, screen)
    elif isPlacingRoad:
        building_lockon = findLockon(road_centres, mouse_pos, screen)
    if cur_game_state in ["FirstRound","ReadyToRoll", "PlayerTurn"]:
        #Dice
        screen.blit(frame_surf, (WIDTH//1.6, HEIGHT//1.2)) 
        #CardHolder UI
        card_area_rect = pygame.Rect(20, HEIGHT//1.25, WIDTH//1.7, 130)
        fg_rect = pygame.Rect(40, HEIGHT//1.25, WIDTH//1.8, 110)
        pygame.draw.rect(screen, (102, 62, 17), card_area_rect)
        pygame.draw.rect(screen, (186, 118, 41), fg_rect)

        drawCards(player_resources, player-1, card_types, mouse_pos)

        """
        testCard = Card(card_types[1], 0, 400, 100)
        testCard.draw()
        """


        #Store
        town_store_btn.draw_icon(mouse_pos, cur_game_state, icon_town,r)
        road_store_btn.draw_icon(mouse_pos, cur_game_state, icon_road,r)

        price_label_town.draw(mouse_pos, cur_game_state, card_types)
        price_label_road.draw(mouse_pos, cur_game_state, card_types)


    #Draw player Towns
    if player_towns != None:
        for lists in player_roads:
            for road in lists:
                road.draw(mouse_pos, screen,r, road_centres, road_orientation, building_lockon)
        for lists in player_towns:
            for town in lists:
                town.draw(mouse_pos, screen)
        


    if isPlacingTown:
        placeBuilding(player, new_town,r, mouse_pos, screen, building_lockon, "town")
    elif isPlacingRoad:
        placeBuilding(player, new_road,r, mouse_pos, screen, building_lockon, "road", road_centres, road_orientation, )

    #Debug
    game_state_lbl = InfoText(f"{cur_game_state}", 80, 30, 150, 50, player, visible_in_game_state=["Menu", "FirstRound", "ReadyToRoll", "PlayerTurn", "Trade(?)", "Victory"])
    game_state_lbl.draw(mouse_pos, cur_game_state)

    #Draw road points
    """
        for i in road_centres:
        pygame.draw.circle(screen, (255,0,0), i, 10)
    """

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()