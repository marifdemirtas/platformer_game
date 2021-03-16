import os

WIDTH = 480 * 2
HEIGHT = 360 * 2
FPS = 30

TITLE = "HEY"

FOLDER = "/home/marif/Documents/platformer"

SPRITES = os.path.join(FOLDER, "assets/sprites")


class Player:
    ACC = .5
    FR = -.08
    GRAV = .8
