import pygame

class Scoreboard:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font = pygame.font.SysFont('Arial', 30)
        

    def txt(self):
        txt = f'Score: {self.game.vistited_num - 1}'
        self.img = self.font.render(txt, False, 'black', 'grey')
        self.rect = self.img.get_rect()
        self.rect.topleft = self.screen_rect.topleft
        self.screen.blit(self.img, self.rect)