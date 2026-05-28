import pygame
import math
from random import randint

class darkBall(pygame.sprite.Sprite):
    def __init__(self, screen, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('dungeon game/images/enemy1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.game = game
        self.player = game.player
        self.screen = screen
        self.health = 360
        self.spawn = pos
        self.rect.x = self.spawn[0]
        self.rect.y = self.spawn[1]
        self.tick = 0
        self.slowed = False
        self.game.entities.add(self)
        self.healthBar = HealthBar(self, game, screen)
        self.dmgTimer = 0
        self.moving = True
        self.speed = randint(2,5)
        self.speed *= 0.6
    
    def check_walls(self):
        for wall in self.game.room.walls:
            if self.rect.colliderect(wall):
                self.rect.x += self.stepx
                self.rect.y += self.stepy

    def update(self, x,y):
        self.healthBar.text()
        self.tick +=1
        self.check_walls()
        dx, dy = (x-self.rect.centerx, y-self.rect.centery)
        distance = math.sqrt(dx**2+dy**2)
        t = distance
        try:
            self.stepx, self.stepy = (dx/t,dy/t)
        except ZeroDivisionError:
            pass
        if self.moving:
            self.movement()
        self.check_collide()
        if self.health <= 0:
            self.kill()

    def movement(self):
        if not self.slowed:
            if self.tick % (5*self.speed) == 0:
                self.rect.x += self.stepx
                self.rect.y += self.stepy
        if self.slowed:
            if self.tick % (10*self.speed) == 0:
                self.rect.x += self.stepx
                self.rect.y += self.stepy

    def check_collide(self):
        if self.rect.colliderect(self.game.player.rect) and self.game.player.dmgTimer ==0:
            self.game.player.health -= 1
            self.game.player.dmgTimer = 1000
        if self.game.player.dmgTimer != 0:
            self.game.player.dmgTimer -= 1
        for other in self.game.enemies:
            if other == self:
                pass
            else:
                if self.rect.colliderect(other.rect):
                    """self.moving = False
                    other.moving =True
                    This is for later.
                    #from the left-right dir
                    if self.rect.x <= (other.rect.x + other.rect.width):
                        self.moving = False
                    #from the right-left dir
                    elif (self.rect.x + self.rect.width) >= other.rect.x:
                        self.moving = False
                    #from the down-up dir 
                    elif self.rect.y <= (other.rect.y + other.rect.height):
                        self.moving = False
                    #from the up-down dir
                    elif (self.rect.y + self.rect.height) >= other.rect.y:
                        self.moving = False"""
                else:
                    self.moving = True

    def respawn(self):
        self.health = 360
        self.rect.x = self.spawn[0]
        self.rect.y = self.spawn[1]
        
    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.healthBar.draw()

class HealthBar:
    def __init__(self, thing, game, screen):
        self.game = game
        self.screen = screen
        self.thing = thing
        self.font = pygame.font.SysFont('Arial', 15)
        self.text()
        
    def text(self):
        txt = f'{round((self.thing.health*100/360), 0)}'
        self.img = self.font.render(txt, False, 'White', (10,10,10))
        self.rect = self.img.get_rect()
        self.rect.midbottom = self.thing.rect.midtop

    def draw(self):
        self.screen.blit(self.img, self.rect)
