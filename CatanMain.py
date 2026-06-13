import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 1200, 700
cx, cy = WIDTH//2, HEIGHT//2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catan")

BG_COLOR  = (30, 80, 160)
BTN_COLOR = (220, 180, 80)
BTN_HOVER = (240, 200, 100)
BTN_TEXT  = (30, 30, 30)
BOARD = (255, 198, 41)

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
endturn_pos = (WIDTH // 1.2, HEIGHT// 1.1 )
endturn_size = (180,50)
btn_rect = pygame.Rect(endturn_pos[0]-endturn_size[0]//2,
                       endturn_pos[1]-endturn_size[1]//2,
                        endturn_size[0], endturn_size[1])

r=65 #Hex radius
bg_tile_pts = [(-math.sqrt(3)/2*r, -r/2), (0,-r), (math.sqrt(3)/2*r, -r/2),
               (math.sqrt(3)/2*r, r/2), (0,r), (-math.sqrt(3)/2*r, r/2)]

#BoardSetup
def BoardSetup(pts, r=65):
    s= math.sqrt(3)/2*r
    h= r/2
    oy=200
    for i in range(3):
        ox=100+2*s+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=1)
    oy=200+(r+h)
    for i in range(4):
        ox=100+s+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=1)
    oy=200+2*(r+h)
    for i in range(5):
        ox=100+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=1)
    oy=200+3*(r+h)
    for i in range(4):
        ox=100+s+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=1)
    oy=200+4*(r+h)
    for i in range(3):
        ox=100+2*s+2*s*i
        bg_tiles_adjusted = [(x + ox, y + oy) for x,y in pts]
        pygame.draw.polygon(screen, BOARD, bg_tiles_adjusted, width=1)


    


running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(mouse_pos):
            print("End turn!")

    screen.fill(BG_COLOR)

    color = BTN_HOVER if btn_rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color, btn_rect, border_radius=8)
    label = font.render("END TURN", True, BTN_TEXT)
    screen.blit(label, label.get_rect(center=btn_rect.center))
    
    BoardSetup(bg_tile_pts)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()