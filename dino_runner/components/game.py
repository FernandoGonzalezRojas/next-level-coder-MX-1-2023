import pygame
import random
from dino_runner.utils.constants import (BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_ARIAL, CLOUD, GAME_OVER, DINO_START,RESET)
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacles_manager import ObstacleManager 
from dino_runner.components.player_hearts.heart_manager import HeartManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 15
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_cloud = SCREEN_WIDTH
        self.y_cloud = 100
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.heart_manager = HeartManager()
        self.power_up_manager = PowerUpManager()
        self.alter_color = 500
        self.points = 0
        self.score = 0
        self.game_player = 0
        self.death_count = 0
        self.color_points = ()

    def increase_score(self):
        self.points += 1
        if self.points % 200 == 0:
            self.game_speed += 1
        self.player.check_invincibility()
        
    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self)
        self.power_up_manager.update(self.points, self.game_speed, self.player, self)
        self.increase_score()

    def draw(self):
        self.clock.tick(FPS)
        self.color_inverti()
        self.draw_cloud()
        self.draw_background()
        self.player.draw(self.screen, self.color_points)
        self.obstacle_manager.draw(self.screen)
        self.heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_ARIAL, 30)
        surface = font.render("points:" + str(self.points), True, self.color_points)
        rect = surface.get_rect()
        rect.center = (1000,40)
        self.screen.blit(surface, rect)

    def draw_cloud(self):
        cloud_speed = 5
        image_width = CLOUD.get_width()
        self.screen.blit(CLOUD,(self.x_cloud, self.y_cloud))
        self.screen.blit(CLOUD,(image_width + self.x_cloud, self.y_cloud))
        if self.x_cloud < -image_width:
            self.screen.blit(CLOUD,(image_width + self.x_cloud, self.y_cloud))
            self.x_cloud = 0
       
        self.x_cloud -= cloud_speed   

    def color_inverti(self):
        
        current_time = pygame.time.get_ticks()
        if current_time % 60000 >= 30000:
            self.screen.fill((29,31,35))
            self.color_points = (255,255,255)
            
        else:
            self.screen.fill((255,255,255))
            self.color_points = (0,0,0)
            

    def menu(self):
        font = pygame.font.Font(FONT_ARIAL, 30)
        if self.points >= self.score:
            self.score = self.points
        self.points = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                       self.run()
                        
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        

            self.screen.fill((255,255,255))
            if self.death_count == 0:
                self.screen.blit(DINO_START, (SCREEN_WIDTH // 2 -40, SCREEN_HEIGHT // 2 - 140))
                surface = font.render("Press SPACE to start the game", True, (0,0,0))
            else:
                 self.screen.blit(GAME_OVER,(370, SCREEN_HEIGHT/2 - 150))
                 self.screen.blit(DINO_START, (SCREEN_WIDTH // 2 -40, SCREEN_HEIGHT // 2 - 120))
                 surface = font.render("Maximum score: " + str(self.score), True, (0,0,0))
                 surface_games = font.render("Games: " + str(self.death_count), True, (0,0,0))
                 self.screen.blit(surface_games,(SCREEN_WIDTH/2-40, SCREEN_HEIGHT/2 + 70))
                 self.screen.blit(RESET, (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 150))
            rect = surface.get_rect()
            rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50)
            self.screen.blit(surface, rect)
            pygame.display.update()
            #self.clock.tick(1)