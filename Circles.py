import pygame
import socket
from threading import Thread
from pygame import *
from enum import Enum
from drawing_functions import AAfilledRoundedRect
import Levels

player_speed = 5
player_radius = 20
screen_width, screen_height = (800, 600)

class PlayerCharacter():

    def __init__(self, x, y, radius,r=139,g=30,b=139):
        self.x = x
        self.y = y
        self.radius = radius
        self.r = r
        self.g = g
        self.b = b

    def drawplayer(self, screen):
        print('afsf')
        pygame.draw.circle(screen, (self.r,self.g,self.b), (self.x, self.y), self.radius)

    def moveplayer(self, xmove, ymove):
        self.x += xmove
        self.y += ymove

    def inRadius(self, coordinate):
        if coordinate[0] >= self.x-self.radius and coordinate[0] <= self.x+self.radius:
            if coordinate[1] >= self.y-self.radius and coordinate[1] <= self.y+self.radius:
                return True
        return False

class UDPInput(Thread):
    def __init__(self,port,screen,player):
        super().__init__()
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('0.0.0.0', self.port))
        self.screen = screen
        self.player = player

    def run(self):
        while True:
            data, addr = self.server.recvfrom(1024)
            input = data.decode()
            x, y = input.split(',')
            self.player.x = int(x)
            self.player.y = int(y)

    def close(self):
        self.server.close()

def runStartScreen(screen, clock, running):
    font = pygame.font.SysFont('comicsansms', 72)
    text = font.render('Start', True, (255, 255, 255))
    startScreen = True
    blue = 20
    green = 240
    blue_up = True
    green_up = False
    rect_height, rect_width = (100, 300)
    rect_x, rect_y = (screen_width/2 - rect_width/2, screen_height/2 - rect_height/2) 
    while startScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                startScreen = False
        if blue == 240:
            blue_up = False
        if blue == 20:
            blue_up = True
        if blue_up:
            blue += 1
        else:
            blue -= 1

        if green == 240:
            green_up = False
        if green == 20:
            green_up = True
        if green_up:
            green += 1
        else:
            green -= 1

        screen.fill((50,green,blue))
        AAfilledRoundedRect(screen, (rect_x, rect_y, rect_width,rect_height), (50,50,50), 0.5)
        screen.blit(text, [300,250])
        pygame.display.update()
        clock.tick(60)

def main():
    
    pygame.init()
    levelHandler = Levels.LevelHandler()
    running = True
    lost = False
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    runStartScreen(screen, clock, running)
    currentLevel = levelHandler.firstLevel()
    player2 = PlayerCharacter(200,200,20,r=255,g=165,b=0)

    UDP_IP_ADDRESS = "192.168.170.67"
    UDP_SERVER_PORT_NO = 9000
    UDP_CLIENT_PORT_NO = 9001

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    serverthread = UDPInput(UDP_CLIENT_PORT_NO, screen, player2)
    serverthread.daemon = True
    serverthread.start()
    packet = 'Start'

    while running:
        player = PlayerCharacter(int(screen_width / 2), screen_height, player_radius)
        lost = False
        try:
            clientSock.sendto(packet.encode(), (UDP_IP_ADDRESS, UDP_SERVER_PORT_NO))
        except:
            pass

        while not lost:
            running, lost = currentLevel.updatelevel(player)
            currentLevel.render(screen, player, player2)
            pygame.display.update()

            clock.tick(60)

        currentLevel = levelHandler.nextlevel()

    pygame.quit()
    serverthread.close()
    quit()


main()