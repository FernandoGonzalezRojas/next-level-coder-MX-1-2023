import pygame
import random
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, BIRD  

class ObstacleManager:

    def __init__(self):
        self.obstacles = []

    def update(self, game_speed, game):
        if len(self.obstacles) == 0:
            if random.randint(0,1) == 0:   
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif random.randint(0,1) == 1:
                self.obstacles.append(Bird(BIRD))
        
        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                game.heart_manager.reduce_heart()   
                if game.heart_manager.heart_count < 1:
                    pygame.time.delay(300)
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)