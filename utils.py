
from types import NoneType
from typing import Callable, Tuple
import pygame as pg

class Cursor:
    def set_cursor_hand():
        c = pg.cursors.Cursor(pg.SYSTEM_CURSOR_HAND)
        pg.mouse.set_cursor(c)

    def set_cursor_arrow():
        c = pg.cursors.Cursor(pg.SYSTEM_CURSOR_ARROW)
        pg.mouse.set_cursor(c)


class Func:
    def __init__(self, func: Callable, args: Tuple = None):
        assert isinstance(func, Callable)
        assert isinstance(args, (Tuple, NoneType))
        self.func = func
        self.args = args

    def evoke(self):
        if self.args == None or len(self.args) == 0:
            self.func()
        else:
            self.func(*self.args)


def draw_broder(screen, color, rect, thickness):
    t = thickness
    pg.draw.rect(
        screen,
        color,
        (rect.left-t, rect.top-t, rect.width+t*2, rect.height+t*2),
        t
    )


# class Anchor(Enum):
#     TOPLEFT = auto()
#     CENTER = auto()


class CenteredRect(pg.Rect):
    def __init__(self, *args):
        if len(args) == 4:
            self.init1(*args)
        else:
            self.init2(*args)
        
    
    def init1(self, x, y, width, height):
        super().__init__(x-width/2, y-height/2, width, height)

    def init2(self, pos:Tuple[int,int], size:Tuple[int,int]):
        super().__init__((pos[0]-size[0]/2, pos[1]-size[1]/2), size)

    
    


    # def anchor_change(self, _from: Anchor, to: Anchor):
    #     '''changes to another anchor's position'''
    #     self.anchor = to
    #     val = getattr(self, Rect.anchor_to_attr(_from))
    #     setattr(self, Rect.anchor_to_attr(to), val)

    # def anchor_to_attr(anchor: Anchor) -> str:
    #     match anchor:
    #         case Anchor.TOPLEFT:
    #             return "topleft"
    #         case Anchor.CENTER:
    #             return "center"
    #         case _:
    #             raise Exception("Case not implemented!")

