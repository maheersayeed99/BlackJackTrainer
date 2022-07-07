# IMPORTS--------------------------------------------------------------
import sys, pygame
import random
import math
# Helper Functions ----------------------------------------------------

def cyclethru(l):
    r = l.pop(0)
    l.append(r)

# INITIAL VARIABLES----------------------------------------------------
pygame.init()
width = 700
height = 700
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
characterbox = pygame.image.load('lookerl1.png')
charx,chary = characterbox.get_size()

# ANIMATIONS-----------------------------------------------------------------
MainLeft = [pygame.image.load('lookerl11.png'),pygame.image.load('lookerl12.png'),pygame.image.load('lookerl13.png'),pygame.image.load('lookerl14.png')]
MainRight = [pygame.image.load('lookerr11.png'),pygame.image.load('lookerr12.png'),pygame.image.load('lookerr13.png'),pygame.image.load('lookerr14.png')]
MainUp = [pygame.image.load('lookeru11.png'),pygame.image.load('lookeru12.png'),pygame.image.load('lookeru13.png'),pygame.image.load('lookeru14.png')]
MainDown = [pygame.image.load('lookerd11.png'),pygame.image.load('lookerd12.png'),pygame.image.load('lookerd13.png'),pygame.image.load('lookerd14.png')]
ZombLeft = [pygame.image.load('zombl11.png'),pygame.image.load('zombl12.png'),pygame.image.load('zombl13.png'),pygame.image.load('zombl14.png')]
ZombRight = [pygame.image.load('zombr11.png'),pygame.image.load('zombr12.png'),pygame.image.load('zombr13.png'),pygame.image.load('zombr14.png')]
ZombUp = [pygame.image.load('zombu11.png'),pygame.image.load('zombu12.png'),pygame.image.load('zombu13.png'),pygame.image.load('zombu14.png')] 
ZombDown = [pygame.image.load('zombd11.png'),pygame.image.load('zombd12.png'),pygame.image.load('zombd13.png'),pygame.image.load('zombd14.png')]

    
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
    def getrect(self):
        pass
class Tiles(pygame.sprite.Sprite):
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
        self.dirs = [0,0,0,0]
        #Animation Timers
        self.walkT = 49
        self.reloadT = 49
        self.shootT = 49
        self.deathT = 49
        self.lifeT = 199
        #Character States
        self.reloading = False
        self.reloaded = True
        self.automatic = False
        #Attributes
        self.lives = 5
        self.gunlist = ['pistol','shotgun','machinegun']
        self.fullbarrel = 6
        self.bullets = self.fullbarrel
        self.bulletdamage = 1
        self.money = 0
        self.updateChr()
        
    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))

    def reloadGun(self):
        if self.reloadT//10 == 0:
            self.bullets = self.fullbarrel
            self.reloaded = True
            self.reloadT = 49
            self.reloading = False
        self.reloadT -=1
    
    def gunAttrs(self,s):
        if s == 'pistol':
            print('yes')
            self.fullbarrel = 6
            self.bulletdamage = 1
            self.automatic = False
        elif s == 'shotgun':
            print('ye2')
            self.fullbarrel = 2
            self.bulletdamage = 10
            self.automatic = False
        elif s == 'machinegun':
            print('ye3')
            self.fullbarrel = 20
            self.bulletdamage = 2
            self.automatic = True
    
    def changeGun(self):
        cyclethru(self.gunlist)
        self.gunAttrs(self.gunlist[0])
        self.bullets = self.fullbarrel
        self.reloaded = True
        self.reloadT = 49
        self.reloading = False

    def takelife(self):
        if self.deathT//10 == 0:
            self.lives -= 1
            self.deathT = 49
        else:
            self.deathT-=1
        if self.lives <= 0:
            print('dead')
    
    def regenlife(self):
        if self.lives <5:
            if self.lifeT//10 == 0:
                self.lives+=1
                self.lifeT = 199
            else:
                self.lifeT -=1

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
        self.damagerect = pygame.Rect(self.x-5,self.y-5,self.width+10,self.height+10)
        #Character speed and Directions
        self.oldx=0
        self.oldy=0
        self.vx = random.randint(1,3)
        self.vy = random.randint(1,3)
        self.dirs = [0,0,0,0]
        #Animation Timers
        self.walkT = 49
        self.stuckT = 10
        #Attributes
        self.lives = 3
        self.count = 0
        
    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//2),self.width,(self.height//2))
        self.damagerect = pygame.Rect(self.x-5,self.y-5,self.width+10,self.height+10)
    
    def freeZomb(self,s):
        if s == 'side':
            if (self.x == self.oldx) and (self.y == self.oldy):
                self.stuckT-=1
                #print(self.stuckT)
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
                print(self.oldy)
                return False
        elif s == 'top':
            if (self.x == self.oldx) and (self.y == self.oldy):
                self.stuckT-=1
                #print(self.stuckT)
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
                print(self.oldy)
                return False
        
       
            
        

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
        self.getrect()
        for obstacle in ObstacleList:
            obstacle.getrect()
        if pygame.sprite.spritecollide(self,grup,False,False):
            self.x -= negx*self.vx
            if self.count%2 == 0:
                if self.freeZomb('side'):
                    self.y += 3*self.vy
                #if self.y< sprit.y:
                #    self.y += 2*self.vy
                #elif self.y>= sprit.y:
                #    self.y -= 2*self.vy
                #self.stuckT = 5
            #if self.x<=x:
                #if self.y>=
                #self.y -= 2*self.vy

            #elif self.y<y:
                #self.y += 2*self.vy

        if self.depthRect.colliderect(sprit.depthRect):
            self.x -= negx*self.vx



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
        if pygame.sprite.spritecollide(self,grup,False,False):
            self.y -= negy*self.vy
            if self.count%2 ==0:
                if self.freeZomb('top'):
                    self.x -= 3*self.vx
#                if self.x< sprit.x:
#                    self.x -= 2*self.vx
#                elif self.x>= sprit.x:
#                    self.x += 2*self.vx

            

        
        
        
        
        if self.depthRect.colliderect(sprit.depthRect):
            self.y -= negy*self.vy
        
        
        if self.damagerect.colliderect(sprit.rect):
            sprit.takelife()
        
        

    def updateChr(self,grup,Source):
        if pygame.sprite.spritecollide(self,grup,True):
            self.lives -= Source.bulletdamage
        if self.lives <= 0:
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
        self.count+=1
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
        elif s == 'gravestone':
            self.character = pygame.image.load('cars.png')
        elif s == 'wall':
            self.character = pygame.image.load('wall.png')
        self.width, self.height = self.character.get_size()
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.image = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//4),self.width,((self.height//4)*3))
    
    def genObstacle(self):
        RelativeMotionList.append(self) #For relative screen motion
        AllSprites.append(self) 
        Stop_Collide_Group.add(self)
        ObstacleList.append(self)

    def getrect(self):
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.depthRect = pygame.Rect(self.x,(self.y+self.height//4),self.width,((self.height//4)*3))
        #self.rect = pygame.Rect(self.x,(self.y+self.height//2),self.width,self.height//2)

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
ObstacleList = []
TileList = []
TileGroup = pygame.sprite.Group()
Slide_Collide_Group = pygame.sprite.Group()
Stop_Collide_Group = pygame.sprite.Group()
Bullet_Group = pygame.sprite.Group()
AllSprites.append(MainCh)
Background = Bg(0,0)
newwww = Tiles(0,0)



RelativeMotionList.append(Background)
Car = Obstacle(-100,-100,'car')
Car.genObstacle()






# EXTRA FUNCTIONS -----------------------------------------------------------------
def makeBackgroundTiles(w,h):
    TileLocations = []
    tilex = width//w
    tiley = height//h
    for i in range(tilex):
        for j in range(tiley):
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
    elif dirzomb == 2:
        zomby = height+50
        zombx = random.randint(0,width)
    elif dirzomb == 3:
        zombx = -50
        zomby = random.randint(0,height)
    elif dirzomb == 4:
        zombx = width+50
        zomby = random.randint(0,height)
    new = Villain(zombx,zomby)
    zombieList.append(new)
    RelativeMotionList.append(new) #For relative screen motion
    AllSprites.append(new) 
    Slide_Collide_Group.add(new) #for collisions
    if pygame.sprite.spritecollide(new,Stop_Collide_Group,False,False):
        killZombie(new)
        genZombie()

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

def genBulletMach(Source,x,y):
    if Source.reloaded:
        Source.shooting = True
        if Source.shootT//10 == 0:
            Source.bullets-=1
            new = Bullet(x,y)
            new.SetDir(Source)
            RelativeMotionList.append(new)
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
    MainCh.money+=10 

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
    if Source.dirs == [0,0,1,0]:
        for sprit in RelativeMotionList:
            sprit.x += Source.vx
            sprit.getrect()
            MainCh.getrect()
        #if pygame.sprite.spritecollide(Source,grup1,False,False):
        #    sprit.y -= Source.vy
        if pygame.sprite.spritecollide(Source,grup2,False,False):
            for sprit in RelativeMotionList:
                sprit.x -= Source.vx 
                MainCh.getrect()
    elif Source.dirs == [0,0,0,1]:
        for sprit in RelativeMotionList:
            sprit.x -= Source.vx
            MainCh.getrect()
            sprit.getrect()
        #if pygame.sprite.spritecollide(Source,grup1,False,False):
        #    sprit.y += Source.vy
        if pygame.sprite.spritecollide(Source,grup2,False,False):
            for sprit in RelativeMotionList:
                sprit.x += Source.vx 
                MainCh.getrect()
    elif Source.dirs == [1,0,0,0]:
        for sprit in RelativeMotionList:
            sprit.y += Source.vy
            sprit.getrect()
            MainCh.getrect()
        #if pygame.sprite.spritecollide(Source,grup1,False,False):
        #    sprit.x -= Source.vx
        if pygame.sprite.spritecollide(Source,grup2,False,False):
            for sprit in RelativeMotionList:
                sprit.y -= Source.vy 
                MainCh.getrect()
    elif Source.dirs == [0,1,0,0]:
        for sprit in RelativeMotionList:
            sprit.y -= Source.vy
            sprit.getrect()
            MainCh.getrect()
        #if pygame.sprite.spritecollide(Source,grup1,False,False):
        #    sprit.x += Source.vx
        if pygame.sprite.spritecollide(Source,grup2,False,False):
            for sprit in RelativeMotionList:
                sprit.y += Source.vy 
                MainCh.getrect()
    for tile in TileList:
        if (tile.x<0):#(-1*newwww.width)):
            tile.x +=width
        if (tile.x>width):
            tile.x -= width
        if (tile.y<0):
            tile.y += height
        if (tile.y>height):
            tile.y -= height


def drawOverlay():
    screen.blit(pygame.image.load('shadow.png'),(0,0))
    

# REDRAW-----------------------------------------------------------------------------
def redrawGame(screen,Back):
    sprite_Group = generateOrderedGroup(AllSprites)
    sprite_Group.update(width,height)
    TileGroup.update(width,height)
    #screen.blit(Back.img,(Back.x, Back.y))
    screen.fill((0,0,0))
    #pygame.draw.rect(screen,(255,0,0),(MainCh.x,MainCh.y,MainCh.width,MainCh.height))
    #pygame.draw.rect(screen,(0,255,0),(Car.x,Car.y,Car.width,Car.height))
    TileGroup.draw(screen)
    sprite_Group.draw(screen)
    #drawOverlay()
    
    pygame.display.flip()

# MAIN LOOP-----------------------------------------------------------------

makeBackgroundTiles(newwww.width,newwww.height)

while playing:
    clock.tick(40)
    for event in pygame.event.get():
        # SINGLE BUTTON PRESSES 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                genZombie()
            if event.key == pygame.K_SPACE:
                if MainCh.automatic:
                    pass
                else:
                    genBullet(MainCh,width//2,height//2)
            if event.key == pygame.K_z:
                MainCh.reloading = True
            if event.key == pygame.K_b:
                MainCh.changeGun()
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
    if keys[pygame.K_SPACE]:
        if MainCh.automatic == False:
            pass
        else:
            genBulletMach(MainCh,width//2,height//2)
    # THIS GENERATES NEW ZOMBIES
    
    if MainCh.reloading:
        MainCh.reloadGun()

    for zombie in zombieList:
        Slide_Collide_Group.remove(zombie)
        zombie.follow(MainCh.x,MainCh.y,MainCh,Stop_Collide_Group)
        zombie.updateChr(Bullet_Group,MainCh)
        Slide_Collide_Group.add(zombie)

    for bullet in bulletlist:
        bullet.updateChr(Slide_Collide_Group)
    newwww.updateChr()
    Car.updateChr()
    MainCh.regenlife()
    
    #rando = random.randint(1,50)
    #if rando ==1:
    #    genZombie()


    # CALLS ON REDRAW ALL 
    redrawGame(screen,Background)



pygame.quit()