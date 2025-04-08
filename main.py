# Imports
import sys
import os
import pygame
from pygame.locals import *
import math
import time

# Initialisierung
pygame.init()
pygame.display.set_caption("Bro u gay")

# Bildschirm-Variablen
WIDTH, HEIGHT = 800, 448
W_WIDTH, W_HEIGHT = 800, 448
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), RESIZABLE)  # Normaler Fenstermodus
surface = pygame.Surface((WIDTH, HEIGHT))

# Clock
fps = 60
fpsClock = pygame.time.Clock()

# Spieler-Variablen
player = pygame.image.load('player.png')
player_rect = player.get_rect()  # Rechteck für den Spieler, um die Position zu verfolgen
xp, yp = 50, 50
vel = 5

# Cursor-Image laden
cursor_image = pygame.image.load('assets/cursor.png')  # Cursor-Bild
cursor_rect = cursor_image.get_rect()

# Maus-Position lock
pygame.mouse.set_visible(False)  # Mauszeiger unsichtbar machen

# Projektile
projectiles = []
bullet_image = pygame.image.load('assets/bullet.png')  # Lade das Projektilbild

# Munition und Feuerrate
max_ammo = 100  # Maximale Munition
ammo = max_ammo  # Aktuelle Munition
fire_rate = 0.05  # Feuerrate (Sekunden pro Schuss)
last_shot_time = 0  # Zeit des letzten Schusses
reload_time = 4  # Nachladezeit in Sekunden
last_reload_time = 0  # Zeit des letzten Nachladens
is_reloading = False  # Nachladen ist inaktiv zu Beginn

#Timemap
TILE_SIZE = 16

tiles = {
    0: pygame.image.load("assets/tiles/grasstile.png"), #Grass
    1: pygame.image.load("assets/tiles/groundtile.png"), #Ground
    2: pygame.image.load("assets/tiles/watertile.png"), #Water
}

tilemap = [
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
]

# Game Loop
while True:
    # Hintergrundfarbe
    surface.fill((0, 225, 0))

    # Quit-Funktion (damit du das Spiel mit ESC oder dem Kreuz schließen kannst)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # ESC-Taste zum Beenden
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            # Nachladen mit der R-Taste
            if event.key == K_r and not is_reloading and ammo < max_ammo:
                is_reloading = True
                last_reload_time = time.time()  # Nachladen starten

    # Maus-Position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Berechnung des Winkels zwischen dem Spieler und der Maus
    dx = mouse_x - (xp + player_rect.width / 2)  # Spieler-Mitte für Drehung
    dy = mouse_y - (yp + player_rect.height / 2)
    angle = math.degrees(math.atan2(dy, dx))  # Winkel in Grad

    # Drehen des Spieler-Bildes
    rotated_player = pygame.transform.rotate(player, -angle)  # Negativ, weil Pygame im Uhrzeigersinn dreht
    rotated_rect = rotated_player.get_rect(center=(xp + player_rect.width // 2, yp + player_rect.height // 2))

    # Tastenregistrierung für Bewegung
    Keys = pygame.key.get_pressed()
    if Keys[pygame.K_d]:
        xp += vel
    elif Keys[pygame.K_a]:
        xp -= vel
    elif Keys[pygame.K_w]:
        yp -= vel
    elif Keys[pygame.K_s]:
        yp += vel

    # Schießen (linke Maustaste gedrückt und Munition vorhanden)
    if pygame.mouse.get_pressed()[0] and ammo > 0 and not is_reloading:
        current_time = time.time()
        if current_time - last_shot_time >= fire_rate:  # Überprüfe Feuerrate
            # Berechnung des Winkels zwischen dem Spieler und der Maus
            angle = math.degrees(math.atan2(dy, dx))
            # Erstellen eines neuen Projektils
            speed = 20  # Geschwindigkeit des Projektils
            projectiles.append({
                'x': xp + player_rect.width / 2,
                'y': yp + player_rect.height / 2,
                'angle': angle,
                'speed': speed
            })
            ammo -= 1  # Munitionsverbrauch
            last_shot_time = current_time  # Update der letzten Schusszeit

    # Nachladen-Logik
    if is_reloading:
        if time.time() - last_reload_time >= reload_time:
            ammo = max_ammo  # Munition auf Maximum setzen
            is_reloading = False  # Nachladen beendet

    # Bewege alle Projektile
    for projectile in projectiles[:]:
        # Berechne die Bewegung des Projektils basierend auf dem Winkel
        proj_dx = math.cos(math.radians(projectile['angle'])) * projectile['speed']
        proj_dy = math.sin(math.radians(projectile['angle'])) * projectile['speed']

        projectile['x'] += proj_dx
        projectile['y'] += proj_dy

        # Entferne Projektile, die aus dem Bildschirm rausgehen
        if not (0 <= projectile['x'] <= WIDTH and 0 <= projectile['y'] <= HEIGHT):
            projectiles.remove(projectile)

    #DRAW ON SCREEN

    for rowindex, row in enumerate(tilemap):
        for colindex, tile_id in enumerate(row):
           x = colindex * TILE_SIZE
           y = rowindex * TILE_SIZE
           tile_image = tiles[tile_id]
           surface.blit(tile_image, (x,y))

    # Malen auf dem Bildschirm
    surface.blit(rotated_player, rotated_rect.topleft)  # Zeichne das gedrehte Bild

    # Zeichne Projektile
    for projectile in projectiles:
        surface.blit(bullet_image, (int(projectile['x']), int(projectile['y'])))  # Zeichne das Projektil als 'bullet.png'

    # Munition anzeigen
    font = pygame.font.Font(None, 36)
    ammo_text = font.render(f'Ammo: {ammo}/{max_ammo}', True, (255, 255, 255))
    surface.blit(ammo_text, (10, 10))

    # Ladebalken für Nachladen
    if is_reloading:
        reload_text = font.render(f'Reloading...', True, (255, 255, 255))
        surface.blit(reload_text, (WIDTH - 150, 10))

    # Bildschirm aktualisieren
    screen.blit(surface, (0, 0))

    # Setze die Position des Cursors auf die Mausposition
    cursor_rect.center = (mouse_x, mouse_y)

    # Zeichne den Cursor auf dem Bildschirm
    screen.blit(cursor_image, cursor_rect.topleft)

    # Bildschirm aktualisieren
    pygame.display.flip()
    fpsClock.tick(fps)
