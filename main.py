#Imports
import sys
import os
import pygame
from pygame.locals import *

#Initialization
pygame.init()
pygame.display.set_caption("Bro u gay")

#Screen vars
WIDTH, HEIGHT = 640, 480 #<--- change for different Window size
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Clock 
fps = 60
fpsClock = pygame.time.Clock()

player = pygame.image.load('player.png')

x = 50
y = 50
vel = 5

# Game loop.
while True:
    #Background colors
    screen.fill((0, 0, 0))
    #Quit function (So that you can exit on press of cross and escape)
    for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
  
    # Update.

    Keys = pygame.key.get_pressed()

    if Keys[pygame.K_d]:
       x += vel
    
    if Keys[pygame.K_a]:
       x -= vel
    
    if Keys[pygame.K_w]:
       y -= vel
    
    if Keys[pygame.K_s]:
       y += vel

    # Draw.
    screen.blit(player, (x,y))

    pygame.display.flip()
    fpsClock.tick(fps)