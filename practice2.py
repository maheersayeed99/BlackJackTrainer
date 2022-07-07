# IMPORTS--------------------------------------------------------------
import sys, pygame
import random
import math

# INITIAL VARIABLES----------------------------------------------------
pygame.init()
width = 650
height = 650
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
characterbox = pygame.image.load('lookerl1.png')
charx,chary = characterbox.get_size()

# ANIMATIONS-----------------------------------------------------------------
MainLeft = [pygame.image.load('lookerl1.png'),pygame.image.load('lookerl2.png'),pygame.image.load('lookerl3.png'),pygame.image.load('lookerl4.png')]
MainRight = [pygame.image.load('lookerr1.png'),pygame.image.load('lookerr2.png'),pygame.image.load('lookerr3.png'),pygame.image.load('lookerr4.png')]
MainUp = [pygame.image.load('lookeru1.png'),pygame.image.load('lookeru2.png'),pygame.image.load('lookeru3.png'),pygame.image.load('lookeru4.png')]
MainDown = [pygame.image.load('lookerd1.png'),pygame.image.load('lookerd2.png'),pygame.image.load('lookerd3.png'),pygame.image.load('lookerd4.png')]
ZombLeft = [pygame.image.load('zombl1.png'),pygame.image.load('zombl2.png'),pygame.image.load('zombl3.png'),pygame.image.load('zombl4.png')]
ZombRight = [pygame.image.load('zombr1.png'),pygame.image.load('zombr2.png'),pygame.image.load('zombr3.png'),pygame.image.load('zombr4.png')]
ZombUp = [pygame.image.load('zombu1.png'),pygame.image.load('zombu2.png'),pygame.image.load('zombu3.png'),pygame.image.load('zombu4.png')] 
ZombDown = [pygame.image.load('zombd1.png'),pygame.image.load('zombd2.png'),pygame.image.load('zombd3.png'),pygame.image.load('zombd4.png')]

    
# BACKGROUND CLASS------------------------------------------------
class Bg(object):
    def __init__(self,x,y):
        self.img = pygame.image.load('bg1.png')
        self.width, self.height = self.img.get_size()
        self.x = x - self.width//2
        self.y = y - self.height//2
        self.border = 100
    def updateChr(self):
        pass

# MAIN CHARACTER CLASS------------------------------------------------
class Hero(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        # Character Dimensions
        self.character = pygame.image.load('looker1.png')
        self.width, self.height = self.character.get_size()
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))
        #Speed and Direction
        self.vx = 8
        self.vy = 8
        self.dirs = [0,0,0,0]
        #Animation Timers
        self.walkT = 49
        self.reloadT = 49
        #Character States
        self.reloading = False
        self.reloaded = True
        #Attributes
        self.bullets = 6
        self.updateChr()
        
    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))

    def reloadGun(self):
        if self.reloadT//10 == 0:
            self.bullets = 6
            self.reloaded = True
            self.reloadT = 49
            self.reloading = False
        self.reloadT -=1

    def updateChr(self):
        self.image.fill((0,0,0,0))
        if self.dirs == [1,0,0,0]:
            animateChr(self,MainUp)
        elif self.dirs == [0,1,0,0]:
            animateChr(self,MainDown)
        elif self.dirs == [0,0,1,0]:
            animateChr(self,MainLeft)
        elif self.dirs == [0,0,0,1]:
            animateChr(self,MainRight)

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
        #Character speed and Directions
        self.vx = random.randint(1,3)
        self.vy = random.randint(1,3)
        self.dirs = [0,0,0,0]
        #Animation Timers
        self.walkT = 49
        #Attributes
        self.lives = 3
        
    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))
    
    def follow(self,x,y,sprit,grup):
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
        
        if self.depthRect.colliderect(sprit.depthRect):
            self.x -= negx*self.vx
        if self.y > y:
            self.dirs = [1,0,0,0]
            negy = -1
        elif self.y//15*15 == y//15*15:
            negy = 0
            if self.x>x:
                self.dirs = [0,0,1,0]
            elif self.x<x:
                self.dirs = [0,0,0,1]
        elif self.y < y:
            self.dirs = [0,1,0,0]
        self.y += negy*self.vy
        if pygame.sprite.spritecollide(self,grup,False,False):
            #self.y -= negy*self.vy
            self.x -= negx*self.vx
        if self.depthRect.colliderect(sprit.depthRect):
            self.y -= negy*self.vy
        

    def updateChr(self,grup):
        if pygame.sprite.spritecollide(self,grup,True):
            self.lives -= 1
        if self.lives == 0:
            killZombie(self)
        if self.dirs != [0,0,0,0]:
            self.image.fill((0,0,0,0))
        if self.dirs == [0,0,0,0]:
            pass
        elif self.dirs == [0,0,1,0]:
            animateChr(self,ZombLeft)
        elif self.dirs == [0,0,0,1]:
            animateChr(self,ZombRight)
        elif self.dirs == [1,0,0,0]:
            animateChr(self,ZombUp)
        elif self.dirs == [0,1,0,0]:
            animateChr(self,ZombDown)
        
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
        self.v = 20
        self.dirs = [0,1,0,0]
        self.fix = True

    def getrect(self):
        self.width, self.height = self.character.get_size()
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        
    def SetDir(self,source):
        if self.fix:
            self.dirs = source.dirs
        self.fix = False

    def updateChr(self,grup):
        self.image.fill((0,0,0,0))
        if (self.y<0) or (self.y>height) or (self.x<0) or (self.x>width):
            killBullet(self)
        if pygame.sprite.spritecollide(self,grup,True ):
            killBullet(self)
        if self.dirs == [1,0,0,0]:
            self.character = pygame.image.load('bulletu.png')
            self.y-=self.v
        elif self.dirs == [0,1,0,0]:
            self.character = pygame.image.load('bulletd.png')
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
        self.width, self.height = self.character.get_size()
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//4),self.width,((self.height//4)*3))
    
    def genObstacle(self):
        RelativeMotionList.append(self) #For relative screen motion
        AllSprites.append(self) 
        Stop_Collide_Group.add(self)

    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//4),self.width,((self.height//4)*3))

    def updateChr(self):
        self.getrect()
        self.image.blit(self.character,(0,0))


#MAIN LOOP STARTING CONDITIONS------------------------------------------------------

playing = True
MainCh = Hero(width//2-(charx//2),height//2-(chary//2))


zombieList = []
bulletlist = []
AllSprites = []
RelativeMotionList = []
Slide_Collide_Group = pygame.sprite.Group()
Stop_Collide_Group = pygame.sprite.Group()
Bullet_Group = pygame.sprite.Group()
AllSprites.append(MainCh)
Background = Bg(0,0)
RelativeMotionList.append(Background)



# EXTRA FUNCTIONS -----------------------------------------------------------------
def genZombie():
    x = random.randint(0,width)
    y = random.randint(0,height)
    new = Villain(x,y)
    zombieList.append(new)
    RelativeMotionList.append(new) #For relative screen motion
    AllSprites.append(new) 
    Slide_Collide_Group.add(new) #for collisions

def genTestZombie(x,y):
    new = Villain(x,y)
    zombieList.append(new)
    RelativeMotionList.append(new) #For relative screen motion
    AllSprites.append(new) 
    Slide_Collide_Group.add(new) #for collisions

def genBullet(Source,x,y):
    #x = Source.x#+Source.width//2
    #y = Source.y#+Source.height//2+40
    if Source.reloaded:
        Source.shooting = True
        Source.bullets-=1
        if Source.bullets == 0:
            Source.reloaded = False
        new = Bullet(x,y)
        new.SetDir(Source)
        RelativeMotionList.append(new)
        AllSprites.append(new)
        bulletlist.append(new)
        Bullet_Group.add(new)


def killBullet(bullet):
    if bullet not in RelativeMotionList:
        pass
    else:
        RelativeMotionList.remove(bullet)
    if bullet not in AllSprites:
        pass
    else:
        AllSprites.remove(bullet)
    if bullet not in bulletlist:
        pass
    else:
        bulletlist.remove(bullet)

def killZombie(zombie):
    zombieList.remove(zombie)
    RelativeMotionList.remove(zombie)
    AllSprites.remove(zombie) 
    Slide_Collide_Group.remove(zombie) 

def animateChr(grup,L):
    if grup.walkT//10 == 0:
        grup.walkT = 49
    if grup.walkT//10 == 4:
        grup.character = L[0]
    elif grup.walkT//10 == 3:
        grup.character = L[1]
    elif grup.walkT//10 == 2:
        grup.character = L[2]
    elif grup.walkT//10 == 1:
        grup.character = L[3]
    grup.walkT -= 1


def generateOrderedGroup(L):
    new = sorted(L,key=lambda character: (character.y))
    sprite_Group = pygame.sprite.OrderedUpdates()
    for i in new:
        sprite_Group.add(i) 
    return sprite_Group
    
def UpdateMap(Source,grup1,grup2):
    if pygame.sprite.spritecollide(Source,grup2,False,False):
        print('hit')
        print('XXXXXXXXXXXXXXX')
    for sprit in RelativeMotionList:
        if Source.dirs == [0,0,1,0]:
            sprit.x += Source.vx
            sprit.updateChr()
            MainCh.updateChr()
            if pygame.sprite.spritecollide(Source,grup1,False,False):
                sprit.y -= Source.vy
            elif pygame.sprite.spritecollide(Source,grup2,False,False):
                sprit.x -= Source.vx 
                MainCh.updateChr()
                #sprit.y -= Source.vy
        elif Source.dirs == [0,0,0,1]:
            sprit.x -= Source.vx
            MainCh.updateChr()
            sprit.updateChr()
            if pygame.sprite.spritecollide(Source,grup1,False,False):
                sprit.y += Source.vy
            elif pygame.sprite.spritecollide(Source,grup2,False,False):
                #sprit.y += Source.vy
                sprit.x += Source.vx 
                MainCh.updateChr()
        elif Source.dirs == [1,0,0,0]:
            sprit.y += Source.vy
            sprit.updateChr()
            MainCh.updateChr()
            if pygame.sprite.spritecollide(Source,grup1,False,False):
                sprit.x -= Source.vx
            elif pygame.sprite.spritecollide(Source,grup2,False,False):
                #sprit.x -= Source.vx
                sprit.y -= Source.vy 
                MainCh.updateChr()
        elif Source.dirs == [0,1,0,0]:
            sprit.y -= Source.vy
            sprit.updateChr()
            MainCh.updateChr()
            if pygame.sprite.spritecollide(Source,grup1,False,False):
                sprit.x += Source.vx
            elif pygame.sprite.spritecollide(Source,grup2,False,False):
                #sprit.x += Source.vx
                sprit.y += Source.vy 
                MainCh.updateChr()
# REDRAW-----------------------------------------------------------------------------
def redrawGame(screen,Back):
    sprite_Group = generateOrderedGroup(AllSprites)
    sprite_Group.update(width,height)
    screen.blit(Back.img,(Back.x, Back.y))
    pygame.draw.rect(screen,(255,0,0),(MainCh.x,MainCh.y,MainCh.width,MainCh.height))
    pygame.draw.rect(screen,(0,255,0),(Car.x,Car.y,Car.width,Car.height))
    sprite_Group.draw(screen)
    
    pygame.display.flip()

# MAIN LOOP-----------------------------------------------------------------
Car = Obstacle(75,75,'car')
Car.genObstacle()
while playing:
    clock.tick(10)
    for event in pygame.event.get():
        # SINGLE BUTTON PRESSES 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                genZombie()
            if event.key == pygame.K_SPACE:
                genBullet(MainCh,width//2,height//2)
            if event.key == pygame.K_z:
                MainCh.reloading = True
            if event.key == pygame.K_v:
                genTestZombie(100,100)
        if event.type ==   pygame.QUIT:
            playing = False
    # CONTINUOUS BUTTON PRESSES
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_UP]:
        MainCh.dirs = [1,0,0,0]
        MainCh.updateChr()
        UpdateMap(MainCh,Slide_Collide_Group,Stop_Collide_Group)
        
    if keys[pygame.K_DOWN]:
        MainCh.dirs = [0,1,0,0]
        
        UpdateMap(MainCh,Slide_Collide_Group,Stop_Collide_Group)
        MainCh.updateChr()
    if keys[pygame.K_LEFT]:
        MainCh.dirs = [0,0,1,0]
        UpdateMap(MainCh,Slide_Collide_Group,Stop_Collide_Group)
        MainCh.updateChr()
    if keys[pygame.K_RIGHT]:
        MainCh.dirs = [0,0,0,1]
        UpdateMap(MainCh,Slide_Collide_Group,Stop_Collide_Group)
        MainCh.updateChr()
    
    # THIS GENERATES NEW ZOMBIES
    
    if MainCh.reloading:
        MainCh.reloadGun()

    for zombie in zombieList:
        Slide_Collide_Group.remove(zombie)
        zombie.follow(MainCh.x,MainCh.y,MainCh,Stop_Collide_Group)
        zombie.updateChr(Bullet_Group)
        Slide_Collide_Group.add(zombie)

    for bullet in bulletlist:
        bullet.updateChr(Slide_Collide_Group)
    
    Car.updateChr()
        


    # CALLS ON REDRAW ALL 
    redrawGame(screen,Background)



pygame.quit()