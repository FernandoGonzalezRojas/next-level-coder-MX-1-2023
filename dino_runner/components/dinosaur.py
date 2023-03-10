import pygame

from pygame.sprite import Sprite
from dino_runner.utils.constants import (
    SOUND_JUMP,
    RUNNING,
    DUCKING, 
    JUMPING,
    DEFAULT_TYPE,
    SHIELD_TYPE,
    RUNNING_SHIELD,
    DUCKING_SHIELD,
    JUMPING_SHIELD,
    HAMMER_TYPE,
    DUCKING_HAMMER,
    JUMPING_HAMMER,
    RUNNING_HAMMER,
    HEART_TYPE,
    FONT_ARIAL,
    SCREEN_WIDTH,
    )

class Dinosaur(Sprite):
    POS_X = 80
    POS_Y = 310
    POS_Y_DUCKING = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.run_img = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER, HEART_TYPE: RUNNING}
        self.duck_img = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER, HEART_TYPE: DUCKING}
        self.jump_img = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER, HEART_TYPE: JUMPING}
        self.type = DEFAULT_TYPE
        self.audio_jump = SOUND_JUMP
        self.image = self.run_img[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.POS_X
        self.dino_rect.y = self.POS_Y
        self.step_index = 0
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.time_to_show = 0
        self.setup_states()

    def setup_states(self):
        self.has_power_up = False
        self.shield = False
        self.hammer = False
        self.heart = False
        self.heart_time_up = 0
        self.shield_time_up = 0
        self.hammer_time_up = 0

    def update(self, user_input):
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()

        if user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif user_input[pygame.K_UP]  or user_input[pygame.K_SPACE] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
        elif not self.dino_jump:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

        if self.step_index >= 10:
            self.step_index = 0

    def draw(self, screen, color):
        screen.blit(self.image, self.dino_rect)
        self.draw_time(screen, color)
        

    def run(self):
        self.image = self.run_img[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.POS_X
        self.dino_rect.y = self.POS_Y
        self.step_index += 1
    
    def duck(self):
        self.image = self.duck_img[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.POS_X
        self.dino_rect.y = self.POS_Y_DUCKING
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4 # Salto
            self.jump_vel -= 0.8 # Salto, cuando llega a negativo, baja
            
        if self.jump_vel < -self.JUMP_VEL: # Cuando llega a JUMP_VEL en negativo, este se detiene
            self.audio_jump.play()
            self.dino_rect.y = self.POS_Y
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            

    def check_invincibility(self):
        if self.shield or self.hammer:
            self.time_to_show = round((self.shield_time_up - pygame.time.get_ticks()) / 1000, 2)

            if not self.time_to_show >= 0:
                self.shield = False
                self.hammer = False
                self.update_to_default(SHIELD_TYPE)
                self.update_to_default(HAMMER_TYPE)

    def update_to_default(self, current_type):
        if self.type == current_type:
            self.type = DEFAULT_TYPE
    
    def draw_time(self,screen, color):
        font = pygame.font.Font(FONT_ARIAL, 30)
        if self.time_to_show >= 0:
            text = font.render("Time left: " + str(int(self.time_to_show)), True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH/2, 50))
            screen.blit(text, text_rect)
            