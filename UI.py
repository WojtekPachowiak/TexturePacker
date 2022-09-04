import time
import pygame as pg
from enum import Enum, auto
from globals import Color, Globals as g
from threading import Thread

from utils import CenteredRect, Func



class Button:
    class State(Enum):
        HOVERED_OVER = auto()
        PRESSED = auto()
        IDLE = auto()

    background_color = Color.BLUE

    font_color = Color.BLACK
    font = pg.font.SysFont(None, 32)


    def __init__(self, x, y, width, height, text, func:Func = None):
        self.text = text
        self.rect = CenteredRect(x, y, width, height)
        self.surf = pg.Surface(self.rect.size)
        self.surf.fill(Button.background_color)

        # blit text on button' surf
        text_surf = Button.font.render(text, True, Button.font_color)
        text_rect = text_surf.get_rect(center=(width/2, height/2))
        self.surf.blit(text_surf, text_rect)

        #preallocate different surface's color variants
        hovered_over = self.surf.copy()
        hovered_over.fill((32,32,32), special_flags=pg.BLEND_RGB_ADD)
        pressed = self.surf.copy()
        pressed.fill((64,64,64), special_flags=pg.BLEND_RGB_ADD)
        self.surf_variants = {
            Button.State.HOVERED_OVER : hovered_over,
            Button.State.PRESSED : pressed,
            Button.State.IDLE : self.surf
            }

        self.state = Button.State.IDLE

        self.func = func

    def draw(self):
        g.SCREEN.blit(self.surf, self.rect)

    def handle_event(self, event: pg.event.Event):
        
        
        state = None
        S = Button.State

        #check press
        if event.type == pg.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(pg.mouse.get_pos()):
            state = S.PRESSED

        #check hover over
        elif self.rect.collidepoint(pg.mouse.get_pos()):
            state = S.HOVERED_OVER    

        #button is idle
        else:
            state = S.IDLE

        match state:
            case S.IDLE:
                self.surf = self.surf_variants[state]
            case S.PRESSED:
                self.evoke_func()
                Thread(
                    target=self.blink_surf_variant, 
                    args=(0.3, self.state, state,)
                    ).start()
            case S.HOVERED_OVER:
                self.surf = self.surf_variants[state]
            case _:
                raise Exception("Case not implemented!")

        #update state
        self.state = state
        assert isinstance(self.surf, pg.Surface)


    def evoke_func(self):
        if (self.func != None):
            self.func.evoke()

    # def lighten_button(self, seconds):
    #     tmp = self.surf.copy()
    #     self.surf.fill(Button.press_highlight, special_flags=pg.BLEND_RGB_ADD)
    #     time.sleep(seconds)
    #     self.surf = tmp

    # def lighten_button(self):
    #     self.surf.fill(Button.press_highlight, special_flags=pg.BLEND_RGB_ADD)

    # def darken_button(self, seconds=-1):
    #     tmp = self.surf.copy()
    #     self.surf.fill(Button.press_highlight,
    #                    special_flags=pg.BLEND_RGB_SUBTRACT)
    #     if (seconds != -1):
    #         time.sleep(seconds)
    #     self.surf = tmp

    def blink_surf_variant(self, seconds, _from, to):
        self.surf = self.surf_variants[to]
        time.sleep(seconds)
        self.surf = self.surf_variants[_from]
