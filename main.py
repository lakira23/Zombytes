import pygame
import random
import math
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Prototype 3")
clock = pygame.time.Clock()

enemy_x = random.randint(0, 750)
enemy_y = random.randint(0, 750)
enemy = pygame.Rect(enemy_x, enemy_y, 40, 40)
player = pygame.Rect(375, 375, 50, 50)

FPS = 60
speed = 5
enemy_speed = 2
running = True

player_health = 100

minimum_distance = player.height

while running:
    clock.tick(FPS)
    window.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed() #uses the keys to affect the user speed.
    if keys[K_w] or keys[K_UP]:
        player.y -= speed
    if keys[K_s] or keys[K_DOWN]:
        player.y += speed
    if keys[K_a] or keys[K_LEFT]:
        player.x -= speed
    if keys[K_d] or keys[K_RIGHT]:
        player.x += speed

    player.clamp_ip(window.get_rect())

    # Vector movement with overlap prevention
    dx = player.centerx - enemy.centerx
    dy = player.centery - enemy.centery
    distance = math.hypot(dx, dy)

    enemy_player_colision = pygame.Rect.colliderect(player, enemy)    

    if player_health <= 0:
        running = False
    else:
        if enemy_player_colision: player_health -= 1
    
    if not enemy_player_colision: 
        dx, dy = dx / distance, dy / distance
        enemy.x += dx * enemy_speed
        enemy.y += dy * enemy_speed

    print("health is ", player_health)

    pygame.draw.rect(window, (200, 100, 100), player)
    pygame.draw.rect(window, (255, 0, 0), enemy)
    pygame.display.update()

	#prototype 3
     
    
pygame.quit() #quits the game
