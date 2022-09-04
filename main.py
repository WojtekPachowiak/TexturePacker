import sys
import os
import pygame as pg
from pygame.locals import *
from globals import Color, Globals as g
from image import EditableImage
from sound import Sound
from utils import Func

pg.init() 
from UI import Button

fpsClock = pg.time.Clock()

g.SCREEN = pg.display.set_mode((g.WIDTH, g.HEIGHT))

# button = Button(g.WIDTH/4, g.HEIGHT/2, g.WIDTH/4, g.HEIGHT /
#                 8, "Sieema", Func(Sound.beep))



def drop_img(e: pg.event.Event):
    _, file_ext = os.path.splitext(e.file)
    if file_ext in [".jpg", ".png"]:
        editable_images.append(
            EditableImage(pg.image.load(e.file), pg.mouse.get_pos())
        )


clock = pg.time.Clock()
editable_images :list[pg.Surface] = []
event_handlers = []

# Game loop.
while True:
    clock.tick(30)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.DROPFILE:
            drop_img(event)

        for h in event_handlers:
            h.handle_event(event)

        for img in editable_images: 
            img.handle_event(event)

    g.SCREEN.fill(Color.GRAY)

    # button.draw()
    for img in editable_images: 
      img.draw(g.SCREEN)

    pg.display.flip()
    fpsClock.tick(g.FPS)
