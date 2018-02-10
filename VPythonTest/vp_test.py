from vpython import *

def keyInput(evt):
    s = evt.key
    if evt.key == "up":
    	scene.camera.pos = vector(scene.camera.pos.x, scene.camera.pos.y + 0.5, scene.camera.pos.z)
    elif evt.key == "down":
    	scene.camera.pos = vector(scene.camera.pos.x, scene.camera.pos.y - 0.5, scene.camera.pos.z)
    elif evt.key == "left":
    	scene.camera.pos = vector(scene.camera.pos.x - 0.5, scene.camera.pos.y, scene.camera.pos.z)
    elif evt.key == "right":
    	scene.camera.pos = vector(scene.camera.pos.x + 0.5, scene.camera.pos.y, scene.camera.pos.z)

def spawnCubeAt(x, y, z, l, w, h, c):
	box1 = box(pos = vector(x, y, z), length = l, width = w, height = h, color = c)
	return box1

def init_floor( x , y ):
    for i in range(0,x):
        for j in range(0,y):
            spawnCubeAt(i, 0, j, 1, 1, 1, color.green)

def main():
	scene.bind('keydown', keyInput)
	init_floor(10, 10)

main()