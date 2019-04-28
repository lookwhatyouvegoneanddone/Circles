import pygame
from pygame import *
import Enemies

player_speed = 5
player_radius = 20
screen_width, screen_height = (800, 600)



class LevelHandler():

    def __init__(self):
        self.levelCounter = 1

        self.switcher = {
            1:Level1,
            2:Level2,
            3:Level3
        }

    def firstLevel(self):
        level = Level1()
        return level

    def nextlevel(self):
        if self.levelCounter >= len(self.switcher.keys()):
            self.levelCounter = 1
        else:
            self.levelCounter += 1
        level = self.switcher[self.levelCounter]()
        return level

class Level():

    def __init__(self):
        pass

    def updatelevel(self, player):
        d = {}
        running = True
        lost = False
        # Return enemy pixels then check for loss condition
        for x in range(0, len(self.enemy_list)):
            d['points{0}'.format(x)] = self.enemy_list[x].returnpixels()

        for x in range(0, len(self.enemy_list)):
            for item in d['points{0}'.format(x)][1:]:
                if player.inRadius(item):
                    print('DEAD')
                    running = False
                    lost = True
                    return running, lost

        # Move enemies
        for enemy in self.enemy_list:
            enemy.moveenemy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                lost = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.pressed_left = True
                if event.key == pygame.K_RIGHT:
                    self.pressed_right = True
                if event.key == pygame.K_UP:
                    self.pressed_up = True
                if event.key == pygame.K_DOWN:
                    self.pressed_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.pressed_left = False
                if event.key == pygame.K_RIGHT:
                    self.pressed_right = False
                if event.key == pygame.K_UP:
                    self.pressed_up = False
                if event.key == pygame.K_DOWN:
                    self.pressed_down = False

        if self.pressed_left:
            if player.x > player_radius:
                player.moveplayer(-player_speed, 0)
        if self.pressed_right:
            if player.x < screen_width - player_radius:
                player.moveplayer(player_speed, 0)
        if self.pressed_up:
            if player.y > player_radius:
                player.moveplayer(0, -player_speed)
        if self.pressed_down:
            if player.y < screen_height - player_radius:
                player.moveplayer(0, player_speed)

        if player.y == player_radius:
            lost = True

        return running, lost

    def render(self, screen, player, player2):
        font = pygame.font.SysFont('comicsansms', 36)
        text = font.render('Level: ' + str(self.levelnum), True, (255, 255, 255))        
        screen.fill((50, 50, 50))
        pygame.draw.rect(screen, (50,205,50), (0, 0, screen_width, 10), 0)
        screen.blit(text, [35, 50])

        for enemy in self.enemy_list:
            enemy.drawenemy(screen)

        player.drawplayer(screen)
        player2.drawplayer(screen)

    def handleevents(self, events):
        raise NotImplementedError

class Level1(Level):

    def __init__(self):
        self.enemy_list = [
        Enemies.RectEnemy(0, 200, 15) 
        ]

        self.pressed_left, self.pressed_right, self.pressed_up, self.pressed_down = (False, False, False, False)

        self.levelnum = 1

    def updatelevel(self, player):
        return super().updatelevel(player)

    def render(self, screen, player, player2):
        super().render(screen, player, player2)

class Level2(Level):

    def __init__(self):
        self.enemy_list = [
        Enemies.RectEnemy(0, 200, 15), 
        Enemies.RectEnemy(screen_width, 340, 36, rightward=False),
        Enemies.RectEnemy(0, 480, 15, rightward=False)
        ]

        self.pressed_left, self.pressed_right, self.pressed_up, self.pressed_down = (False, False, False, False)

        self.levelnum = 2

    def updatelevel(self, player):
        return super().updatelevel(player)

    def render(self, screen, player, player2):
        super().render(screen, player, player2)

class Level3(Level):

    def __init__(self):
        self.enemy_list = [
        Enemies.RectEnemy(0, 200, 15), 
        Enemies.RectEnemy(0, 50, 15, rightward=False),
        Enemies.TriangleEnemy(50, 25),
        Enemies.RectEnemy(screen_width, 800, 15),
        Enemies.RectEnemy(screen_width, 650, 22)
        ]

        self.pressed_left, self.pressed_right, self.pressed_up, self.pressed_down = (False, False, False, False)

        self.levelnum = 3

        self.levelheight = screen_height * 2

    def updatelevel(self, player):
        for enemy in self.enemy_list:
            enemy.y = enemy.y + 1
        return super().updatelevel(player)

    def render(self, screen, player, player2):
        super().render(screen, player, player2)