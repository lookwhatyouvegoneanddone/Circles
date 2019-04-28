import pygame
from pygame import *
from random import *
import random

player_speed = 5
player_radius = 20
screen_width, screen_height = (800, 600)

class EnemyCharacter():
    # Superclass used for all enemies. 
    # Used to define certain functionality that must be 
    # present for every enemy no matter what (move, draw, etc)
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = randint(1,10)

    def drawenemy(self, screen):
        pass

    def moveenemy(self):
        pass

    def returnpixels(self):
        pass

class RectEnemy(EnemyCharacter):

    def __init__(self, x, y, size, rightward=True):
        super().__init__(x, y, size)
        self.rightward = rightward

    def drawenemy(self, screen):
        pygame.draw.rect(screen, (255,50,50), (self.x, self.y, self.size, self.size), 0)

    def moveenemy(self):     
        if self.rightward:
            if self.x > screen_width:
                self.x = 0
            else:
                self.x += self.speed
        else:
            if self.x <= 0:
                self.x = screen_width
            else:
                self.x -= self.speed  

    def returnpixels(self):
        myList =[[]]
        for numx in range(self.x, self.x + self.size):
            for numy in range(self.y, self.y + self.size):
                myList.append([numx, numy])
        return myList

class TriangleEnemy(EnemyCharacter):

    def __init__(self, y, size):
        self.upward = bool(random.getrandbits(1))
        self.rightward = bool(random.getrandbits(1))
        if self.rightward:
            self.x = 0
        else:
            self.x = screen_width
        super().__init__(self.x, y, size)

    def drawenemy(self, screen):
        points = [
        [self.x + self.size/2, self.y],
        [self.x, self.y + self.size],
        [self.x + self.size, self.y + self.size]
        ]
        pygame.draw.polygon(screen, (255,255,0), points, 0)

    def moveenemy(self):
        if self.rightward:
            if self.x > screen_width - self.size:
                self.rightward = False
            else:
                self.x += self.speed
        else:
            if self.x <= 0:
                self.rightward = True
            else:
                self.x -= self.speed    
        if self.upward:
            if self.y <= 0:
                self.upward = False
            else:
                self.y -= self.speed
        else: 
            if self.y >= screen_height - self.size:
                self.upward = True
            else:
                self.y += self.speed

    # Needs updating, still returns a square of pixels rather than a triangle
    def returnpixels(self):
        myList =[[]]
        for numx in range(self.x, self.x + self.size):
            for numy in range(self.y, self.y + self.size):
                myList.append([numx, numy])
        return myList