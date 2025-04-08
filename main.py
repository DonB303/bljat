import pygame
import math
import sys

# Initialisierung
pygame.init()
WIDTH, HEIGHT = 640, 480
HALF_HEIGHT = HEIGHT // 2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CEIL_COLOR = (100, 100, 100)
FLOOR_COLOR = (50, 50, 50)
WALL_COLOR = (200, 0, 0)

# Weltkarte (1 = Wand, 0 = frei)
MAP = [
    [1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1],
]

TILE_SIZE = 64
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE_SIZE
SCALE = WIDTH // NUM_RAYS

# Spieler
player_x, player_y = 100, 100
player_angle = 0
move_speed = 2
rot_speed = 0.03

# Waffe vorbereiten
gun_idle = pygame.image.load('assets/gun_idle.png')  # Waffe im Idle-Zustand
gun_shoot1 = pygame.image.load('assets/gun_shoot1.png')  # Erster Frame Schuss
gun_shoot2 = pygame.image.load('assets/gun_shoot2.png')  # Zweiter Frame Schuss

# Waffe skalieren (doppelte Größe)
gun_idle = pygame.transform.scale(gun_idle, (gun_idle.get_width() * 6, gun_idle.get_height() * 6))
gun_shoot1 = pygame.transform.scale(gun_shoot1, (gun_shoot1.get_width() * 6, gun_shoot1.get_height() * 6))
gun_shoot2 = pygame.transform.scale(gun_shoot2, (gun_shoot2.get_width() * 6, gun_shoot2.get_height() * 6))

gun_img = gun_idle  # Start mit der Idle-Animation

# Schuss-Status und Animation
shooting = False
shoot_timer = 0

def handle_shooting():
    global gun_img, shoot_timer, shooting  # 'shooting' als global markieren
    if shooting:
        if shoot_timer % 1 == 0:
            gun_img = gun_shoot1  # Zeige den ersten Schuss-Frame
        else:
            gun_img = gun_shoot2  # Zeige den zweiten Schuss-Frame
        
        shoot_timer += 1
        if shoot_timer > 10:  # Nach 10 Frames zurück zum Idle
            shooting = False
            shoot_timer = 0
            gun_img = gun_idle  # Zurück zur Idle-Animation

def ray_casting(screen, px, py, angle):
    start_angle = angle - HALF_FOV
    for ray in range(NUM_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = px + depth * math.cos(start_angle)
            target_y = py + depth * math.sin(start_angle)
            
            # Wand-Trefferprüfung
            map_x, map_y = int(target_x // TILE_SIZE), int(target_y // TILE_SIZE)
            if MAP[map_y][map_x] == 1:
                depth *= math.cos(angle - start_angle)
                wall_height = min(int(PROJ_COEFF / (depth + 0.0001)), HEIGHT)
                pygame.draw.rect(screen, WALL_COLOR,
                                 (ray * SCALE, HALF_HEIGHT - wall_height // 2, SCALE, wall_height))
                break
        start_angle += DELTA_ANGLE

#enemy
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100  # Gesundheit des Gegners
        self.size = 32  # Größe des Gegners
        self.color = (255, 0, 0)  # Rot als Standardfarbe für den Gegner
        self.speed = 1  # Geschwindigkeit des Gegners

    def move(self, player_x, player_y):
        # Einfache KI: Gegner bewegt sich auf den Spieler zu
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 1:  # Wenn der Gegner nicht direkt auf dem Spieler ist
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


# Hauptloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Linksklick
                shooting = True

    # Steuerung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_x += move_speed * math.cos(player_angle)
        player_y += move_speed * math.sin(player_angle)
    if keys[pygame.K_s]:
        player_x -= move_speed * math.cos(player_angle)
        player_y -= move_speed * math.sin(player_angle)
    if keys[pygame.K_a]:
        player_angle -= rot_speed
    if keys[pygame.K_d]:
        player_angle += rot_speed

    screen.fill(BLACK)
    pygame.draw.rect(screen, CEIL_COLOR, (0, 0, WIDTH, HALF_HEIGHT))
    pygame.draw.rect(screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    ray_casting(screen, player_x, player_y, player_angle)

    # Schießen Animation verarbeiten
    handle_shooting()

    # Waffe zeichnen (zentriert unten)
    screen.blit(gun_img, (WIDTH // 2 - 0, HEIGHT - 190))  # Waffe doppelt so groß und positioniert

    pygame.display.flip()
    clock.tick(60)
