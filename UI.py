import pygame
import sys
import math
import numpy as np
import random as rd

WIDTH, HEIGHT = 1200, 730
cx, cy = WIDTH//2, HEIGHT//2
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

BG_COLOR  = (30, 80, 160)
BTN_COLOR = (220, 180, 80)
UNVBLE_BTN_COLOR = (130,130,130)
BTN_HOVER = (240, 200, 100)
BTN_TEXT  = (30, 30, 30)
BOARD = (255, 198, 41)

#Images
#-Tiles
ore_tile = pygame.image.load("images/ore_tile.png").convert_alpha()
sheep_tile = pygame.image.load("images/sheep_tile.png").convert_alpha()
brick_tile = pygame.image.load("images/brick_tile.png").convert_alpha()
wheat_tile = pygame.image.load("images/wheat_tile.png").convert_alpha()
timber_tile = pygame.image.load("images/timber_tile.png").convert_alpha()
desert_tile = pygame.image.load("images/desert_tile.png").convert_alpha()

#-Cards
ore_card = pygame.image.load("images/ore_card.png").convert_alpha()
sheep_card = pygame.image.load("images/sheep_card.png").convert_alpha()
brick_card = pygame.image.load("images/brick_card.png").convert_alpha()
wheat_card = pygame.image.load("images/wheat_card.png").convert_alpha()
timber_card = pygame.image.load("images/timber_card.png").convert_alpha()
general_card = pygame.image.load("images/general_card.png").convert_alpha()

#-Port Icons
ore_icon = pygame.image.load("images/ore_icon.png").convert_alpha()
sheep_icon = pygame.image.load("images/sheep_icon.png").convert_alpha()
brick_icon = pygame.image.load("images/brick_icon.png").convert_alpha()
wheat_icon = pygame.image.load("images/wheat_icon.png").convert_alpha()
timber_icon = pygame.image.load("images/timber_icon.png").convert_alpha()

font        = pygame.font.SysFont(None, 36)
hover_font  = pygame.font.SysFont(None, 38)
toggle_font = pygame.font.SysFont(None, 16)
toggle_hover_font = pygame.font.SysFont(None, 18)
clock       = pygame.time.Clock()


class Button:
    def __init__(self, label, cx, cy, w, h, visible_in_game_state=list, btn_font=None, hover_font=hover_font, color=BTN_COLOR, hover_color=BTN_HOVER, center_offset = None, wrap = False, wrap_width = None):
        self.label       = label
        self.pos         = (cx, cy)
        self.w, self.h   = w, h
        self.rect        = pygame.Rect(int(self.pos[0] - w // 2), int(self.pos[1] - h // 2), int(self.w), int(self.h))
        self.hover_rect  = self.rect.inflate(7,7)
        self.font        = btn_font if btn_font is not None else font
        self.hover_font = hover_font
        self.color       = color
        self.hover_color = hover_color
        self.visible_in_game_state = visible_in_game_state
        self.clickable = False
        self.center_offset = center_offset if center_offset is not None else [0, 0]
        self.wrap = wrap
        self.wrap_width = wrap_width
        self.can_hover = True
        self.border = False
        self.border_color = (99, 47, 3)

    def move_to(self, cx, cy, w=None, h=None):
        self.pos        = (cx, cy)
        if w == None and h == None:
            w, h = self.w, self.h
        self.w, self.h = w, h
        self.rect        = pygame.Rect(int(cx - self.w // 2), int(cy - self.h // 2), int(self.w), int(self.h))
        self.hover_rect  = self.rect.inflate(7,7)

    def draw(self, mouse_pos, gamestate):
        if str(gamestate) in self.visible_in_game_state:
            self.clickable = True


            if self.rect.collidepoint(mouse_pos) and self.can_hover:
                c = self.hover_color
                rect = self.hover_rect
                bg_rect = self.rect.inflate(20,20)
                btn_font_final = self.hover_font 
            else:
                c = self.color
                rect = self.rect
                bg_rect = self.rect.inflate(10,10)
                btn_font_final = self.font
            if self.border == True:
                pygame.draw.rect(screen, self.border_color, bg_rect, border_radius = 8)
            pygame.draw.rect(screen, c, rect, border_radius=8)

            

            label_center = (self.rect.centerx + self.center_offset[0], self.rect.centery + self.center_offset[1])
            if self.wrap:
                max_width = self.wrap_width if self.wrap_width is not None else self.w
                lines = self.wrap_label(self.label, btn_font_final, max_width)
                line_h = btn_font_final.get_linesize()
                top = label_center[1] - (line_h * len(lines)) // 2
                for i, line in enumerate(lines):
                    lbl = btn_font_final.render(line, True, BTN_TEXT)
                    screen.blit(lbl, lbl.get_rect(center=(label_center[0], top + line_h * i + line_h // 2)))
            else:
                lbl = btn_font_final.render(self.label, True, BTN_TEXT)
                screen.blit(lbl, lbl.get_rect(center=label_center))
        else:
            self.clickable = False

    def wrap_label(self, text, btn_font, max_width): #Claude
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if btn_font.size(candidate)[0] <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def draw_icon(self, mouse_pos, gamestate, icon,r):
        if str(gamestate) in self.visible_in_game_state:
            self.clickable = True
            if self.rect.collidepoint(mouse_pos):
                rect = self.hover_rect
                c = self.hover_color
            else:
                c = self.color
                rect = self.rect
            
            pygame.draw.rect(screen, c, rect, border_radius=8)
            icon.draw(mouse_pos, screen,r)
        else:
            self.clickable = False

    def is_clicked(self, mouse_pos):
        if self.clickable:
            return self.rect.collidepoint(mouse_pos)
        


endturn_btn   = Button("END TURN",   WIDTH // 1.1, HEIGHT // 1.1, 180, 50, ["FirstRound", "PlayerTurn"])
startgame_btn = Button("START GAME", WIDTH // 1.3, HEIGHT // 1.3, 180, 50, ["Menu"])
gen_btn       = Button("REGENERATE", WIDTH // 1.3, HEIGHT // 1.5, 180, 50, ["Menu"])
toggle_cd_btn    = Button("CENTER DESERT: ON",
                       gen_btn.rect.right + 12 + 80, gen_btn.rect.top + 20,
                       160, 40,["Menu"], btn_font=toggle_font, hover_font=toggle_hover_font)
toggle_ports_btn = Button("ALTERNATING PORTS: ON",
                          gen_btn.rect.right + 12 + 80, gen_btn.rect.top + 80,
                       160, 40,["Menu"], btn_font=toggle_font, hover_font=toggle_hover_font)

build_btn = Button("BUILD", WIDTH // 1.35, HEIGHT -HEIGHT // 1.1, 160, 50, ["PlayerTurn", "ReadyToRoll"])
trade_btn = Button("TRADE", WIDTH // 1.35+180, HEIGHT -HEIGHT // 1.1, 160, 50, ["PlayerTurn", "ReadyToRoll"])






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
store = (84,84,84) #Store
color_team = [color_team_1, color_team_2, color_team_3, color_team_4, store]

class InfoText:
    def __init__(self, label, cx, cy, w, h, player, visible_in_game_state=list, btn_font=None, color="white"):
        self.label       = label
        self.rect        = pygame.Rect(int(cx - w // 2), int(cy - h // 2), int(w), int(h))
        self.font        = btn_font if btn_font is not None else font
        self.color       = color
        self.visible_in_game_state = visible_in_game_state
        self.player = player
 
    def draw(self, mouse_pos, gamestate, img=None, max_w=50, max_h=50):
        if str(gamestate) in self.visible_in_game_state:
            #c = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
            self.font = hover_font if self.rect.collidepoint(mouse_pos) else font
            #pygame.draw.rect(screen, c, self.rect, border_radius=8)
            lbl = self.font.render(self.label, True, BTN_TEXT)
            screen.blit(lbl, lbl.get_rect(center=self.rect.center))
            if img is not None:
                iw, ih = img.get_size()
                scale = min(max_w / iw, max_h / ih, 1)
                new_w = max(1, int(iw * scale))
                new_h = max(1, int(ih * scale))
                scaled_img = pygame.transform.smoothscale(img, (new_w, new_h))
                screen.blit(scaled_img, lbl.get_rect(center=(self.rect.center[0],self.rect.center[1]+20 )))

class Card:
    def __init__(self, card_img, player,x,y, max_w = 45, max_h = 90):
        self.img = card_img
        self.player = player
        self.color = color_team[player]
        self.x = x
        self.y = y
        
        iw, ih = self.img.get_size()
        scale = min(max_w / iw, max_h / ih, 1)
        new_w = max(1, int(iw * scale))
        new_h = max(1, int(ih * scale))

        self.scaled_card = pygame.transform.smoothscale(self.img, (new_w, new_h))


        self.w_card, self.h_card = self.scaled_card.get_size()
        self.hover_card = pygame.transform.smoothscale(self.scaled_card, (self.w_card*1.1, self.h_card*1.1))
        self.w, self.h = self.w_card*1.1, self.h_card * 1.1
        self.w_bg, self.h_bg = self.w *1.1, self.h*1.1

        self.rect = pygame.Rect(self.x-self.w//2, self.y-self.h//2, int(self.w), int(self.h))
        self.rect_bg = pygame.Rect(self.x-self.w_bg//2, self.y-self.h_bg//2, int(self.w_bg), int(self.h_bg))

        self.hover_rect = self.rect.inflate(10,10)
        self.hover_rect_bg = self.rect_bg.inflate(10,10)
    
    def draw(self, hover):
        if hover:
                rect = self.hover_rect
                rect_bg = self.hover_rect_bg
                card_img = self.hover_card
                blit_pos = (self.x-(self.w_card*1.1)//2,self.y-(self.h_card*1.1)//2)


        else:
                rect = self.rect
                rect_bg = self.rect_bg
                card_img = self.scaled_card
                blit_pos = (self.x-self.w_card//2,self.y-self.h_card//2)

        pygame.draw.rect(screen, (0,0,0), rect_bg, border_radius=10)
        pygame.draw.rect(screen, self.color, rect, border_radius =10)
        
        
        screen.blit(card_img, blit_pos)

        

def drawCards(player_resources, player, card_types, mouse_pos, card_w, card_h, x, y):
    n=0
    spacing= card_w*2
    displace = card_w//3.75
    resource_indexes = ["ore", "sheep", "brick", "wheat", "timber"]
    for resource, amount in player_resources[player].items():
        card_type_index = resource_indexes.index(resource)
        if amount>0:
            offset = []
            amountShown = 0
            for i in range(amount):
                if i >= 3: #Max three cards drawn
                    break
                amountShown+=1
                offset.append((i*displace, i*displace))
            pile_hover = []
            pile = []

            for i in range(amountShown-1, -1, -1):
                card = Card(card_types[card_type_index], player, x+n*spacing+offset[i][0], y//0.93-offset[i][0], card_w, card_h)
                if card.rect.collidepoint(mouse_pos):
                    hover = True
                else:
                    hover = False
                pile_hover.append(hover)
                pile.append(card)
            #Significant hover index
            last_true_idx = next((i for i in range(len(pile_hover) - 1, -1, -1) if pile_hover[i]), None)
            for card in pile:
                if pile.index(card) == last_true_idx:
                    card.draw(True)
                else:
                    card.draw(False)
            amount_label = Button(str(amount),x+n*spacing, y+40, card_w*0.9, card_w*0.9, ["ReadyToRoll", "PlayerTurn"])
            amount_label.draw(mouse_pos, "PlayerTurn")
            n+=1

class PriceLabel:
    def __init__(self, price, x, y,visible_in_game_state, w=230, h=80, color=BTN_COLOR, hover_color=BTN_HOVER,):
        self.price = price
        self.x = x
        self.y = y
        self.w, self.h = w,h
        self.rect        = pygame.Rect(int(self.x - self.w // 2), int(self.y - self.h // 2), int(self.w), int(self.h))
        self.hover_rect  = self.rect.inflate(7,7)
        self.color       = color
        self.hover_color = hover_color
        self.visible_in_game_state = visible_in_game_state
        self.clickable = False

    def draw(self, mouse_pos, gamestate, card_types):
        if str(gamestate) in self.visible_in_game_state:
            self.clickable = True
            if self.rect.collidepoint(mouse_pos):
                rect = self.hover_rect
                c = self.hover_color
                hover=True
            else:
                c = self.color
                rect = self.rect
                hover=False

            pygame.draw.rect(screen, c, rect, border_radius=8)
            resource_indexes = ["ore", "sheep", "brick", "wheat", "timber"]
            cardAmount = len(self.price)
            spacing = (230 - cardAmount*30)//(cardAmount+1)
            i=0
            for priceCard in self.price:
                i+=1
                card_type_index = resource_indexes.index(priceCard)
                card_w = 30
                card = Card(card_types[card_type_index], 4, (self.x-self.w//2-15)+(spacing+card_w)*i, self.y, card_w, 60)
                card.draw(hover)
        else:
            self.clickable = False

    def is_clicked(self, mouse_pos):
            if self.clickable:
                return self.rect.collidepoint(mouse_pos)

class TradeLabel(PriceLabel):
    def __init__(self, price, x, y, visible_in_game_state, w=230, h=80, color=BTN_COLOR, hover_color=BTN_HOVER, trade_possible=True):
        super().__init__(price, x, y, visible_in_game_state, w, h, color, hover_color)
        self.trade_possible = trade_possible

    def draw(self, mouse_pos, gamestate, card_types):
        self.rect        = pygame.Rect(int(self.x - self.w // 2), int(self.y - self.h // 2), int(self.w), int(self.h))
        self.hover_rect  = self.rect.inflate(7,7)

        if str(gamestate) in self.visible_in_game_state:
            self.clickable = True
            if self.rect.collidepoint(mouse_pos):
                rect = self.hover_rect
                c = self.hover_color
                hover=True
            else:
                c = self.color
                rect = self.rect
                hover=False

            pygame.draw.rect(screen, c, rect, border_radius=8)
            resource_indexes = ["ore", "sheep", "brick", "wheat", "timber", "general"]
            cardAmount = len(self.price)
            card_h = self.h//1.4
            card_w = card_h//2
            
            spacing = (230 - cardAmount*card_w)//(cardAmount+2)
            i=0
            for priceCard in self.price:
                i+=1
                card_type_index = resource_indexes.index(priceCard)
                card = Card(card_types[card_type_index], 4, (self.x-self.w//2-15)+(spacing+card_w)*i, self.y, card_w, card_h)
                card.draw(hover)
        else:
            self.clickable = False

def tradeMenuGen(player_trades, player_resources, player, trade_costs_display_order, ):
    available_trades = []                
    player_trades[player-1] = sorted(player_trades[player-1], key=trade_costs_display_order.index) #Sorts available trades in menu
    trades_len = len(player_trades[player-1])
    if trades_len < 5:
        label_h = 80
        fontSize = 25
    else:
        label_h  = 80 //(1+(trades_len-4)/5.5) #Scales down label_h when trades exceed 5, to fit on screen
        fontSize = 25//(1+(trades_len-4)/20)
    
    trade_with_others_font = pygame.font.SysFont(None, int(fontSize))
    trade_with_others_hover_font = pygame.font.SysFont(None, int(fontSize*1.1))
    
    trade_with_others_btn = Button("TRADE WITH PLAYERS", WIDTH//1.5, HEIGHT//4.3, 230, label_h, ["PlayerTurn"], trade_with_others_font, trade_with_others_hover_font)
    i=0
    for trade in player_trades[player-1]:
        resource = trade[0]
        color = (0,0,120)
        trade_possible = True
        if resource == "general":
            resources_needed = max(player_resources[player-1].values())
        else:
            resources_needed = player_resources[player-1][str(resource)]
        if  resources_needed >= len(trade):
            color = BTN_COLOR
            trade_possible = True
        else:
            color = UNVBLE_BTN_COLOR
            trade_possible = False
        available_trades.append(TradeLabel(trade, WIDTH //1.5, HEIGHT//4.3+(i+1)*(label_h*1.15),["ReadyToRoll", "PlayerTurn"], 230, label_h, color, trade_possible=trade_possible))
        i+=1
    return trade_with_others_btn, available_trades

def tradeWithPlayer(active_player, trade_partner, player_resources):
    trade_with_others_font = pygame.font.SysFont(None, int(25))
    trade_with_others_hover_font = pygame.font.SysFont(None, int(25*1.1))
    confirm_trade_btn = Button("CONFIRM", WIDTH//1.5+230*1.1, HEIGHT//4.3, 230, 80, ["PlayerTurn"], trade_with_others_font, trade_with_others_hover_font)
    ap_gets_btn = Button(f"Player {active_player} GETS:", WIDTH//1.5, HEIGHT//2.1, 230, 260, ["PlayerTurn"],trade_with_others_font, trade_with_others_hover_font)
    tp_gets_btn = Button(f"Player {trade_partner} GETS:", WIDTH//1.5+230*1.1, HEIGHT//2.1, 230, 260, ["PlayerTurn"],trade_with_others_font, trade_with_others_hover_font)
    ap_gets_btn.can_hover = False
    tp_gets_btn.can_hover = False
    ap_gets_btn.border = True
    tp_gets_btn.border = True
    ap_gets_btn.center_offset[1] = -100
    tp_gets_btn.center_offset[1] = -100

    tp_card_area_rect = pygame.Rect(WIDTH//1.505-230//2, HEIGHT//1.45, 500, 85)
    tp_fg_rect = pygame.Rect(WIDTH//1.505-230//2+10, HEIGHT//1.45, 480, 75)
    

    return confirm_trade_btn, ap_gets_btn, tp_gets_btn, tp_card_area_rect, tp_fg_rect