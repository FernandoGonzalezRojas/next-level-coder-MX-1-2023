import pygame
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS

class ObstacleManager:

    def __init__(self):
        self.obstacle = []

    def update(self, game_speed, game):
        if len(self.obstacle) == 0:
            self.obstacle.append(Cactus(SMALL_CACTUS))
        
        for obstacle in self.obstacle:
            obstacle.update(game_speed, self.obstacle)

            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(300)
                game.playing = False
    def draw(self, screen):
        for obstacle in self.obstacle:
            obstacle.draw(screen)