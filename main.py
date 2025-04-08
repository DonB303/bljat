#Imports
import sys
import os
import pygame
from pygame.locals import *

#Initialization
pygame.init()
pygame.display.set_caption("Bro u gay")

#Screen vars
WIDTH, HEIGHT = 800, 450
W_WIDTH, W_HEIGHT = 800, 450
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), RESIZABLE)
surface = pygame.Surface((WIDTH, HEIGHT))

#Clock 
fps = 60
fpsClock = pygame.time.Clock()

#Player Variables
player = pygame.image.load('player.png')
x = 50
y = 50
vel = 5

# Game Loop
while True:
    #Background colors
    surface.fill((0, 225, 0))

    #Quit function (So that you can exit on press of cross and escape)
    for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
  
    #UPDATE


    #Key Press Registration
    Keys = pygame.key.get_pressed()

    if Keys[pygame.K_d]:
       x += vel
    
    if Keys[pygame.K_a]:
       x -= vel
    
    if Keys[pygame.K_w]:
       y -= vel
    
    if Keys[pygame.K_s]:
       y += vel

    #Paint on screen
    surface.blit(player, (x,y))
    screen.blit(surface, (0,0))

    #Settings
    pygame.display.flip()
    fpsClock.tick(fps)