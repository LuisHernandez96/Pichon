from vpython import *


def spawnCubeAt(x, y, z, l, w, h, c):
    box1 = box(pos=vector(x, y, z), length=l, width=w, height=h, color=c)
    return box1


KEK = spawnCubeAt(0, 1, 0, 1, 1, 1, color.green)


def keyInput(evt):
    s = evt.key
    if evt.key == "up":
        KEK.pos = KEK.pos + KEK.axis
    elif evt.key == "down":
        KEK.pos = KEK.pos - KEK.axis
    elif evt.key == "left":
        KEK.rotate(radians(90), vec(0, 1, 0))
    elif evt.key == "right":
        KEK.rotate(radians(-90), vec(0, 1, 0))


def init_floor(x, y):
    for i in range(0, x):
        for j in range(0, y):
            spawnCubeAt(i, 0, j, 1, 1, 1, color.green)


def rotate_obj(obj, axis, degrees):
    pass


def main():
    scene.bind('keydown', keyInput)
    scene_floor = spawnCubeAt(0, 0, 0, 10, 10, 1, color.green)

    attach_trail(KEK)

main()