import random
from dino_runner.components.obstacles.obstacle import Obstacle

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        self.y_pos = [230,260,330]
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.y_pos)
        self.step_index = 0

    def draw(self, screen):
        if self.step_index >= 10:
            self.step_index = 0
        screen.blit(self.image[self.step_index//5], self.rect)
        self.step_index += 1