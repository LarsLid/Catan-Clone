import pygame
import sys
import math
import numpy as np
import random as rd

WIDTH, HEIGHT = 1200, 730
cx, cy = WIDTH//2, HEIGHT//2
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BG_COLOR  = (30, 80, 160)
BTN_COLOR = (220, 180, 80)
BTN_HOVER = (240, 200, 100)
BTN_TEXT  = (30, 30, 30)
BOARD = (255, 198, 41)

#Images
ore_tile = pygame.image.load("images/ore_tile.png").convert_alpha()
sheep_tile = pygame.image.load("images/sheep_tile.png").convert_alpha()
brick_tile = pygame.image.load("images/brick_tile.png").convert_alpha()
wheat_tile = pygame.image.load("images/wheat_tile.png").convert_alpha()
timber_tile = pygame.image.load("images/timber_tile.png").convert_alpha()
desert_tile = pygame.image.load("images/desert_tile.png").convert_alpha()

font        = pygame.font.SysFont(None, 36)
hover_font  = pygame.font.SysFont(None, 38)
toggle_font = pygame.font.SysFont(None, 18)
toggle_hover_font = pygame.font.SysFont(None, 21)
clock       = pygame.time.Clock()


class Button:
    def __init__(self, label, cx, cy, w, h, visible_in_game_state=list, btn_font=None, color=BTN_COLOR, hover_color=BTN_HOVER, hover_font=hover_font):
        self.label       = label
        self.rect        = pygame.Rect(int(cx - w // 2), int(cy - h // 2), int(w), int(h))
        self.hover_rect  = self.rect.inflate(7,7)
        self.font        = btn_font if btn_font is not None else font
        self.hover_font = hover_font
        self.color       = color
        self.hover_color = hover_color
        self.visible_in_game_state = visible_in_game_state
        self.clickable = False

    def draw(self, mouse_pos, gamestate):
        if str(gamestate) in self.visible_in_game_state:
            self.clickable = True
            if self.rect.collidepoint(mouse_pos):
                rect = self.hover_rect
                c = self.hover_color
                btn_font_final = self.hover_font 
            else:
                c = self.color
                rect = self.rect
                btn_font_final = self.font

            pygame.draw.rect(screen, c, rect, border_radius=8)
            lbl = btn_font_final.render(self.label, True, BTN_TEXT)
            screen.blit(lbl, lbl.get_rect(center=self.rect.center))
        else:
            self.clickable = False

    def draw_icon(self, mouse_pos, gamestate, icon):
        if str(gamestate) in self.visible_in_game_state:
            self.clickable = True
            if self.rect.collidepoint(mouse_pos):
                rect = self.hover_rect
                c = self.hover_color
            else:
                c = self.color
                rect = self.rect
            
            pygame.draw.rect(screen, c, rect, border_radius=8)
            icon.draw(mouse_pos, screen)
        else:
            self.clickable = False

    def is_clicked(self, mouse_pos):
        if self.clickable:
            return self.rect.collidepoint(mouse_pos)
        


endturn_btn   = Button("END TURN",   WIDTH // 1.1, HEIGHT // 1.1, 180, 50, ["FirstRound", "PlayerTurn"])
startgame_btn = Button("START GAME", WIDTH // 1.3, HEIGHT // 1.3, 180, 50, ["Menu"])
gen_btn       = Button("REGENERATE", WIDTH // 1.3, HEIGHT // 1.5, 180, 50, ["Menu"])
toggle_btn    = Button("CENTER DESERT: ON",
                       gen_btn.rect.right + 12 + 70, gen_btn.rect.top + 20,
                       140, 40,["Menu"], btn_font=toggle_font, hover_font=toggle_hover_font)

pb_w      = int(startgame_btn.rect.width / 3.1)
pb_h      = startgame_btn.rect.height
pb_gap    = 5
scx, scy  = startgame_btn.rect.centerx, startgame_btn.rect.centery
player_btns = [
    Button("2P", scx - (pb_w + pb_gap), scy, pb_w, pb_h, ["Menu"]),
    Button("3P", scx,                    scy, pb_w, pb_h, ["Menu"]),
    Button("4P", scx + (pb_w + pb_gap),  scy, pb_w, pb_h, ["Menu"]),
]

throw_dice_btn = Button("", WIDTH // 1.4, HEIGHT // 1.1, 240, 100, ["FirstRound","ReadyToRoll", "PlayerTurn"])

show_player_selection = False

#Team colors
color_team_1 = (209, 45, 0) #Red
color_team_2 = (255, 255, 255) #White
color_team_3 = (19, 62, 207) #Blue
color_team_4 = (43, 179, 20) #Green

class InfoText:
    def __init__(self, label, cx, cy, w, h, player, visible_in_game_state=list, btn_font=None, color="white"):
        self.label       = label
        self.rect        = pygame.Rect(int(cx - w // 2), int(cy - h // 2), int(w), int(h))
        self.font        = btn_font if btn_font is not None else font
        self.color       = color
        self.visible_in_game_state = visible_in_game_state
        self.player = player
 
    def draw(self, mouse_pos, gamestate):
        if str(gamestate) in self.visible_in_game_state:
            #c = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
            self.font = hover_font if self.rect.collidepoint(mouse_pos) else font
            #pygame.draw.rect(screen, c, self.rect, border_radius=8)
            lbl = self.font.render(self.label, True, BTN_TEXT)
            screen.blit(lbl, lbl.get_rect(center=self.rect.center))

