import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

agent_color = (255, 0, 0)
agent_size = 10
agent_position = (100, 500)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, agent_color, (100, 100), agent_size)
    pygame.display.flip()

pygame.quit()