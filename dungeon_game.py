import pygame
from sys import exit
from player import Player
from straw import strawDude
from darkBall import darkBall
from menu import Menu
from room import Room
from scoreboard import Scoreboard

class Dungeon_Game:
    def __init__(self):
        pygame.init()
        self.rooms = []
        self.active = False
        self.entities = pygame.sprite.Group()
        self.screen = pygame.display.set_mode((1100,900))
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height
        self.player = Player(self)
        self.fires = pygame.sprite.Group()
        self.waters = pygame.sprite.Group()
        self.airs = pygame.sprite.Group()
        self.earths = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.dude1 = darkBall(self.screen, self, (50,50))
        self.dude2 = darkBall(self.screen, self, (300,50))
        self.dude3 = darkBall(self.screen, self, (600,50))
        self.dude4 = darkBall(self.screen, self, (900,50))
        self.menu = Menu(self, self.screen)
        self.entities.add(self.player)
        self.active_room = [0,0]
        self.room =Room(self, self.screen, self.active_room, True, [0,0,1,1,2], [0,0,1,1,2])
        self.rooms.append([0,0])
        self.vistited_num = 1
        self.scoreboard = Scoreboard(self, self.screen)

        

    def run(self):
        while True:
            self.check_events()
            if self.active:
                self.player.update()
                for dude in self.enemies:
                    dude.update(self.player.rect.x, self.player.rect.y)
                self.room.update()
                self.check_doors()
            self.update_screen()
    
    def check_doors(self):
        n=self.vistited_num
        if self.room.fighting == False:
            if self.player.rect.colliderect(self.room.RDrect):
                self.active_room[0] += 1
                self.room.spawn_enemies([n,n,n+1], [n,n,n+1])
                self.vistited_num += 1
                self.player.rect.x = 100
                for earth in self.earths:
                    earth.kill()
            if self.player.rect.colliderect(self.room.LDrect):
                self.active_room[0] -= 1
                self.room.spawn_enemies([n,n,n+1], [n,n,n+1])
                self.vistited_num += 1
                self.player.rect.x = self.screen_width-100-self.player.rect.width
                for earth in self.earths:
                    earth.kill()
            if self.player.rect.colliderect(self.room.TDrect):
                self.active_room[1] += 1
                self.room.spawn_enemies([n,n,n+1], [n,n,n+1])
                self.vistited_num += 1
                self.player.rect.y = self.screen_height-100-self.player.rect.height
                for earth in self.earths:
                    earth.kill()
            if self.player.rect.colliderect(self.room.BDrect):
                self.active_room[1] -= 1
                self.room.spawn_enemies([n,n,n+1], [n,n,n+1])
                self.vistited_num += 1
                self.player.rect.y =100
                for earth in self.earths:
                    earth.kill()
        """if self.active_room not in self.rooms:
            self.room.spawn_enemies([1,1,2], [1,1,2])
            self.rooms.append(self.active_room)
            print(self.rooms)"""

    def update_screen(self):
        self.screen.fill((10,10,10))
        self.room.draw()
        self.scoreboard.txt()
        self.player.draw()
        self.menu.draw()
        for d in self.enemies:
            d.draw()
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                self.check_downs(event)
            if event.type == pygame.KEYUP:
                self.check_ups(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_clicks(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.player.watering = False
        self.check_enemy_hits()

    def check_clicks(self, pos):
        if self.active:
            if self.player.type == 3 or self.player.type == 1 or self.player.type ==2:
                self.player.attack(pos[0], pos[1])
            if self.player.type ==4:
                self.player.watering = True
                self.player.bx,self.player.by = pos[0], pos[1]
        else:
            if self.menu.rect.collidepoint(pos):
                self.active = True

    def reset(self):
        for enemy in self.enemies:
            enemy.respawn()
        for project in self.projectiles:
            project.kill()
        self.player.rect.center = self.screen_rect.center
        self.player.rect.y += 100
        self.player.health = 3
        self.vistited_num = 1
        for e in self.earths:
            e.kill()
        self.player.type =1


    def check_downs(self, event):
        if event.key == pygame.K_q:
            exit()
        if event.key == pygame.K_w:
            self.player.moving_up = True
            if self.player.type ==4:
                self.player.moving_down=False
        if event.key == pygame.K_a:
            self.player.moving_left = True
            if self.player.type ==4:
                self.player.moving_right=False
        if event.key == pygame.K_s:
            self.player.moving_down = True
            if self.player.type ==4:
                self.player.moving_up=False
        if event.key == pygame.K_d:
            self.player.moving_right = True
            if self.player.type ==4:
                self.player.moving_left=False
        if event.key == pygame.K_1:
            self.player.type =1
            self.player_freeze()
        if event.key == pygame.K_2:
            self.player.type =2
            self.player_freeze()
        if event.key == pygame.K_3:
            self.player.type =3
            self.player_freeze()
        if event.key == pygame.K_4:
            self.player.type =4

    def player_freeze(self):
        self.player.moving_down = False
        self.player.moving_up = False
        self.player.moving_right = False
        self.player.moving_left = False

    def check_ups(self, event):
        if self.player.type !=4:
            if event.key == pygame.K_w:
                self.player.moving_up = False
            if event.key == pygame.K_a:
                self.player.moving_left = False
            if event.key == pygame.K_s:
                self.player.moving_down = False
            if event.key == pygame.K_d:
                self.player.moving_right = False

    def check_enemy_hits(self):
        for enemy in self.enemies:
            for projectile in self.projectiles:
                if enemy.rect.colliderect(projectile):
                    enemy.health -= projectile.dmg
                    if projectile.type == 'air':
                        enemy.rect.x -= 100*enemy.stepx
                        enemy.rect.y -= 100*enemy.stepy
                    projectile.kill()
        

jimmy = Dungeon_Game()
jimmy.run()