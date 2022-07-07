#CITATIONS------------------------------------------------------------
# Main Character Sprites --> https://www.deviantart.com/maicerochico/art/Platinum-Looker-Overworld-Sprites-Ripped-651961803
# Zombie Sprite Sheet --> https://forums.rpgmakerweb.com/index.php?threads/zombie-waking-up-sprite.81889/
# Car Sprite --> https://forums.rpgmakerweb.com/index.php?threads/looking-for-moving-car-sprites.33057/
# Tree Sprite --> https://www.pinterest.com/pin/288300813628862845/
# Rock Sprite --> https://www.pngfuel.com/free-png/nynpt
# Shotgun Sprite --> https://www.pngkit.com/view/u2w7i1t4e6y3a9q8_double-barrel-double-barrel-shotgun-sprite/
# Machine Gun Sprite --> https://www.pngguru.com/free-transparent-background-png-clipart-iiclo
# Pistol Sprite --> https://uploads.scratch.mit.edu/users/avatars/18966577.png
# Grave Sprites --> https://opengameart.org/content/lpc-grave-markers-rework
# Bullet Sprite --> https://dlpng.com/png/1454337
# Instakill sprite --> https://www.clipartmax.com/middle/m2K9A0A0A0K9K9m2_skull-clipart-transparent-background-skull-and-crossbones-png/
# Nuke Sprite --> https://www.clipartmax.com/middle/m2i8K9A0G6m2N4m2_bomb-clip-art-at-vector-free-famclipart-nuclear-bomb-clipart/
# Instakill Indicator --> https://www.vectorstock.com/royalty-free-vector/pixel-skull-icon-vector-19144964

# IMPORTS--------------------------------------------------------------
import sys, pygame
import random
import math

# Helper Functions ----------------------------------------------------
def cyclethru(l):  # THis is the only pure helper function 
    r = l.pop(0)    # Used to control which gun is active in gunlist
    l.append(r)

# INITIAL VARIABLES----------------------------------------------------
pygame.init()
width = 700
height = 700
Frames = 40
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
characterbox = pygame.image.load('lookerl1.png')
charx,chary = characterbox.get_size()
toggle = True
# ANIMATIONS-----------------------------------------------------------------
MainLeft = [pygame.image.load('lookerl11.png'),pygame.image.load('lookerl12.png'),pygame.image.load('lookerl13.png'),pygame.image.load('lookerl14.png')]
MainRight = [pygame.image.load('lookerr11.png'),pygame.image.load('lookerr12.png'),pygame.image.load('lookerr13.png'),pygame.image.load('lookerr14.png')]
MainUp = [pygame.image.load('lookeru11.png'),pygame.image.load('lookeru12.png'),pygame.image.load('lookeru13.png'),pygame.image.load('lookeru14.png')]
MainDown = [pygame.image.load('lookerd11.png'),pygame.image.load('lookerd12.png'),pygame.image.load('lookerd13.png'),pygame.image.load('lookerd14.png')]
ZombLeft = [pygame.image.load('zombl11.png'),pygame.image.load('zombl12.png'),pygame.image.load('zombl13.png'),pygame.image.load('zombl14.png')]
ZombRight = [pygame.image.load('zombr11.png'),pygame.image.load('zombr12.png'),pygame.image.load('zombr13.png'),pygame.image.load('zombr14.png')]
ZombUp = [pygame.image.load('zombu11.png'),pygame.image.load('zombu12.png'),pygame.image.load('zombu13.png'),pygame.image.load('zombu14.png')] 
ZombDown = [pygame.image.load('zombd11.png'),pygame.image.load('zombd12.png'),pygame.image.load('zombd13.png'),pygame.image.load('zombd14.png')]
AnimHurt = [pygame.image.load('hurt1.png'),pygame.image.load('hurt2.png'),pygame.image.load('hurt3.png'),pygame.image.load('hurt4.png')]
    
# TILE CLASS------------------------------------------------------------------

class Tiles(pygame.sprite.Sprite):    #This class creates grasstiles that form as the player moves
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = x, y
        self.character = pygame.image.load('grasstile.png')
        self.width, self.height = self.character.get_size()
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
         
    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def updateChr(self):
        self.getrect()
        self.image.blit(self.character,(0,0))

# MAIN CHARACTER CLASS------------------------------------------------
class Hero(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Level
        self.level = 1
        self.deadzombies = 10 #Number of zombies that need to die before level change
        self.spawn = 50 # Controls the likelihood of new zombie spawn

        # Character Dimensions
        self.character = pygame.image.load('lookerd11.png')
        self.width, self.height = self.character.get_size()
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))
        #Speed and Direction
        self.vx = 8
        self.vy = 8
        self.bulletv = 20
        self.dirs = [0,0,0,0]
        #Timers
        self.walkT = 49
        self.reloadT = 49
        self.shootT = 49
        self.deathT = 49 # Makes sure zombie can hurt character once per second
        self.lifeT = 199 # Regenerates health once every 2 seconds
        self.hurtT = 49 # Red animation when hit
        self.instaT = 400 # Lets instakill last 10 seconds
        #Character States
        self.reloading = False
        self.reloaded = True
        self.automatic = False
        self.hurting = False
        self.instakill = False
        self.gameover = False
        self.start = False
        #Attributes
        self.lives = 5
        self.gunlist = ['pistol','shotgun','machinegun']
        self.fullbarrel = 6
        self.bullets = self.fullbarrel
        self.bulletperc = (self.bullets/self.fullbarrel) # Ensures changing gun does not reload
        self.bulletdamage = 2 
        self.money = 0 #This is the score
        self.updateChr()
        
        
    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))

    def reloadGun(self): # This ensures player can't shoot while reloading
        if self.reloadT//10 == 0:
            self.bullets = self.fullbarrel
            self.reloaded = True
            self.reloadT = 49
            self.reloading = False
        self.reloadT -=1
    
    def gunAttrs(self,s): # Perks of each gun 
        if s == 'pistol':
            self.bulletperc = (self.bullets/self.fullbarrel)
            
            self.fullbarrel = 6
            self.bullets = int(self.bulletperc*self.fullbarrel)
            self.bulletdamage = 2
            self.bulletv = 20
            self.automatic = False
        elif s == 'shotgun':
            self.bulletperc = (self.bullets/self.fullbarrel)
            
            self.fullbarrel = 2
            self.bullets = int(self.bulletperc*self.fullbarrel)
            self.bulletdamage = 10
            self.bulletv = 50
            self.automatic = False
        elif s == 'machinegun':
            self.bulletperc = (self.bullets/self.fullbarrel)
            
            self.fullbarrel = 20
            self.bullets = int(self.bulletperc*self.fullbarrel)
            self.bulletdamage = 1
            self.bulletv = 30
            self.automatic = True
    
    def changeGun(self):
        cyclethru(self.gunlist)
        self.gunAttrs(self.gunlist[0])
        #self.reloaded = True
        self.reloadT = 49
        self.reloading = False

    def takelife(self): 
        if self.deathT//10 == 0:
            self.lives -= 1
            self.deathT = 49
            self.hurting = True
        else:
            self.deathT-=1
        if self.lives <= 0:
            pass
    
    def regenlife(self): #Character passively regenerates life
        if self.lives <5:
            if self.lifeT//10 == 0:
                self.lives+=1
                self.lifeT = 199
            else:
                self.lifeT -=1

    def updateChr(self): 
        self.image.fill((0,0,0,0)) #Animates the main character
        if self.dirs == [1,0,0,0]:
            animateChr(self,MainUp)
        elif self.dirs == [0,1,0,0]:
            animateChr(self,MainDown)
        elif self.dirs == [0,0,1,0]:
            animateChr(self,MainLeft)
        elif self.dirs == [0,0,0,1]:
            animateChr(self,MainRight)
        
        if self.deadzombies<=0:  #This changes the level
            self.level +=1
            self.deadzombies = int(self.level*10)
            self.spawn = int(.9*self.spawn)
            for zombie in zombieList:
                zombie.lives +=1
        
        if self.instakill: #This controls states during instakill mode
            self.bulletdamage = 100
            self.instaT-=1
            if self.instaT<=10:
                if self.gunlist[0] == 'pistol':
                    self.bulletdamage = 1
                elif self.gunlist[0] == 'shotgun':
                    self.bulletdamage = 10
                elif self.gunlist[0] == 'machinegun':
                    self.bulletdamage = 2
                self.instaT = 400
                self.instakill = False

    
        self.getrect()
        self.image.blit(self.character,(0,0))

# ZOMBIE CLASS----------------------------------------------------------
class Villain(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Character Dimensions
        self.character = pygame.image.load('zombd2.png')
        self.width, self.height = self.character.get_size()
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))
        self.damagerect = pygame.Rect(self.x-5,self.y-5,self.width+10,self.height+10)
        #Character speed and Directions
        self.oldx=0
        self.oldy=0
        self.vx = random.randint(1,3)
        self.vy = self.vx
        self.dirs = [0,0,0,0]
        #Timers
        self.walkT = 49
        self.stuckT = 10 
        #Attributes
        self.lives = 3
        self.count = 0
        self.die = False #Used for nuke kills
        
    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))
        self.damagerect = pygame.Rect(self.x-5,self.y-5,self.width+10,self.height+10)
    
    def freeZomb(self,s): #This allows zombies to go around simple obstacles
        if s == 'side':
            if (self.x == self.oldx) and (self.y == self.oldy):
                self.stuckT-=1
                self.oldx = self.x
                self.oldy = self.y
                if self.stuckT <= 0:
                    return True
            elif self.stuckT<=0:
                if (self.x == self.oldx):
                    self.oldx = self.x
                    self.oldy = self.y
                    return True
                else:
                    self.stuckT = 10
                    self.oldx = self.x
                    self.oldy = self.y
                    return False
            else:
                self.stuckT = 10
                self.oldx = self.x
                self.oldy = self.y
                return False

        elif s == 'top':
            if (self.x == self.oldx) and (self.y == self.oldy):
                self.stuckT-=1
                self.oldx = self.x
                self.oldy = self.y
                if self.stuckT <= 0:
                    return True
            elif self.stuckT<=0:
                if (self.y == self.oldy):
                    self.oldx = self.x
                    self.oldy = self.y
                    return True
                else:
                    self.stuckT = 10
                    self.oldx = self.x
                    self.oldy = self.y
                    return False
            else:
                self.stuckT = 10
                self.oldx = self.x
                self.oldy = self.y
                return False
        
    def follow(self,x,y,sprit,grup): #This controls zombie ai and makes it follow the main character
        negx = 1
        negy = 1
        if self.x > x:
            self.dirs = [0,0,1,0]
            negx = -1
        elif self.x//10*10 == x//10*10:
            if self.y>y:
                self.dirs = [1,0,0,0]
            elif self.y<y:
                self.dirs = [0,1,0,0]
        elif self.x < x:
            self.dirs = [0,0,0,1]
        self.x += negx*self.vx
        self.getrect()
        for obstacle in ObstacleList:
            obstacle.getrect()
        if pygame.sprite.spritecollide(self,grup,False,False): #If zombie collides with obstacle
            self.x -= negx*self.vx
            if self.count%2 == 0:
                if self.freeZomb('side'):
                    self.y += 3*self.vy

        if self.y > y:
            self.dirs = [1,0,0,0]
            negy = -1
        elif self.y//20*20 == y//20*20:
            negy = 0
            if self.x>x:
                self.dirs = [0,0,1,0]
            elif self.x<x:
                self.dirs = [0,0,0,1]
        elif self.y < y:
            self.dirs = [0,1,0,0]
        self.y += negy*self.vy
        self.getrect()
        for obstacle in ObstacleList:
                obstacle.getrect()
        if pygame.sprite.spritecollide(self,grup,False,False): #If zombie collides with obstacle
            self.y -= negy*self.vy
            if self.count%2 ==0:
                if self.freeZomb('top'):
                    self.x -= 3*self.vx

        if self.damagerect.colliderect(sprit.rect): #If zombie is near player, player gets hurt
            sprit.takelife()
        
    def updateChr(self,grup,Source):
        if pygame.sprite.spritecollide(self,grup,True):
            self.lives -= Source.bulletdamage
        if self.lives <= 0:
            spawn = random.randint(1,20) # There is a 5% chance zombie drops powerup
            powertype = random.randint(1,2) #Powerup can be a nuke or instakill
            if spawn == 1:
                if powertype == 1:
                    power = Powerup(self.x,self.y,'insta')
                elif powertype == 2:
                    power = Powerup(self.x,self.y,'nuke')
                PowerupList.append(power)
                RelativeMotionList.append(power)
                AllSprites.append(power)
            MainCh.deadzombies -= 1
            killZombie(self) #Zombie is killed
            
        if self.dirs != [0,0,0,0]:
            self.image.fill((0,0,0,0))  
        if self.dirs == [0,0,0,0]:
            pass
        elif self.dirs == [0,0,1,0]:
            animateChr(self,ZombLeft)
        elif self.dirs == [0,0,0,1]:     #This block controls zombie animations
            animateChr(self,ZombRight)
        elif self.dirs == [1,0,0,0]:
            animateChr(self,ZombUp)
        elif self.dirs == [0,1,0,0]:
            animateChr(self,ZombDown)
        self.count+=1

        if self.die:
            killZombie(self)      #This is how the zombie dies from a nuke
            MainCh.deadzombies -= 1

        self.getrect()
        self.image.blit(self.character,(0,0))

# BULLET CLASS----------------------------------------------------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        # Dimensions
        self.character = pygame.image.load('bulletr.png')
        self.width, self.height = self.character.get_size()
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        #Speed and directions
        self.v = MainCh.bulletv
        self.dirs = [0,1,0,0]
        self.fix = True

    def getrect(self):
        self.width, self.height = self.character.get_size()
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        
    def SetDir(self,source): #This sets the direction the bullet goes depending on 
        if self.fix:         # where the main character is facing
            self.dirs = source.dirs
        self.fix = False

    def updateChr(self,grup,grup1):
        self.image.fill((0,0,0,0))
        #Bullet disappears if it goes off screen
        if (self.y<0) or (self.y>height) or (self.x<0) or (self.x>width): 
            killBullet(self)
        #Disappears if it hits zombie
        if pygame.sprite.spritecollide(self,grup,True ):
            killBullet(self)
        #Disappears if it hits obstacle
        if pygame.sprite.spritecollide(self,grup1,False ):
            killBullet(self)
        if self.dirs == [1,0,0,0]:
            self.character = pygame.image.load('bulletu.png')
            self.y-=self.v
        elif self.dirs == [0,1,0,0]:
            self.character = pygame.image.load('bulletd.png') #Controls animation
            self.y+=self.v
        elif self.dirs == [0,0,1,0]:
            self.character = pygame.image.load('bulletr.png')
            self.x-=self.v
        elif self.dirs == [0,0,0,1]:
            self.character = pygame.image.load('bulletl.png')
            self.x+=self.v

        self.getrect()
        self.image.blit(self.character,(0,0))

# OBSTACLE CLASS----------------------------------------------------------
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,s):
        pygame.sprite.Sprite.__init__(self)
        # Dimensions
        if s == 'car':
            self.character = pygame.image.load('cars.png')
        elif s == 'grave1':
            self.character = pygame.image.load('grave1.png')
        elif s == 'grave2':
            self.character = pygame.image.load('grave2.png')
        elif s == 'grave3':
            self.character = pygame.image.load('grave3.png')
        elif s == 'tree':
            self.character = pygame.image.load('tree.png')
        elif s == 'rock':
            self.character = pygame.image.load('rock.png')
        elif s == 'topwall':
            self.character = pygame.image.load('topwall.png')
        elif s == 'sidewall':
            self.character = pygame.image.load('sidewall.png')

        self.width, self.height = self.character.get_size()
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        
    def genObstacle(self):
        RelativeMotionList.append(self) #For relative screen motion
        AllSprites.append(self) 
        Stop_Collide_Group.add(self)
        ObstacleList.append(self)

    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def updateChr(self):
        self.getrect()
        self.image.blit(self.character,(0,0))

# POWERUP CLASS----------------------------------------------------------
class Powerup(pygame.sprite.Sprite):
    def __init__(self,x,y,s):
        pygame.sprite.Sprite.__init__(self)
        #Character Dimensions
        self.s = s
        if self.s == 'nuke':
            self.character = pygame.image.load('nuke.png')
        elif self.s == 'insta':
            self.character = pygame.image.load('insta.png')
        self.width, self.height = self.character.get_size()
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)

    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))
    
    def updateChr(self):
        if MainCh.depthRect.colliderect(self.depthRect):
            if self.s == 'nuke':
                for zombie in zombieList:
                    zombie.die = True       #If nuked, a flat score of 50 is added
                    MainCh.money -= 10
                MainCh.money += 50

            elif self.s == 'insta':
                MainCh.bulletdamage = 100
                MainCh.instakill = True
            PowerupList.remove(self)       #If instakill is on, bullet damage is raised to 100
            AllSprites.remove(self)
        self.getrect()
        self.image.blit(self.character,(0,0))


#MAIN LOOP STARTING CONDITIONS------------------------------------------------------
playing = True
MainCh = Hero(width//2-(charx//2),height//2-(chary//2)) # Main Character sprite spawned
testTile = Tiles(0,0) #All tiles referenced to this tile

#EMPTY LISTS AND GROUPS--------------------------------------------------------------
zombieList = []
bulletlist = []
AllSprites = []
RelativeMotionList = []
ObstacleList = []
TileList = []
PowerupList = []
RandomObjectsGroup = pygame.sprite.Group()
TileGroup = pygame.sprite.Group()
Slide_Collide_Group = pygame.sprite.Group()
Stop_Collide_Group = pygame.sprite.Group()
Bullet_Group = pygame.sprite.Group()
AllSprites.append(MainCh)

# EXTRA FUNCTIONS -----------------------------------------------------------------
def makeBackgroundTiles(w,h):
    TileLocations = []
    tilex = width//w
    tiley = height//h
    for i in range(-1,tilex):           # This generates grass tiles filling the screen
        for j in range(-1,tiley):
            TileLocations.append((w*i,h*j))
    
    for (i,j) in TileLocations:
        new = Tiles(i,j)
        new.updateChr()
        TileGroup.add(new)
        RelativeMotionList.append(new)
        TileList.append(new)

def genZombie():
    dirzomb = random.randint(1,4)
    if dirzomb == 1:
        zomby = -50
        zombx = random.randint(0,width)
    elif dirzomb == 2:                  # This generates zombie locations just outside the screen
        zomby = height+50
        zombx = random.randint(0,width)
    elif dirzomb == 3:
        zombx = -50
        zomby = random.randint(0,height)
    elif dirzomb == 4:
        zombx = width+50
        zomby = random.randint(0,height)
    new = Villain(zombx,zomby) #This generates a new zombie in that loaction
    zombieList.append(new)
    RelativeMotionList.append(new) #For relative screen motion
    AllSprites.append(new) 
    Slide_Collide_Group.add(new) #for collisions
    if pygame.sprite.spritecollide(new,Stop_Collide_Group,False,False):
        killZombie(new)
        MainCh.money-=10
        genZombie()

def genTestZombie(x,y): # Generates a zombie in a given loaction
    new = Villain(x,y)
    zombieList.append(new)
    RelativeMotionList.append(new) #For relative screen motion
    AllSprites.append(new) 
    Slide_Collide_Group.add(new) #for collisions

def genBullet(Source,x,y):
    if Source.reloaded:
        Source.shooting = True
        Source.bullets-=1
        if Source.bullets == 0:
            Source.reloaded = False      #Generates a bullet at the main character for normal guns
        new = Bullet(x,y)
        new.SetDir(Source)
        RelativeMotionList.append(new)
        AllSprites.append(new)
        bulletlist.append(new)
        Bullet_Group.add(new)
        

def genBulletMach(Source,x,y):
    if Source.reloaded:
        Source.shooting = True
        if Source.shootT//10 == 0:
            Source.bullets-=1
            new = Bullet(x,y)
            new.SetDir(Source)
            RelativeMotionList.append(new) #This function is used when the machinegun is selected
            AllSprites.append(new)
            bulletlist.append(new)
            Bullet_Group.add(new)
            Source.shootT = 49
        else:
            Source.shootT -= 8
        if Source.bullets == 0:
            Source.reloaded = False


def killBullet(bullet):
    if bullet not in RelativeMotionList:
        pass
    else:
        RelativeMotionList.remove(bullet)
    if bullet not in AllSprites:
        pass                              #This removes a bullet when it lands
    else:
        AllSprites.remove(bullet)
    if bullet not in bulletlist:
        pass
    else:
        bulletlist.remove(bullet)
  


def killZombie(zombie):
    zombieList.remove(zombie)
    RelativeMotionList.remove(zombie)
    AllSprites.remove(zombie)              #This removes a zombie from all lists and groups
    Slide_Collide_Group.remove(zombie)
    MainCh.money+=10 

def animateChr(grup,L):
    if grup.walkT//10 == 0:
        grup.walkT = 49
    if grup.walkT//10 == 4:
        grup.character = L[0]
    elif grup.walkT//10 == 3:
        grup.character = L[1]    #This function used for walking animation
    elif grup.walkT//10 == 2:
        grup.character = L[2]
    elif grup.walkT//10 == 1:
        grup.character = L[3]
    grup.walkT -= 1

def animateHurt(sprit,L):
    if sprit.hurtT//10 == 0:
        sprit.hurtT = 49
        sprit.hurting = False
    elif sprit.hurtT//10 == 4:
        screen.blit(L[0],(0,0))
    elif sprit.hurtT//10 == 3:
        screen.blit(L[1],(0,0))   # This function used for red hurting animation
    elif sprit.hurtT//10 == 2:
        screen.blit(L[2],(0,0))
    elif sprit.hurtT//10 == 1:
        screen.blit(L[3],(0,0))
    sprit.hurtT -= 1

def populateMap(n,xl,xu,yl,yu):
    count = 0
    for __ in range(n):
        xi = random.randint(xl,xu)
        yi = random.randint(yl,yu)
        if count<5:
            s = 'grave1'
        elif count<10:          # This populates the map with obstacles
            s = 'grave2'        # in a given range
        elif count<15:
            s = 'grave3'
        elif count<20:
            s = 'rock'
        elif count<23:
            s = 'car'
        elif count<n:
            s = 'tree'

        new = Obstacle(xi,yi,s) # Obstacle generated
        while (pygame.sprite.spritecollide(new,RandomObjectsGroup,False,False))\
             or (MainCh.rect.colliderect(new.rect)==True):
            xi = random.randint(xl,xu)
            yi = random.randint(yl,yu)
            new = Obstacle(xi,yi,s)     #This block ensures obstacles don't overlap
        RandomObjectsGroup.add(new)

        new.genObstacle()
        count+=1

# Function below makes sure sprites are printed according to the location of their y-coordinate.
# This lets the sprites have some depth
def generateOrderedGroup(L):
    new = sorted(L,key=lambda character: (character.y))
    sprite_Group = pygame.sprite.OrderedUpdates()
    for i in new:
        sprite_Group.add(i) 
    return sprite_Group #Returns ordered group
    
def UpdateMap(Source,grup1,grup2):
    if Source.dirs == [0,0,1,0]:
        for sprit in RelativeMotionList:
            sprit.x += Source.vx
            sprit.getrect()
            MainCh.getrect()
        if pygame.sprite.spritecollide(Source,grup2,False,False):
            for sprit in RelativeMotionList:
                sprit.x -= Source.vx 
                MainCh.getrect()
    elif Source.dirs == [0,0,0,1]:
        for sprit in RelativeMotionList:
            sprit.x -= Source.vx
            MainCh.getrect()
            sprit.getrect()
        if pygame.sprite.spritecollide(Source,grup2,False,False):
            for sprit in RelativeMotionList:
                sprit.x += Source.vx 
                MainCh.getrect()
    elif Source.dirs == [1,0,0,0]:
        for sprit in RelativeMotionList:
            sprit.y += Source.vy
            sprit.getrect()
            MainCh.getrect()
        if pygame.sprite.spritecollide(Source,grup2,False,False):
            for sprit in RelativeMotionList:
                sprit.y -= Source.vy 
                MainCh.getrect()
    elif Source.dirs == [0,1,0,0]:
        for sprit in RelativeMotionList:
            sprit.y -= Source.vy
            sprit.getrect()
            MainCh.getrect()
        if pygame.sprite.spritecollide(Source,grup2,False,False):
            for sprit in RelativeMotionList:
                sprit.y += Source.vy 
                MainCh.getrect()
    for tile in TileList:
        if (tile.x<-testTile.width):#(-1*testTile.width)):
            tile.x +=width+testTile.width
        if (tile.x>width):
            tile.x -=width+testTile.width
        if (tile.y<testTile.height):
            tile.y += height+testTile.height
        if (tile.y>height):
            tile.y -= height+testTile.height


def drawOverlay():
    screen.blit(pygame.image.load('shadow.png'),(0,0))
    if MainCh.gunlist[0] == 'pistol':
        screen.blit(pygame.image.load('pistolbanner.png'),(0,0))    #Picks and draws gun image
    elif MainCh.gunlist[0] == 'shotgun':
        screen.blit(pygame.image.load('shotgunbanner.png'),(0,0))
    elif MainCh.gunlist[0] == 'machinegun':
        screen.blit(pygame.image.load('machinebanner.png'),(0,0))
    font = pygame.font.SysFont("impact", 30)                        #Picks Font
    text1 = font.render(str(MainCh.bullets), True, (255, 255, 0))
    text2 = font.render(str(MainCh.money), True, (255, 255, 0))     
    text3 = font.render(str(MainCh.lives), True, (255, 255, 0))     #Picks text location
    text4 = font.render(str(MainCh.level), True, (255, 0, 0))
    screen.blit(text1,(50,12))
    screen.blit(text2,(390,12))     #Draws text
    screen.blit(text3,(525,12))
    screen.blit(text4,(650,12))


    

# REDRAW-----------------------------------------------------------------------------
def redrawGame(screen):
    screen.fill((0,0,0))
    sprite_Group = generateOrderedGroup(AllSprites) #Makes ordered group
    sprite_Group.update(width,height) 
    TileGroup.update(width,height) 
    TileGroup.draw(screen)      # Background(grass tiles)
    sprite_Group.draw(screen)   # All sprites drawn
    if MainCh.hurting:
        animateHurt(MainCh,AnimHurt)  #Red hurt animation
    if MainCh.gameover:
        screen.blit(pygame.image.load('gameover.png'),(0,0))
    if MainCh.start == False:
        screen.blit(pygame.image.load('startscreen.png'),(0,0))
    if MainCh.instakill:
        screen.blit(pygame.image.load('indicator.png'),(0,0))
    drawOverlay() #Overlay with score and lives
    
    pygame.display.flip()

#BACKGROUND SETUP-----------------------------------------------------------------

makeBackgroundTiles(testTile.width,testTile.height)
populateMap(33,-1000,1000,-1000,1000)

# MAIN LOOP-----------------------------------------------------------------

while playing:
    clock.tick(Frames) 
    for event in pygame.event.get():
        # SINGLE BUTTON PRESSES 
        if event.type == pygame.KEYDOWN: #When button is pressed down
            if event.key == pygame.K_SPACE: #Space shoots if not machine gun
                if MainCh.automatic:
                    pass
                else:
                    genBullet(MainCh,width//2,height//2)
            if event.key == pygame.K_s: # s starts the game
                MainCh.start = True
            if event.key == pygame.K_z: # z reloads
                MainCh.reloading = True
            if event.key == pygame.K_x: # x changes guns
                MainCh.changeGun()
            if event.key == pygame.K_w: # w generates test zombie at 100,100 
                genTestZombie(100,100)
            if event.key == pygame.K_q: # q toggles zombie spawn 
                if toggle:
                    toggle = False
                else:
                    toggle = True 
            if event.key == pygame.K_e: # e generates nuke at 100,100 
                newpowerup = Powerup(100,100,'nuke')
                PowerupList.append(newpowerup)
                RelativeMotionList.append(newpowerup)
                AllSprites.append(newpowerup)
                
            if event.key == pygame.K_r: # r generates instakill at 100,100 
                newpowerup = Powerup(100,100,'insta')
                PowerupList.append(newpowerup)
                RelativeMotionList.append(newpowerup)
                AllSprites.append(newpowerup)

            if event.key == pygame.K_t: # t generates car at 100,100 
                Car = Obstacle(100,100,'car')
                Car.genObstacle()
        if event.type ==   pygame.QUIT:
            playing = False
    # CONTINUOUS BUTTON PRESSES
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_UP]:  # Up moves up
        MainCh.dirs = [1,0,0,0]
        MainCh.updateChr()
        UpdateMap(MainCh,Slide_Collide_Group,Stop_Collide_Group)
        
    if keys[pygame.K_DOWN]: # Down moves down
        MainCh.dirs = [0,1,0,0]
        UpdateMap(MainCh,Slide_Collide_Group,Stop_Collide_Group)
        MainCh.updateChr()

    if keys[pygame.K_LEFT]: # Left moves left
        MainCh.dirs = [0,0,1,0]
        UpdateMap(MainCh,Slide_Collide_Group,Stop_Collide_Group)
        MainCh.updateChr()

    if keys[pygame.K_RIGHT]: # Right moves right
        MainCh.dirs = [0,0,0,1]
        UpdateMap(MainCh,Slide_Collide_Group,Stop_Collide_Group)
        MainCh.updateChr()

    if keys[pygame.K_SPACE]: # Space shoots if automatic weapon
        if MainCh.automatic == False:
            pass
        else:
            genBulletMach(MainCh,width//2,height//2)
    
    # UPDATES

    if MainCh.reloading:  # reloads for 1 second
        MainCh.reloadGun()

    for zombie in zombieList:
        Slide_Collide_Group.remove(zombie) #Updates zombies to follow main character
        zombie.follow(MainCh.x,MainCh.y,MainCh,Stop_Collide_Group)
        zombie.updateChr(Bullet_Group,MainCh)
        Slide_Collide_Group.add(zombie)

    for bullet in bulletlist: # Updates bullets to make them move and land
        bullet.updateChr(Slide_Collide_Group,RandomObjectsGroup)
    testTile.updateChr()

    for obstacle in ObstacleList: #Updates bbjects as main character moves
        obstacle.updateChr()
    MainCh.regenlife()
    
    for powerup in PowerupList: # Updates all powerups
        powerup.updateChr()

    if MainCh.start == True and toggle == True:
        rando = random.randint(1,MainCh.spawn) #Starts spawning zombies
        if rando ==1:
            genZombie()


    if MainCh.lives<=0: #Ends game if       
        MainCh.lives = 0           
        MainCh.gameover = True

    # CALLS ON REDRAW ALL 
    redrawGame(screen)

print("Your Score is "+str(MainCh.money))

pygame.quit()