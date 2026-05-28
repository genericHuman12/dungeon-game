import pygame

class Menu:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font = pygame.font.SysFont("Arial",40)
        self.txt()

    def txt(self):
        txt = 'PLAY!'
        self.img = self.font.render(txt, False, 'black', 'white')
        self.rect = self.img.get_rect()
        self.rect.center = self.screen_rect.center

    def draw(self):
        if not self.game.active:
            self.screen.blit(self.img, self.rect)