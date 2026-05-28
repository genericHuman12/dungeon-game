import pygame
import pygame.sprite
import math
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        pygame.init()
        self.game=game
        self.screen = game.screen
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.image = pygame.image.load("dungeon game/images/airDude.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.screen.get_rect().center
        self.rect.y += 100
        self.speed = 1
        self.type =1
        self.attacking = False
        self.watering = False
        self.bx = 0
        self.by = 0
        self.slowed = False
        self.tick = 0
        self.health = 3
        self.healthBar = HealthBar(self, game, self.screen)
        self.dmgTimer =0
        

    def update_image(self):
        if self.type==1:
            self.image = pygame.image.load("dungeon game/images/airDude.png").convert_alpha()
        if self.type==2:
            self.image = pygame.image.load("dungeon game/images/earthDude.png").convert_alpha()
        if self.type==3:
            self.image = pygame.image.load("dungeon game/images/fireDude.png").convert_alpha()
        if self.type==4:
            self.image = pygame.image.load("dungeon game/images/waterDude.png").convert_alpha()
    
    def draw(self):
        for earth in self.game.earths:
            earth.d()
        for fire in self.game.fires:
            fire.d()
        for water in self.game.waters:
            water.d()
        for air in self.game.airs:
            air.d()
        self.healthBar.draw()
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.tick += 1
        pos = pygame.mouse.get_pos()
        self.bx,self.by = pos[0], pos[1]
        self.check_border()
        if self.game.active:
            self.movement()
        self.check_attacks()
        self.update_image()
        self.add_projects()
        self.check_health()

    def check_health(self):
        if self.health == 0:
            self.game.active = False
            self.game.reset()

    def check_attacks(self):
        if self.attacking:
            for fire in self.game.fires:
                fire.update()
            for water in self.game.waters:
                water.update()
            for air in self.game.airs:
                air.update()
        if self.type == 4 and self.watering and len(self.game.waters)<=50:
            water = waterBullet(self.rect.centerx,self.bx, self.rect.centery, self.by, self.screen)
            self.attacking = True
            self.game.waters.add(water)

    def movement(self):
        if not self.slowed:
            if self.moving_up == True:
                self.rect.y -= self.speed
            if self.moving_down:
                self.rect.y += self.speed
            if self.moving_right:
                self.rect.x += self.speed
            if self.moving_left == True:
                self.rect.x -= self.speed
        else:
            if self.tick%5 ==0:
                if self.moving_up == True:
                    self.rect.y -= self.speed
                if self.moving_down:
                    self.rect.y += self.speed
                if self.moving_right:
                    self.rect.x += self.speed
                if self.moving_left == True:
                    self.rect.x -= self.speed
        

    def add_projects(self):
        for fire in self.game.fires:
            self.game.projectiles.add(fire)
        for water in self.game.waters:
            self.game.projectiles.add(water)
        for air in self.game.airs:
            self.game.projectiles.add(air)
        

    def check_border(self):
        if self.rect.x<0:
            self.moving_left=False
            if self.type == 4:
                self.moving_right =True
        if self.rect.y<0:
            self.moving_up = False
            if self.type == 4:
                self.moving_down =True
        if self.rect.x>(self.screen.get_rect().width-self.rect.width):
            self.moving_right = False
            if self.type == 4:
                self.moving_left =True
        if self.rect.y>(self.screen.get_rect().height-self.rect.height):
            self.moving_down = False
            if self.type == 4:
                self.moving_up =True
        for wall in self.game.earths:
            for thing in self.game.entities:
                if wall.rect.colliderect(thing.rect):
                    if thing.rect.x<= (wall.rect.x + wall.rect.width):
                        thing.slowed = True
                    if thing.rect.y<=(wall.rect.y + wall.rect.height):
                        thing.slowed = True
                    if (thing.rect.x + thing.rect.width)>=wall.rect.x:
                        thing.slowed = True
                    if (thing.rect.y + thing.rect.height)>=wall.rect.y:
                        thing.slowed = True
                elif not wall.rect.colliderect(thing.rect):
                    thing.slowed =False
                    

    def attack(self, bx,by):
        if self.type ==3 and len(self.game.fires) <3:
            fire = fireBomb(self.rect.centerx,bx, self.rect.centery, by, self.screen)
            self.attacking=True
            self.game.fires.add(fire)
        if self.type ==1 and len(self.game.airs) <1:
            air = airWave(self.rect.centerx,bx, self.rect.centery,by, self.screen)
            self.attacking=True
            self.game.airs.add(air)
        if self.type ==2:
            earth = EarthenWall(bx, by, self.screen)
            if len(self.game.earths) ==1:
                self.game.earths.sprites()[0].kill()
            self.game.earths.add(earth)        
        
        


class fireBomb(pygame.sprite.Sprite):
    def __init__(self, ax, bx, ay, by, screen):
        pygame.sprite.Sprite.__init__(self)
        dx, dy = (bx-ax, by-ay)
        distance = math.sqrt(dx**2+dy**2)
        t = distance/2
        self.ax,self.bx,self.ay,self.by=(ax,bx,ay,by)
        self.stepx, self.stepy = (dx/t, dy/t)
        self.screen = screen
        self.x =ax
        self.y = ay
        self.bx =bx,
        self.by = by
        self.image = pygame.draw.circle(screen, 'red', (self.x,self.y), 25)
        self.rect =self.image
        self.dmg = 60
        self.type = 'fire'

    def d(self):
        if (self.x,self.y) != (self.bx, self.by):
            self.image = pygame.draw.circle(self.screen, 'red', (self.x,self.y), 25)
            
    
    def update(self):
        self.rect =self.image
        self.x += self.stepx
        self.y += self.stepy
        if self.image.x > self.screen.get_rect().width or self.image.x<0 or self.image.y<0 or self.image.y>self.screen.get_rect().height:
            self.kill()

class waterBullet(pygame.sprite.Sprite):
    def __init__(self, ax, bx, ay, by, screen):
        pygame.sprite.Sprite.__init__(self)
        dx, dy = (bx-ax, by-ay)
        distance = math.sqrt(dx**2+dy**2)
        t = distance/2
        self.ax,self.bx,self.ay,self.by=(ax,bx,ay,by)
        self.stepx, self.stepy = (dx/t, dy/t)
        self.screen = screen
        self.bx =bx,
        self.by = by
        self.x =ax
        self.y = ay
        self.image = pygame.draw.circle(screen, 'blue', (self.x,self.y), 1)
        self.rect =self.image
        self.dmg = 1
        self.type = 'water'

    def d(self):
        if (self.x,self.y) != (self.bx, self.by):
            self.image = pygame.draw.circle(self.screen, 'blue', (self.x,self.y), 1)
    
    def update(self):
        self.rect = self.image
        self.x += self.stepx
        self.y += self.stepy
        if self.image.x > self.screen.get_rect().width or self.image.x<0 or self.image.y<0 or self.image.y>self.screen.get_rect().height:
            self.kill()

class airWave(pygame.sprite.Sprite):
    def __init__(self, ax, bx, ay, by, screen):
        pygame.sprite.Sprite.__init__(self)
        dx, dy = (bx-ax, by-ay)
        distance = math.sqrt(dx**2+dy**2)
        t = distance/2
        self.ax,self.bx,self.ay,self.by=(ax,bx,ay,by)
        self.stepx, self.stepy = (dx/t, dy/t)
        self.screen = screen
        self.x =ax
        self.y = ay
        self.bx =bx,
        self.by = by
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        self.image = pygame.image.load("dungeon game/images/airWave.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect =self.image.get_rect()
        self.dmg = 25
        self.type = 'air'


    def d(self):
        if (self.x,self.y) != (self.bx, self.by):
            self.screen.blit(self.image, self.rect)
    
    def update(self):
        self.x += self.stepx
        self.y += self.stepy
        self.rect.centerx, self.rect.centery = self.x,self.y
        if self.rect.x > self.screen.get_rect().width or self.rect.x<0 or self.rect.y<0 or self.rect.y>self.screen.get_rect().height:
            self.kill()

class EarthenWall(pygame.sprite.Sprite):
    def __init__(self, x,y, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.draw.circle(self.screen, 'brown', (x,y), 60)
        self.rect = self.image
        self.rect.centerx = x
        self.rect.centery = y
        self.pos = (x,y)

    def d(self):
        self.image = pygame.draw.circle(self.screen, 'brown', self.pos, 60)

class HealthBar:
    def __init__(self, thing, game, screen):
        self.game = game
        self.screen = screen
        self.thing = thing
        self.oneH = pygame.transform.scale(pygame.image.load('dungeon game/images/heart.png').convert_alpha(), (50,50))
        self.oneHR = self.oneH.get_rect()
        self.twoH = pygame.transform.scale(pygame.image.load('dungeon game/images/heart.png').convert_alpha(), (50,50))
        self.twoHR = self.twoH.get_rect()
        self.threeH = pygame.transform.scale(pygame.image.load('dungeon game/images/heart.png').convert_alpha(), (50,50))
        self.threeHR = self.threeH.get_rect()    
        self.oneHR.topright = self.screen.get_rect().topright
        self.twoHR.topright = self.oneHR.topleft
        self.threeHR.topright = self.twoHR.topleft    

    def draw(self):
        if self.thing.health == 3:
            self.screen.blit(self.oneH, self.oneHR)
            self.screen.blit(self.twoH, self.twoHR)
            self.screen.blit(self.threeH, self.threeHR)
        if self.thing.health == 2:
            self.screen.blit(self.oneH, self.oneHR)
            self.screen.blit(self.twoH, self.twoHR)
        if self.thing.health == 1:
            self.screen.blit(self.oneH, self.oneHR)


