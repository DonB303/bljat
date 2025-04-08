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
W_WIDTH, W_HEIGHT = 800, 448
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), RESIZABLE)
surface = pygame.Surface((WIDTH, HEIGHT))

#Clock 
fps = 60
fpsClock = pygame.time.Clock()

#Player Variables
player = pygame.image.load('player.png')
xp = 50
yp = 50
vel = 5

#Timemap
TILE_SIZE = 16

tiles = {
    0: pygame.image.load("assets/tiles/grasstile.png"),
    1: pygame.image.load("assets/tiles/groundtile.png"),
    2: pygame.image.load("assets/tiles/watertile.png"),
}

tilemap = [
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
]

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
       xp += vel
    
    if Keys[pygame.K_a]:
       xp -= vel
    
    if Keys[pygame.K_w]:
       yp -= vel
    
    if Keys[pygame.K_s]:
       yp += vel

    #PAINT ON SCREEN

    #Tilemap draw
    for rowindex, row in enumerate(tilemap):
        for colindex, tile_id in enumerate(row):
           x = colindex * TILE_SIZE
           y = rowindex * TILE_SIZE
           tile_image = tiles[tile_id]
           surface.blit(tile_image, (x,y))

    #player
    surface.blit(player, (xp,yp))

    screen.blit(surface, (0,0))

    #Settings
    pygame.display.flip()
    fpsClock.tick(fps)