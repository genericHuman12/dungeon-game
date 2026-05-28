import pygame
from darkBall import darkBall
from straw import strawDude
from random import choice

class Room(pygame.sprite.Sprite):
    def __init__(self, game, screen, xy, start, strawRNG, ballRNG):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game =game
        self.player = game.player
        self.xy = xy
        self.fighting = True
        self.Lwall = pygame.rect.Rect(0,0,100,self.screen_rect.height)
        self.Twall = pygame.rect.Rect(0,0,self.screen_rect.width,100)
        self.Bwall = pygame.rect.Rect(0, self.screen_rect.height-100, self.screen_rect.width, 100)
        self.Rwall = pygame.rect.Rect(self.screen_rect.width-100,0,100,self.screen_rect.height)
        self.walls =[]
        self.walls.append(self.Lwall)
        self.walls.append(self.Rwall)
        self.walls.append(self.Twall)
        self.walls.append(self.Bwall)
        self.spawn_enemies(strawRNG, ballRNG)
        self.TDimg = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('dungeon game/images/door.png').convert_alpha(), (88.8,100)), 0)
        self.TDrect = self.TDimg.get_rect()
        self.BDimg = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('dungeon game/images/door.png').convert_alpha(), (88.8,100)), 180)
        self.BDrect = self.BDimg.get_rect()
        self.LDimg = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('dungeon game/images/door.png').convert_alpha(), (88.4,100)), 90)
        self.LDrect = self.LDimg.get_rect()
        self.RDimg = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('dungeon game/images/door.png').convert_alpha(), (88.8,100)), 270)
        self.RDrect = self.RDimg.get_rect()
        self.TDrect.midtop = self.screen_rect.midtop
        self.BDrect.midbottom = self.screen_rect.midbottom
        self.LDrect.midleft = self.screen_rect.midleft
        self.RDrect.midright = self.screen_rect.midright

    def spawn_enemies(self, strawRNG, ballRNG):
        straws = choice(strawRNG)
        balls = choice(ballRNG)
        for n in range(1,straws+1):
            self.game.enemies.add(strawDude(self.screen, self.game, ((((self.screen_rect.width-300)*n/straws)),100)) )
        for n in range(1,balls+1):
            self.game.enemies.add(darkBall(self.screen, self.game, ((((self.screen_rect.width-300)*n/balls)),300)) )

    def draw(self):
        for wall in self.walls:
            pygame.draw.rect(self.screen, "grey", wall)
        if not self.fighting:
            self.screen.blit(self.BDimg, self.BDrect)
            self.screen.blit(self.RDimg, self.RDrect)
            self.screen.blit(self.LDimg, self.LDrect)
            self.screen.blit(self.TDimg, self.TDrect)
    
    def update(self):
        if self.player.rect.x<100:
            self.player.moving_left=False
            if self.player.type == 4:
                self.player.moving_right =True
        if self.player.rect.y<100:
            self.player.moving_up = False
            if self.player.type == 4:
                self.player.moving_down =True
        if self.player.rect.x>(self.screen.get_rect().width-100-self.player.rect.width):
            self.player.moving_right = False
            if self.player.type == 4:
                self.player.moving_left =True
        if self.player.rect.y>(self.screen.get_rect().height-100-self.player.rect.height):
            self.player.moving_down = False
            if self.player.type == 4:
                self.player.moving_up =True
        if len(self.game.enemies) == 0:
            self.fighting = False
        else:
            self.fighting =True
        for wall in self.walls:
            for pro in self.game.projectiles:
                if wall.colliderect(pro.rect):
                    pro.kill()

