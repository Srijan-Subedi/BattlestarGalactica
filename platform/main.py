import pygame
import random

pygame.init()

# Screen settings
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

pygame.display.set_caption("Galactica")
clock = pygame.time.Clock()
FPS = 120

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Player settings
player_size = 50
player_x = width // 4
player_y = height - player_size
player_speed = 10

# Enemy settings
enemies = []
enemy_size = 100
enemy_speed = 5
enemy_spawn_delay = 30
enemy_timer = 1

# Image assets
player_image = pygame.image.load("platform/assets/player.png")
player_image = pygame.transform.scale(player_image, (player_size, player_size))

level1_enemy_image = pygame.image.load("platform/assets/level 1 boss.png")
level1_enemy_image = pygame.transform.scale(level1_enemy_image, (enemy_size, enemy_size))
level1_enemy_image = pygame.transform.rotate(level1_enemy_image, 180)

level2_enemy_image = pygame.image.load("platform/assets/level 2 boss.png")
level2_enemy_image = pygame.transform.scale(level2_enemy_image, (enemy_size, enemy_size))
level2_enemy_image = pygame.transform.rotate(level2_enemy_image, 180)

# Bullet settings
bullets = []
enemy_bullets = []
bullet_speed = 10
bullet_width = 5
bullet_height = 10

# Game loop control
running = True

def draw_player(x, y):
    screen.blit(player_image, (x, y))

def draw_player_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

def draw_enemies1():
    for enemy in enemies:
        screen.blit(level1_enemy_image, enemy)

def draw_enemies2():
    for enemy in enemies:
        screen.blit(level2_enemy_image, enemy)

def draw_enemy_bullets():
    for eb in enemy_bullets:
        pygame.draw.rect(screen, RED, eb)

def detect_collisions():
    global enemies, bullets

    # Bullet-enemy collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break

# Game loop
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        bullets.append(pygame.Rect(
            player_x + player_size // 2 - bullet_width // 2,
            player_y,
            bullet_width,
            bullet_height
        ))

    for event in pygame.event.get():
        if event.type == pygame.QUIT \
        or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Update bullets
    bullets = [b.move(0, -bullet_speed) for b in bullets if b.y > 0]

    # Spawn enemies
    enemy_timer += 1
    if enemy_timer >= enemy_spawn_delay:
        enemy_timer = 0
        enemies.append(pygame.Rect(
            random.randint(0, width - enemy_size),
            0,
            enemy_size,
            enemy_size
        ))

    # Move enemies
    enemies = [e.move(0, enemy_speed) for e in enemies if e.y < height]

    # Collision detection
    detect_collisions()

    # Drawing
    draw_player(player_x, player_y)
    draw_player_bullets()
    draw_enemies1()
    draw_enemies2()
    draw_enemy_bullets()

    pygame.display.flip()

pygame.quit()
