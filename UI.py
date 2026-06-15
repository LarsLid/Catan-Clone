import pygame
import sys
import math
import numpy as np
import random as rd

WIDTH, HEIGHT = 1200, 730
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BG_COLOR  = (30, 80, 160)
BTN_COLOR = (220, 180, 80)
BTN_HOVER = (240, 200, 100)
BTN_TEXT  = (30, 30, 30)
BOARD = (255, 198, 41)

font        = pygame.font.SysFont(None, 36)
toggle_font = pygame.font.SysFont(None, 20)
clock       = pygame.time.Clock()


class Button:
    def __init__(self, label, cx, cy, w, h, visible_in_game_state=list, btn_font=None, color=BTN_COLOR, hover_color=BTN_HOVER):
        self.label       = label
        self.rect        = pygame.Rect(int(cx - w // 2), int(cy - h // 2), int(w), int(h))
        self.font        = btn_font if btn_font is not None else font
        self.color       = color
        self.hover_color = hover_color
        self.visible_in_game_state = visible_in_game_state

    def draw(self, mouse_pos, gamestate):
        if str(gamestate) in self.visible_in_game_state:
            c = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
            pygame.draw.rect(screen, c, self.rect, border_radius=8)
            lbl = self.font.render(self.label, True, BTN_TEXT)
            screen.blit(lbl, lbl.get_rect(center=self.rect.center))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


endturn_btn   = Button("END TURN",   WIDTH // 1.3, HEIGHT // 1.1, 180, 50, ["FirstRound", "PlayerTurn"])
startgame_btn = Button("START GAME", WIDTH // 1.3, HEIGHT // 1.3, 180, 50, ["Menu"])
gen_btn       = Button("REGENERATE", WIDTH // 1.3, HEIGHT // 1.5, 180, 50, ["Menu"])
toggle_btn    = Button("CENTER DESERT: ON",
                       gen_btn.rect.right + 12 + 70, gen_btn.rect.top + 20,
                       140, 40,["Menu"], btn_font=toggle_font)

pb_w      = int(startgame_btn.rect.width / 3.1)
pb_h      = startgame_btn.rect.height
pb_gap    = 5
scx, scy  = startgame_btn.rect.centerx, startgame_btn.rect.centery
player_btns = [
    Button("2P", scx - (pb_w + pb_gap), scy, pb_w, pb_h, ["Menu"]),
    Button("3P", scx,                    scy, pb_w, pb_h, ["Menu"]),
    Button("4P", scx + (pb_w + pb_gap),  scy, pb_w, pb_h, ["Menu"]),
]

show_player_selection = False
