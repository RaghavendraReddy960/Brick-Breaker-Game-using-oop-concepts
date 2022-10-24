from colorama import *
import numpy as np
import time
import os
from datetime import datetime
from function import *
from config import *

# Initialize the scene
scene = Scene(SC_LENGTH, SC_WIDTH, SC_FULLWIDTH)
# Put Paddle at predefined initial position
paddle = Paddle(PADDLE_LENGTH, PADDLE_WIDTH)
paddle.setPos(scene, PADDLE_INIT_X, PADDLE_INIT_Y)
# Put Paddle at predefined initial position
ball = Ball(1, 1)
ball.setPos(scene, PADDLE_INIT_X-2, PADDLE_INIT_Y)
getinp = Get()

while True:
    input = input_to(getinp)
    os.system('clear')
    #generatescene(scene)
    
    print(scene.displayScene(datetime.now()))
    #sys.exit()
    if input is not None:
        if input in ALLOWED_INPUTS:
            if input in ['a', 'A']:
                paddle.moveleft(scene)
            elif input in ['d', 'D']:
                paddle.moveright(scene)
                
        #move ball
#        ball.moveBox(scene,1, 3)
#        if ball.x <= 0: # Left wall
#            ball.xDir *= -1
#        elif ball.x + 1 >= SC_WIDTH: # Right wall
#            ball.xDir *= -1
#        elif ball.y <= 0: # Top wall
#            ball.yDir *= -1
#        elif ball.y + 1 >= SC_LENGTH: # If crash Bottom wall
#            sys.exit()        
    
        if input == 'q':
            os.system('clear')
            sys.exit()