import pygame
import random
from dino_runner.components.obstacles.cactus import CactusSmall, CactusLarge
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, LIVES, GAME_SPEED

class ObstacleManager:

    def __init__(self):
        self.obstacles = []

    def update(self, game_speed, game):
        if len(self.obstacles) == 0:
            if random.randint(0,2) == 0:   
                self.obstacles.append(CactusSmall(SMALL_CACTUS))
            elif random.randint(0,2) == 1:
                self.obstacles.append(CactusLarge(LARGE_CACTUS))
            elif random.randint(0,2) == 2:
                self.obstacles.append(Bird(BIRD))
        
        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield:
                    game.heart_manager.reduce_heart()
                    
                if game.heart_manager.heart_count < 1:
                    pygame.time.delay(300)
                    game.death_count += 1
                    game.game_speed = GAME_SPEED
                    game.heart_manager.heart_count += LIVES
                    game.power_up_manager.when_appears = 0
                    game.menu()
                else:
                    self.obstacles.remove(obstacle)
                    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)