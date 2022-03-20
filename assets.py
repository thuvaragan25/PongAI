import pygame
import neat
import random
import sys
import pickle

pygame.init()

class Button:
    def __init__(self, text, width, height, pos, color):

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = color 

        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius = 13)
        screen.blit(self.text_surf, self.text_rect)
class Paddle:
    def __init__(self, x_c, y_c, color):
        self.x_c = x_c
        self.y_c = y_c
        self.vel = 0
        self.color = color
        self.width = 50
        self.height = 6
        self.rect = pygame.Rect(self.x_c,self.y_c,self.width,self.height)

    def move_left(self):
        self.vel = -5

    def move_right(self):
        self.vel = 5

    def move_stop(self):
        self.vel = 0

    def move(self):
        if self.rect.x + self.rect.width >= WIDTH:
            self.vel = 0 
            self.rect.x = WIDTH - self.rect.width - 1
        if self.rect.x <= 0:
            self.vel = 0
            self.rect.x = 0 + 1
        self.rect = self.rect.move([self.vel, 0])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def get_y(self):
        return self.rect.y

    def get_x(self):
        return self.rect.x
def random_sign():
    i = random.randint(0,1)
    if i == 0:
        return -1
    return 1
class Ball:
    def __init__(self, x_c, y_c, color):
        self.x_c = x_c
        self.y_c = y_c
        self.vel = [random_sign()*4,random_sign()*4]
        self.color = color
        self.width = 10
        self.rect = pygame.Rect(self.x_c,self.y_c,self.width,self.width)

    def change_vel_y(self):
        self.vel[1] = -self.vel[1]

    def change_vel_x(self):
        self.vel[0] = -self.vel[0]
    

    def move(self):
        if self.rect.y <= 0:
            self.change_vel_y()
        elif self.rect.y + self.rect.height >= HEIGHT:
            self.change_vel_y()
        if self.rect.x <= 0 or self.rect.x + self.rect.width > WIDTH:
            self.change_vel_x()
        self.rect = self.rect.move([self.vel[0],self.vel[1]])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def collide(self, paddle):
        return self.rect.colliderect(paddle)

class Obstacle:
    def __init__(self, width, height, color):
        self.x = 20
        self.y = 90
        self.height = height
        self.width = width
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) 
    def movement(self, boundary):
        self.x = random.randint(boundary[0], boundary[2])
        self.y = random.randint(boundary[1], boundary[3])
    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.rect)
    
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

mainClock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)
STAT_FONT = pygame.font.SysFont('calibri', 20)
pygame.display.set_caption("Pong AI")
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))