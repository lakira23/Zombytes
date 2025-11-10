import pygame
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Protoype 2")
clock = pygame.time.Clock()

player = pygame.Rect(375, 375, 50, 50)

speed = 5
running = True

while running:
    clock.tick(60)
    window.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        player.y -= speed
    if keys[K_s] or keys[K_DOWN]:
        player.y += speed
    if keys[K_a] or keys[K_LEFT]:
        player.x -= speed
    if keys[K_d] or keys[K_RIGHT]:
        player.x += speed

    player.clamp_ip(window.get_rect())

    pygame.draw.rect(window, (200, 100, 100), player)
    pygame.display.update()
    #prototype 2

pygame.quit()
