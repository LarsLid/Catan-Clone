import pygame
import sys
import math
import numpy as np
import random as rd

pygame.init()

WIDTH, HEIGHT = 1200, 700
cx, cy = WIDTH//2, HEIGHT//2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catan")

#Colors
BG_COLOR  = (30, 80, 160)
BTN_COLOR = (220, 180, 80)
BTN_HOVER = (240, 200, 100)
BTN_TEXT  = (30, 30, 30)
BOARD = (255, 198, 41)

#Images
ore_tile = pygame.image.load("ore_tile.png").convert_alpha()
sheep_tile = pygame.image.load("sheep_tile.png").convert_alpha()
brick_tile = pygame.image.load("brick_tile.png").convert_alpha()
wheat_tile = pygame.image.load("wheat_tile.png").convert_alpha()
timber_tile = pygame.image.load("timber_tile.png").convert_alpha()
desert_tile = pygame.image.load("desert_tile.png").convert_alpha()

tile_types = [ore_tile, sheep_tile, brick_tile, wheat_tile, timber_tile, desert_tile]

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



#UI
font = pygame.font.SysFont(None, 36)
toggle_font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()
endturn_pos = (WIDTH // 1.3, HEIGHT// 1.1 )
endturn_size = (180,50)
endturn_rect = pygame.Rect(endturn_pos[0]-endturn_size[0]//2,
                       endturn_pos[1]-endturn_size[1]//2,
                        endturn_size[0], endturn_size[1])

# Generate map button (same size/structure as other buttons, placed above end turn)
gen_pos = (WIDTH//1.3, HEIGHT // 1.5)
gen_size = endturn_size
gen_rect = pygame.Rect(gen_pos[0]-gen_size[0]//2,
                       gen_pos[1]-gen_size[1]//2,
                        gen_size[0], gen_size[1])

# Small toggle button to the right of Generate map
toggle_size = (140, 40)
toggle_rect = pygame.Rect(gen_rect.right + 12, gen_rect.top, toggle_size[0], toggle_size[1])

# Startm game button
startgame_pos = (WIDTH // 1.3, HEIGHT// 1.3 )
startgame_size = (180,50)
startgame_rect = pygame.Rect(startgame_pos[0]-startgame_size[0]//2,
                       startgame_pos[1]-startgame_size[1]//2,
                        startgame_size[0], startgame_size[1])


r=65 #Hex radius
bg_tile_pts = [(-math.sqrt(3)/2*r, -r/2), (0,-r), (math.sqrt(3)/2*r, -r/2),
               (math.sqrt(3)/2*r, r/2), (0,r), (-math.sqrt(3)/2*r, r/2)]

#BoardSetup
def BoardSetup(pts, r=65):
    tile_centres = []
    s= math.sqrt(3)/2*r
    h= r/2
    oy=200
    for i in range(3):
        ox=100+2*s+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=0)
        tile_centres.append((ox,oy))
    oy=200+(r+h)
    for i in range(4):
        ox=100+s+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=0)
        tile_centres.append((ox,oy))
    oy=200+2*(r+h)
    for i in range(5):
        ox=100+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=0)
        tile_centres.append((ox,oy))
    oy=200+3*(r+h)
    for i in range(4):
        ox=100+s+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=0)
        tile_centres.append((ox,oy))
    oy=200+4*(r+h)
    for i in range(3):
        ox=100+2*s+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=0)
        tile_centres.append((ox,oy))
    
    return tile_centres

mapseed = [rd.randint(0,4) for i in range(19)] #Not MapGen, just placeholder list
number_on_tile = [1 for i in range(19)] # Placeholder number placement
CENTER_DESERT = True
def mapGen(mapseed, number_on_tile):
    allowed_tiles = [0,0,0, 1,1,1,1, 2,2,2, 3,3,3,3, 4,4,4,4, 5] #weighted odds
    numbers = [2,3,3,4,4,5,5,6,6,7,8,8,9,9,10,10,11,11,12] #Resource numbers
    if CENTER_DESERT:
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
        blit_pos = (int(cx - new_w // 2), int(cy - new_h // 2))
        screen.blit(scaled_tiles[mapseed[i]], blit_pos)
        
        #Place numbers
        number_piece = f"Number on tile {i}" #Name for objects in dict
        number_pieces[number_piece] = NumberPiece(number_on_tile[i], (cx,cy))
        number_pieces[number_piece].draw()




mapGen(mapseed, number_on_tile)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and endturn_rect.collidepoint(mouse_pos):
            print("End turn!")
        if event.type == pygame.MOUSEBUTTONDOWN and gen_rect.collidepoint(mouse_pos):
            print("Generate map")
            mapGen(mapseed, number_on_tile)
        if event.type == pygame.MOUSEBUTTONDOWN and toggle_rect.collidepoint(mouse_pos):
            # toggle center-desert state
            CENTER_DESERT = not CENTER_DESERT
            print("CENTER_DESERT set to", CENTER_DESERT)
        if event.type == pygame.MOUSEBUTTONDOWN and startgame_rect.collidepoint(mouse_pos):
            print("Start game")

    screen.fill(BG_COLOR)

    #End Turn Button
    color = BTN_HOVER if endturn_rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color, endturn_rect, border_radius=8)
    label = font.render("END TURN", True, BTN_TEXT)
    screen.blit(label, label.get_rect(center=endturn_rect.center))
    #Start Game Button
    color = BTN_HOVER if startgame_rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color, startgame_rect, border_radius=8)
    label = font.render("START GAME", True, BTN_TEXT)
    screen.blit(label, label.get_rect(center=startgame_rect.center))

    # Generate Map Button
    color = BTN_HOVER if gen_rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color, gen_rect, border_radius=8)
    label = font.render("REGENERATE", True, BTN_TEXT)
    screen.blit(label, label.get_rect(center=gen_rect.center))
    # Center Desert Toggle
    t_color = (120,220,120) if CENTER_DESERT else BTN_COLOR
    t_color = BTN_HOVER if toggle_rect.collidepoint(mouse_pos) else t_color
    pygame.draw.rect(screen, t_color, toggle_rect, border_radius=8)
    state = "ON" if CENTER_DESERT else "OFF"
    label = toggle_font.render(f"CENTER DESERT: {state}", True, BTN_TEXT)
    screen.blit(label, label.get_rect(center=toggle_rect.center))
    
    tile_centres = BoardSetup(bg_tile_pts)
    placeTiles(tile_centres)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()