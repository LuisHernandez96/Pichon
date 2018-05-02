# Pichon
Pichón is a programming language created with the purpose of helping people understand the basic concepts of programming, such as conditions, loops, functions, etc., in a fun way by giving the user the ability to build a basic 3D environment and be able to move around it while trying to achieve an objective.

## Requirements
The following languages and libraries need to be installed in order to run Pichón
Python 3 or above (https://www.python.org/download/releases/3.0/)
Vpython (http://vpython.org)
Tkinter (https://docs.python.org/3/library/tkinter.html)
PLY (http://www.dabeaz.com/ply/)


## Getting Pichón
Pichón can be downloaded from https://github.com/LuisHernandez96/Pichon as a .zip file and be extracted at any location the user wants.
Running Pichón
Now that Pichón has been downloaded, you only need to run the following command from inside Pichón’s directory.

> python pichon.py

Pichón basic IDE should now appear on screen.


## My first program
Below you can find the source code of a simple Pichón program which you can copy and paste into the Code Editor section to see what it produces.

```
FUNCTIONS{
  function void moveCircleRight(int n){
    int i;
    int j;
    for(i = 0; i < 4; i = i + 1){
      for(j = 0; j < n; j = j + 1){
        forward();
      };
      turnRight();
    };
  }
}

ENVIRONMENT{
  start(2, 2, 2);
  goal(2, 2, 2);
  spawnObject(sphere, 6, 2, 2);
  spawnObject(sphere, 6, 2, 6);
  spawnObject(sphere, 2, 2, 6);
  spawnObject(sphere, 4, 2, 2);
}

MOVEMENT{
  moveCircleRight(4);
}
```

What’s going on?
First we can see the FUNCTIONS section. This section is where you can define your own functions to be executed whenever you need. Right now, there’s a moveCircleRight function already defined that basically moves you forward n times and then turn right, and repeats that 4 times.

Next, the ENVIRONMENT section is where you can define what will be in the environment. The start and goal functions are used to define where the player will start and where the player should be at the end of the program execution. Then, 4 spheres are created at the given coordinates. In Pichón, sphere objects act as collectibles that the user needs to get before reaching the goal, and cube objects act as obstacle that block some of the player’s movements.

And finally, the MOVEMENT section is where you define how you will move around your masterpiece! You can see that here the moveCircleRight function is the only code being called, which manages to pick up all the spheres defined in ENVIRONMENT and reach the goal position. In the end, if you have picked up all the spheres and reached the goal, a message will appear to congratulate you on your feat!
