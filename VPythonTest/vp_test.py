from vpython import *

def init_floor( x , y ):
    for i in range(0,x):
        for j in range(0,y):
            box(pos=vec(i, 0, j), radius=1, color=color.green)

def main():
    init_floor(10, 10)