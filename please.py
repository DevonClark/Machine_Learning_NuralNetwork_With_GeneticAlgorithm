import pygame as p
import math as m
import random
import numpy as np

# Switch between simulation and game mode
GAME_MODE = True      

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Screen parameters.
screenWidth = 700
screenHeight = 500

# Target parameters
targWidth = 20
targHeight = 30

maxTargets = 10                        

# Target control, percent chance of dropping bomb
launchBomb = 3

# Target move choices.
noMove = 0
left = -1
right = 1


def deg2Rad(deg):
    rad = (deg/180.0)*m.pi
    return rad

def getDist(x0, y0, x1, y1):
    dist = m.sqrt((x0 - x1)**2 + (y0 - y1)**2)
    return dist

def collideTarget(bx, by, bRad, tx, ty, tw, th):
    collision = False
    if ((bx >= tx-tw/2-bRad) and (bx <= (tx+tw/2+bRad))) and ((by >= ty-th/2-bRad) and (by <= (ty+th/2+bRad))):
        collision = True
    return collision

def collideBomb(bx, by, bRad, Bx, By, Brad):
    collision = False
    myDist = getDist(bx, by, Bx, By)
    if (myDist < (bRad + Brad)):
        collision = True
    return collision

class bullet:
    def __init__(self, x0, y0, heading0):
        self.x = x0
        self.y = y0
        self.radius = 5
        self.heading = heading0
        self.velocity = 20
        self.exists = True
        self.hit = False
        return
    
    def drawMe(self, s):
        if (self.exists == True):
            if (self.hit == False):
                if (GAME_MODE):
                    p.draw.circle(s, GREEN, [int(self.x), int(self.y)], self.radius, 1)
            else:
                self.explodeMe(s)
        return
    
    def moveMe(self):
        angRad = deg2Rad(self.heading)
        bX = self.x + self.velocity*m.cos(angRad)
        bY = self.y + self.velocity*m.sin(angRad)
        if ((bX > 0) and (bX < screenWidth))and((bY > 0) and (bY < screenHeight)):
            self.x = bX
            self.y = bY
        else:
            self.exists = False              
        return
    
    def doIExist(self):
        return self.exists
    
    def explodeMe(self, s):
        if (GAME_MODE):
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius-4, 1)
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius, 1)
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius+4, 1)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+6, 1)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+9, 1)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+11, 1)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+13, 1)
        
        self.hit = False
        self.exists = False
        return
    
class bomb:
    def __init__(self, x0, y0):
        self.x = x0
        self.y = y0
        self.radius = 7
        self.heading = 90
        self.velocity = 4
        self.exists = True
        self.hit = False
        return
    
    def drawMe(self, s):
        if (self.exists == True):
            if (self.hit == False):
                if (GAME_MODE):
                    p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius, 0)
            else:
                self.explodeMe(s)
        return
    
    def moveMe(self):
        angRad = deg2Rad(self.heading)
        bX = self.x + self.velocity*m.cos(angRad)
        bY = self.y + self.velocity*m.sin(angRad)
        if ((bX > 0) and (bX < screenWidth))and((bY > 0) and (bY < screenHeight)):
            self.x = bX
            self.y = bY
        else:
            self.exists = False              
        return
    
    def doIExist(self):
        return self.exists
    
    def explodeMe(self, s):
        if (GAME_MODE):
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius-4, 1)
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius, 0)
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius+4, 1)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+6, 0)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+9, 1)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+11, 0)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+13, 1)
        
        self.hit = False
        self.exists = False
        return

class target:
    def __init__(self, x0, y0, heading0):
        self.x = x0
        self.y = y0
        self.width = targWidth
        self.height = targHeight
        self.heading = heading0
        self.velocity = 1
        self.exists = True
        self.hitCount = 0
        self.directionInc = noMove
        self.moveSteps = 0
        return
    
    def getBombBay(self):
        bombBayX = self.x
        bombBayY = self.y + self.height
        return bombBayX, bombBayY
    
    def drawMe(self, s):
        if (self.exists == True):
            if (self.hitCount < 50):
                if (GAME_MODE):
                    p.draw.rect(s, RED, [self.x - self.width/2,self.y - self.height/2, self.width, self.height], 2)
            else:
                self.explodeMe(s)
        return
    
    def explodeMe(self, s):
        if (GAME_MODE):
            p.draw.rect(s, YELLOW, [self.x - self.width/8, self.y - self.height/8, self.width/4, self.height/4], 2)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], int(self.width/8), 1)
            p.draw.rect(s, ORANGE, [self.x - self.width/4, self.y - self.height/4, self.width/2, self.height/2], 2)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], int(self.width/4), 1)
            p.draw.rect(s, GREEN, [self.x - self.width/2, self.y - self.height/2, self.width, self.height], 2)
            p.draw.circle(s, GREEN, [int(self.x), int(self.y)], int(self.width/2), 1)
            p.draw.rect(s, GREEN, [self.x - self.width, self.y - self.height, self.width*2, self.height*2], 2)
            p.draw.circle(s, GREEN, [int(self.x), int(self.y)], int(self.width * 2), 1)
        
        self.exists = False
        
        return
        
    def what2Do(self, closeTargX, targWidth, turretX, inc):

        myMove = noMove
        # Here we want to move left.
        if (turretX < self.x):
            if (closeTargX < self.x):
                if ((self.x - inc) > (closeTargX + targWidth)):
                    myMove = left
                else:
                    myMove = noMove
            else:
                myMove = left
        # No move.        
        elif (turretX == self.x):
            myMove = noMove
        # Move to the right.    
        elif (turretX > self.x):
            if (closeTargX > self.x):
                if ((self.x + inc) < (closeTargX - targWidth)):
                    myMove = right
                else:
                    myMove = noMove
            else:
                myMove = right
                
        return myMove
        
        
    
    def moveMe(self, inc):
        self.x = self.x + inc
        if (self.x < self.width):  
            self.x = self.width
        elif (self.x > (screenWidth - self.width)):
            self.x = screenWidth - self.width
            
        return
    
    def doIExist(self):
        return self.exists
    
class turret:
   def  __init__(self, x0, y0, rad0):
        self.x = x0
        self.y = y0
        self.exists = True
        self.hitCount = 0
        self.rad = rad0
        self.leftLimit = 3*rad0
        self.rightLimit = screenWidth - (3*rad0)
        self.gunLen = rad0*2
        self.gunAngle = 270
        self.gunTipX = 0
        self.gunTipY = 0      
        return
    
   def drawMe(self, s):
       if (self.exists == True):
           if (self.hitCount < 7):
               if (GAME_MODE):
                   p.draw.circle(s, WHITE, [self.x, self.y], self.rad, 1)
               angRad = deg2Rad(self.gunAngle)
               self.gunTipX = self.x + self.gunLen*m.cos(angRad)
               self.gunTipY = self.y + self.gunLen*m.sin(angRad)
               if (GAME_MODE):
                   p.draw.line(s, WHITE, [self.x, self.y], [self.gunTipX, self.gunTipY], 1)
           else:
               self.explodeMe(s)
       return
        
       
   def rotateMe(self, inc):
       self.gunAngle = self.gunAngle + inc
       if (self.gunAngle >= 360):
           self.gunAngle = 0
       elif (self.gunAngle < 0):
           self.gunAngle = 359
       return
   
   def moveMe(self, inc):
       self.x = self.x + inc
       if (self.x < self.leftLimit):
           self.x = self.leftLimit
       elif (self.x > self.rightLimit):
           self.x = self.rightLimit
       self.y = self.y
   
   def getGunTip(self):
       x = self.gunTipX
       y = self.gunTipY
       
       return x, y
   
   def getGunAngle(self):
       return self.gunAngle
   
   def explodeMe(self, s):
       if (GAME_MODE):
           p.draw.circle(s, RED, [int(self.x), int(self.y)], self.rad-4, 0)
           p.draw.circle(s, RED, [int(self.x), int(self.y)], self.rad, 0)
           p.draw.circle(s, RED, [int(self.x), int(self.y)], self.rad+4, 0)
           p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.rad+6, 0)
           p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.rad+9, 0)
           p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.rad+11, 0)
           p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.rad+13, 0)
        
       self.exists = False
       return
   
def learnGame(neuralNet = None, neuron_number = None, nb_layers = None):
    

    # Count the number of game loops.
    loopcount = 0
    
    # Game stats
    bulletsShot = 0
    bulletHits = 0
    bombsShotDown = 0
    targetsKilled = 0
    frame = 0
    
    # Initialize random.
    random.seed()
    
    # Set the width and height of the screen [width, height] .
    size = (screenWidth, screenHeight)
    
    # Set up screen and whatnot.
    screen = None
    if (GAME_MODE):
        p.init()
        screen = p.display.set_mode(size)
        p.display.set_caption("learnGame()")
    
    # Turret postion.
    turrX = (int)(screenWidth/2)
    turrY = screenHeight - 50
    # Create turret
    t = turret(turrX, turrY, 20)
    
    # Create the targets.
    targets = []
    
    if (maxTargets < 1):
        print("Gun Training")
    elif (maxTargets == 1):
        myX = int(screenWidth/2)
        myY = 20
        myTarget = target(myX, myY, 90)
        targets.append(myTarget)
    else:
        for j in range(maxTargets):
            if (j == 0):
                myX = 20
                myY = 20
                targXInc = int((screenWidth - 40)/(maxTargets-1))
                
            else:
                myX = myX + targXInc
                myY = 20
                
            myTarget = target(myX, myY, 90)
            targets.append(myTarget)
    
    # Create bullet array.
    bullets = []
    
    # Create a bomb array.
    bombs = []
    
    # Loop until the user clicks the close button.
    running = True 
    
    # Used to manage how fast the screen updates
    clock = p.time.Clock()

    Rand_BombX = np.random.randint(0, screenWidth)
    closeestTarget = distance(targets, t)
    args = np.array([t.x, closeestTarget.x, Rand_BombX])

    
    neuralNet.build(args, neuron_number, nb_layers)
    # -------- Main Program Loop -----------
    while running:
        # --- Main event loop
        
        # If playing a game, process keystrokes to control the
        # turret.
        if (GAME_MODE):
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
        
            """ Check for keyboard presses. """
            key = p.key.get_pressed()
            
            if (key[p.K_ESCAPE] == True): 
                running = False
            
            # Actions that the turret can take.  The
            # user controls this, or a smart controller
            # can control these.
            if(neuralNet == None):
                if (key[p.K_UP] == True): 
                    t.moveMe(1)
                if (key[p.K_DOWN] == True): 
                    t.moveMe(-1)
                if (key[p.K_LEFT] == True): 
                    t.rotateMe(-1)
                if (key[p.K_RIGHT] == True): 
                    t.rotateMe(1)
                if (key[p.K_SPACE] == True):
                    gx, gy = t.getGunTip()
                    ang = t.getGunAngle()
                    bullets.append(bullet(gx, gy, ang))
                    bulletsShot = bulletsShot + 1
            else:

                if(frame > 0):
                    if(len(bombs) > 1):
                        update_targ = distance(targets, t)
                        update_bomb = distance(bombs, t)
                        args = np.array([t.x, update_targ.x, update_bomb.x])
                    else:
                        update_targ = distance(targets, t)
                        args = np.array([t.x, update_targ.x, Rand_BombX])
                
                # print(f"Args at frame {frame}: ",args)

                controls = neuralNet.forward(args)

                best_neuron1 = np.argmax(controls[0])
                best_neuron2 = np.argmax(controls[1])
                best_neuron3 = np.argmax(controls[2])
                best_neuron4 = np.argmax(controls[3])
                best_neuron5 = np.argmax(controls[4])

                print(controls)

                if (controls[0][best_neuron1] > .25): 
                    t.moveMe(1)
                if (controls[1][best_neuron2] > .25): 
                    t.moveMe(-1)
                if (controls[2][best_neuron3] > .25): 
                    t.rotateMe(-1)
                if (controls[3][best_neuron4] > .25): 
                    t.rotateMe(1)
                if (controls[4][best_neuron5] > .25):
                    gx, gy = t.getGunTip()
                    ang = t.getGunAngle()
                    bullets.append(bullet(gx, gy, ang))
                    bulletsShot = bulletsShot + 1

                frame += 1
        # If in simulation mode, turrets actoins are controlled by
        # other means.
        else:
            if(frame > 0):
                if(len(bombs) > 1):
                    update_targ = distance(targets, t)
                    update_bomb = distance(bombs, t)
                    args = np.array([t.x, update_targ.x, update_bomb.x])
                else:
                    update_targ = distance(targets, t)
                    args = np.array([t.x, update_targ.x, Rand_BombX])
            
            # print(f"Args at frame {frame}: ",args)

            controls = neuralNet.forward(args)
            
            best_neuron1 = np.argmax(controls[0])
            best_neuron2 = np.argmax(controls[1])
            best_neuron3 = np.argmax(controls[2])
            best_neuron4 = np.argmax(controls[3])
            best_neuron5 = np.argmax(controls[4])

            # print(controls)

            # print(controls[0][best_neuron1])
            # print(controls[1][best_neuron2])
            # print(controls[2][best_neuron3])
            # print(controls[3][best_neuron4])
            # print(controls[4][best_neuron5])

            if (controls[0][best_neuron1] > 1.5): 
                t.moveMe(1)
            if (controls[1][best_neuron2] > 1.5): 
                t.moveMe(-1)
            if (controls[2][best_neuron3] > 1.5): 
                t.rotateMe(-1)
            if (controls[3][best_neuron4] > 1.5): 
                t.rotateMe(1)
            if (controls[4][best_neuron5] > 1.5):
                gx, gy = t.getGunTip()
                ang = t.getGunAngle()
                bullets.append(bullet(gx, gy, ang))
                bulletsShot = bulletsShot + 1

            frame += 1
            
        # --- Game logic should go here
        
        # Target Actions and crowd handeling
        numTargs = len(targets)
        if (numTargs > 1):
            j = 0
            for targ in targets:
                if (targ.doIExist() == True):
                    # Drop bomb.
                    myChance = random.randint(0, 100)
                    if (myChance < launchBomb):
                        bombBayX, bombBayY = targ.getBombBay()
                        bombs.append(bomb(bombBayX, bombBayY))
                    
                    # Target move.
                    # Find closest target to this target so we do not
                    # run into it.
                    if (j == 0):
                        closeTargX = targets[j+1].x
                    elif (j == (numTargs - 1)):
                        closeTargX = targets[j-1].x
                    else:
                        lDiff = abs(targ.x - targets[j-1].x)
                        rDiff = abs(targ.x - targets[j+1].x)
                        
                        closeTargX = targets[j-1].x
                        if (rDiff < lDiff):
                            closeTargX = targets[j+1].x
                            
                    # Figure out which way to move.
                    myMove = targ.what2Do(closeTargX, targWidth, t.x, 1)
                    # Move.
                    targ.moveMe(myMove)
                    
                    # Update j.
                    j = j+1
        # Lone Target movment
        elif (numTargs == 1):
            # Drop bomb.
            myChance = random.randint(0, 100)
            if (myChance < launchBomb):
                bombBayX, bombBayY = targ.getBombBay()
                bombs.append(bomb(bombBayX, bombBayY))
                
            # Move Target based on turret position.
            if (t.x < targets[0].x):
                myMove = left
            elif (t.x > targets[0].x):
                myMove = right
            else:
                myMove = noMove
                
            # Move.
            targets[0].moveMe(myMove)
           
        # --- Move bullets. 
        for b in bullets:
            b.moveMe()
            if (b.doIExist() == False):
                bullets.remove(b)
                #print(len(bullets))
                
        # --- Move bombs.
        for B in bombs:
            B.moveMe()
            if (B.doIExist() == False):
                bombs.remove(B)
        
        
                
        # --- Check to see if the bullets hit anything
        
        # Did a bullet hit a bomb?
        for b in bullets:
            for B in bombs:
                if (b.hit == False):
                    if (B.exists == True):
                        b.hit = collideBomb(b.x, b.y, b.radius, B.x, B.y, B.radius)
                        if (b.hit == True):
                            B.hit = True
                            bombsShotDown = bombsShotDown + 1
    
                        
        # Did a bullet hit a target?
        for b in bullets:
            for targ in targets:
                if (b.hit == False):
                    if (targ.exists == True):
                        b.hit = collideTarget(b.x, b.y, b.radius, targ.x, targ.y, targ.width, targ.height)
                        if (b.hit == True):
                            targ.hitCount = targ.hitCount + 1
                            bulletHits = bulletHits + 1
                          
        # Did a bomb hit the turret?
        for B in bombs:
            if ((B.exists == True) and (B.hit == False)):
                B.hit = collideBomb(B.x, B.y, B.radius, t.x, t.y, t.rad)
                if (B.hit == True):
                    t.hitCount = t.hitCount + 1
                    
        # Remove old targets.
        for targ in targets:
            if (targ.exists == False):
                targets.remove(targ)
                targetsKilled = targetsKilled + 1      
                #print("num targets = ", len(targets))
        
              
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        if (GAME_MODE) :
            screen.fill(BLACK)

        # --- Drawing code should go here
        # Draw turret.
        t.drawMe(screen)

        
        
        # Draw bullets.
        for b in bullets:
            b.drawMe(screen)

        # Draw targets.
        for targ in targets:
            targ.drawMe(screen)
            
        # Draw bombs.
        for B in bombs:
            B.drawMe(screen)
                
        # --- Go ahead and update the screen with what we've drawn.
        if (GAME_MODE):
            p.display.flip()
            # Only delay in game mode.
            clock.tick(60)
        
        if ((t.exists == False)or(len(targets) == 0)):
            running = False
           # print("Game Over")
            # Here is where you print the game statistics.
            
        loopcount = loopcount + 1
     
    # Close the window and quit.
    p.quit()
    
    return loopcount, t.hitCount, bulletsShot, bulletHits, bombsShotDown, targetsKilled


def distance(items, turret):
    closest_item = None
    closest_index = 0
    for i in range(len(items)):
        item = items[i]
        iXY = item.x, item.y
        tXY = turret.x, turret.y
        if(closest_item == None):
            closest_item = m.dist(iXY, tXY)
            closest_index = i
        elif(closest_item > m.dist(iXY, tXY)):
            closest_item = m.dist(iXY, tXY)
            closest_index = i

    return items[closest_index]

# def sigmoid_activate(layer):
#     return 1/(1+np.exp(-layer))

def softmax_activate(layer):
    # print(layer)
    m = np.exp(layer)
    # print(m/m.sum(len(layer.shape)-1))
    return m/m.sum(len(layer.shape)-1)

def activation_ReLU(inputs):
    output = np.maximum(0, inputs)
    return np.clip(output, 1e-7, 1 - 1e-7)


# def activation_softmax(inputs):
#     exp_values = np.exp(inputs - np.max(inputs, axis = 1, keepdims=True))
#     probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
#     print(probabilities)
#     return probabilities


class neuralNetwork:
    def __init__(self):
        self._score = 0
        self._layers = []
        self._biases = []

    def build(self, arguments, neurons, nb_layers, isACopy = False):
        self._score = 0
        self._layers = []
        self._biases = []

        if(not isACopy):
            for i in range(nb_layers):
                entry_size = neurons if i != 0 else len(arguments)
                self._layers.append(np.random.rand(neurons,entry_size)*2-1)
                self._biases.append(np.random.rand(neurons,1)*2-1)


            self._outputs = np.random.rand(5,neurons)*2-1

    def forward(self, inputs):
        inputs = inputs.reshape((-1,1))
        #layer acting as wieght
        for layer, bias in zip(self._layers, self._biases):
            inputs = np.matmul(layer,inputs)
            inputs = inputs+bias
            inputs = activation_ReLU(inputs)

        inputs = np.matmul(self._outputs, inputs)
        if(inputs.shape == 1): inputs = inputs.reshape(-1)

        return softmax_activate(inputs)



    def mutate(self, chances_of_mutation, neurons, nb_layers):
        update_neuarl = neuralNetwork()
        update_neuarl.build(np.random.randn(3,1), neurons, nb_layers, isACopy=True)

        for l in self._layers:
            random_mutation_probs = np.random.rand(l.shape[0], l.shape[1])

            random_mutation_probs = np.where(random_mutation_probs < chances_of_mutation,
                                             (np.random.rand()-0.5)/2, 0)
            new_l = l + random_mutation_probs
            update_neuarl._layers.append(new_l)


        for b in self._biases:
            random_mutation_probs = np.random.rand(b.shape[0], 1)
            random_mutation_probs = np.where(random_mutation_probs < chances_of_mutation,
                                             (np.random.rand()-0.5)/2, 0)
            new_l = b + random_mutation_probs
            update_neuarl._biases.append(new_l)


        random_mutation_probs = np.random.rand(self._outputs.shape[0],self._outputs.shape[1])
        random_mutation_probs = np.where(random_mutation_probs < chances_of_mutation,
                                         (np.random.rand()-0.5)/2, 0)

        new_l = self._outputs + random_mutation_probs
        update_neuarl._outputs = new_l
        return update_neuarl

    def rePopulate(self, best_network,):
        pass


    def give_score(self, score):
        self._score = score

class genetic_stuff:
    
    def __init__(self, weights):
        self.weights = weights
        self.rankings = []
       

    def rank_king(self):
        self.rankings = []
            
        for i in range(len(self.weights)):
            loopcount, turrethitCount, bulletsShot, bulletHits, bombsShotDown, targetsKilled = learnGame(self.weights[i])
            
            turretHitScore = (turrethitCount**2) * 10
            if(turrethitCount == 7):
                turretHitScore = 1000000
 
            rank = turretHitScore - ((targetsKilled)**4 + (loopcount)*10 + (bombsShotDown*2))
            self.rankings.append(rank)
        
        temp = list(zip(self.weights, self.rankings))
        temp.sort(key = lambda x: x[1])
        self.weights = [x[0] for x in temp]
        self.rankings = [x[1] for x in temp]
        best = self.weights[:15]
        new_weights = best.copy()
        for i in range(len(self.weights)-15):
            mutation = np.random.randint(0,100)
            mom = best[np.random.randint(0,15)]
            child_support = best[np.random.randint(0,15)]
            cross_point = np.random.randint(0,len(mom))
            child = mom[:cross_point].copy() + child_support[cross_point:].copy()
            if(mutation < 30):
                jean = np.random.randint(0, len(child))
                choices = np.array([True,False])
                child[jean] = np.random.choice(choices, size = 5).tolist()
            new_weights.append(child)

        self.weights = new_weights

#Neural Network
nb_layers = 3
neurons = 5

percentage_saved = 0.1 
chances_of_mutation = .15
training_rate = 1e+1
population_size = 10
epoch = 100

np.random.seed(0)

thePeople = []
creditScores = []
the_network = neuralNetwork()
GAME_MODE = False
# Train Neural Network for range(Population_Size)
for i in range(population_size):
    #Train said network
    for i in range(epoch):
        loopcount, turrethitCount, bulletsShot, bulletHits, bombsShotDown, targetsKilled = learnGame(the_network, neurons, nb_layers)
        the_network = the_network.mutate(chances_of_mutation, neurons, nb_layers)

        turretHitScore = (turrethitCount**2) * 10
        if(turrethitCount == 7):
            turretHitScore = 1000000
        score = turretHitScore - ((targetsKilled*5)**2 + (bombsShotDown * 10) + (bulletHits))

        the_network.give_score(score)
        thePeople.append(the_network)
        creditScores.append(the_network._score)

        #Asign to an array that ranks the members
    temp = list(zip(thePeople, creditScores))
    temp.sort(key = lambda x: x[1])

    best = [x[0] for x in temp]
    creditCheck = [x[1] for x in temp]

    
    print("Sorted: ",temp)
    print("Best Network: ", best[0])
    print("Best Score: ", creditCheck[0])
    print("loopcount: ", loopcount)
    print("turret was hit this many times: ", turrethitCount)
    print("bullets shot: ", bulletsShot)
    print("bullet hits:", bulletHits)
    print("bombs shot down: ", bombsShotDown)
    print("targets killed: ", targetsKilled) 

    the_network = best[0]
    thePeople = []
    creditScores = []

GAME_MODE = True
learnGame(the_network, neurons, nb_layers)
