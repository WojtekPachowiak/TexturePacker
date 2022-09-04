

from enum import Enum, Flag, auto
from typing import Tuple
from globals import Color
import pygame as pg

from utils import CenteredRect, draw_broder


class EditableImage:

    class Selection:
        color = Color.ORANGE
        thickness = 5

    class State(Flag):
        DRAGGED = auto()
        SCALED = auto()
        IDLE = auto()

    def __init__(self, image: pg.Surface, pos: Tuple[int, int]):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.selected = True
        self.state = EditableImage.State.IDLE

        t = EditableImage.Selection.thickness
        self.scale_handles = pg.Surface(
            (t+2, t+2))

        r = self.rect
        self.scale_handles_pos: list[Tuple] = [
            (r.topleft[0] - t-1, r.topleft[1] - t-1),
            (r.midtop[0] - t/2, r.midtop[1] - t-1),
            (r.topright[0]+1, r.topright[1]-t-1),
            (r.midright[0] +1, r.midright[1]-t/2),
            (r.bottomright[0]+0, r.bottomright[1]+0),
            (r.midbottom[0]-t/2, r.midbottom[1]+0),
            (r.bottomleft[0]-t, r.bottomleft[1]+0),
            (r.midleft[0]-t, r.midleft[1]-t/2)
            ]
        assert len(self.scale_handles_pos) == 8

    def draw(self, screen):
        # blit image to main screen
        screen.blit(self.image, self.rect)
        if(self.selected):
            # draw selection borders
            draw_broder(screen, EditableImage.Selection.color,
                        self.rect, EditableImage.Selection.thickness)
            # draw scale handles
            for pos in self.scale_handles_pos:
                screen.blit(self.scale_handles, pg.Rect(
                    pos, (EditableImage.Selection.thickness, EditableImage.Selection.thickness)))


    def flip(self, horizontal: bool, vertical: bool):
        self.image=pg.transform.flip(self.image, horizontal, vertical)

    def drag(self):
        delta=pg.mouse.get_rel()
        new_pos=self.rect.topleft[0] + \
            delta[0], self.rect.topleft[1] + delta[1]
        self.rect.move_ip(new_pos)

    class ScaleMode(Enum):
        TOPLEFT=auto()
        TOPRIGHT=auto()
        BOTTOMLEFT=auto()
        BOTTOMRIGHT=auto()
        RIGHT=auto()
        LEFT=auto()
        TOP=auto()
        BOTTOM=auto()
        UNIFORM=auto()
        HORIZONTAL=auto()
        VERTICAL=auto()

    def scale(self, mode: ScaleMode):
        # self.rect.update()
        # self.rect.inflate_ip()
        pass

    def handle_event(self, e):
        s=EditableImage.State

        if (e.type == pg.MOUSEBUTTONDOWN and
                self.rect.collidepoint(e.pos)):
            # flip
            if e.button == pg.BUTTON_MIDDLE:
                self.flip(True, False)
            elif e.button == pg.BUTTON_RIGHT:
                # prepare for dragging
                if (self.state != s.DRAGGED):
                    self.state=s.DRAGGED
                # drag if already prepared
                else:
                    self.drag()
            # select
            elif e.button == pg.BUTTON_LEFT:
                self.selected=True
        # deselect
        elif (e.type == pg.MOUSEBUTTONDOWN and
                not self.rect.collidepoint(e.pos)):
            self.selected=False
