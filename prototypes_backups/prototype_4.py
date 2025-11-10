import pygame
import random
import math
from pygame.locals import *

pygame.init()

HEIGHT,WIDTH = 800,800
window = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("Prototype 3")
clock = pygame.time.Clock()

ENEMY_SIZE = 25
USER_WIDTH = 64
USER_HEIGHT = 64
ENEMY_GAP = 10

enemy_spawn_timer = pygame.time.get_ticks()
enemies_per_round = 1
enemy_speed_max = 2

current_level = 1
level_timer = pygame.time.get_ticks()


enemy_x = random.randint(0, 750)
enemy_y = random.randint(0, 750)

FPS = 60
running = True

####clases

class Object():
    def __init__(self, width, height, x_pos, y_pos):
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.width = width
        self.height = height
        
        self.mouse_pos = [0, 0]

    def get_rect(self):
        return self.rect

    def set_pos_x(self, pos_x):
        self.rect.x = pos_x

    def set_pos_y(self,pos_y):
        self.rect.y = pos_y

    def draw(self, screen, colour):
        pygame.draw.rect(screen, colour, self.get_rect())


    def set_mouse_pos(self):
        self.mouse_pos[0], self.mouse_pos[1] = pygame.mouse.get_pos()

class Characters(Object):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)


class Enemy(Characters):
    def __init__(self, size, x_pos, y_pos, speed):
        super().__init__(size, size, x_pos, y_pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = speed

        self.damage = 0.05
        self.health = 100
        
        self.min_distance = ENEMY_SIZE + ENEMY_GAP + 5
        self.user_enemy_col = False

    def get_user_enemy_col(self):
        return self.user_enemy_col
    
    def get_health(self):
        return self.health
    
    def get_damage(self):
        return self.damage

   
    def update(self, user, enemies):
        user_pos = user.get_rect().center

        # Calculate direction vector from enemy to user
        direction = pygame.math.Vector2(user_pos) - pygame.math.Vector2(self.rect.center)

        distance_to_user = direction.length()

        # Avoid normalizing zero-lengwwwwwth vector and adjust stopping distance logic
        if distance_to_user > self.min_distance:
            if distance_to_user != 0:
                self.user_enemy_col = False
                direction = direction.normalize()

            self.velocity = direction * self.speed
        else:
            # Add a slight hover effect to avoid freezing in place
            self.user_enemy_col = True
            self.velocity *= 0.9

        for other_enemies in enemies:
            if other_enemies != self:
                vector_difference = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(other_enemies.rect.center)
                distance = vector_difference.length()   

                if distance < ENEMY_SIZE + ENEMY_GAP and distance != 0:
                    repulse = vector_difference.normalize() * (ENEMY_SIZE + ENEMY_GAP - distance)
                    self.velocity += repulse * 0.1

        # Update position
        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)

        # Ensure enemies stay within window bounds
        self.rect.clamp_ip(window.get_rect())

class User(Characters):
    def __init__(self, height, length, x_pos, y_pos):
        super().__init__(height, length, x_pos, y_pos)
        self.speed = 2
        self.health = 100
        self.movements  = pygame.math.Vector2(0,0)
        
    
    
    def set_health(self,enemies):
        if pygame.Rect.colliderect(enemies.get_rect(),self.get_rect()) or enemies.get_user_enemy_col():
            self.health -= enemies.get_damage()
            self.health = int(self.health)

    def get_health(self):
        return self.health
           
    
    def handle_keys(self):
        self.movements = pygame.math.Vector2(0, 0)
        pressed_key = pygame.key.get_pressed()

        user_animation_status = False  # assume not moving unless key is pressed

        if pressed_key[K_UP] or pressed_key[K_w]:
            self.movements.y = -self.speed
            user_animation_status = True
        elif pressed_key[K_DOWN] or pressed_key[K_s]:
            self.movements.y = self.speed
            user_animation_status = True

        if pressed_key[K_LEFT] or pressed_key[K_a]:
            self.movements.x = -self.speed
            user_animation_status = True
        elif pressed_key[K_RIGHT] or pressed_key[K_d]:
            self.movements.x = self.speed
            user_animation_status = True

    def update(self):

        self.rect.x += int(self.movements.x)
        self.rect.y += int(self.movements.y)

        self.rect.clamp_ip(window.get_rect())


def game():
    global enemy_spawn_timer,level_timer,current_level,enemies_per_round,enemy_speed_max

    enemy_elapsed_time = pygame.time.get_ticks() - enemy_spawn_timer
    level_elapsed_time = pygame.time.get_ticks() - level_timer

    if level_elapsed_time > 30*1000: #and len(enemies) == 0: 
        enemy_speed_max += 0.2
        enemies.clear()

        enemies_per_round += 0.5

        current_level += 1
        level_timer = pygame.time.get_ticks()
        print(f"next level: this is level {current_level} and it will include {enemies_per_round} enemies per round")

    if enemy_elapsed_time > 6 * 1000 - (current_level * 500):
        for _ in range(int(enemies_per_round)):
            x = random.randint(0, WIDTH - ENEMY_SIZE)
            y = random.randint(0, HEIGHT - ENEMY_SIZE)
            print(f"{_}'s enemy position is {x} and {y} and their max speed in {enemy_speed_max}")
            enemies.append(Enemy(ENEMY_SIZE, x, y,random.uniform(1.5,enemy_speed_max)))

        enemy_spawn_timer = pygame.time.get_ticks()
    user.handle_keys()
    user.update()
    user.draw(window,(255,255,255))

    update_enemies(enemies,user)
###

def update_enemies(enemies,user):
    for enemy in enemies:
        enemy.update(user, enemies)
        color = (153,255,153)  # Default red color
        
        if enemy.get_health() < 25:
            color = (255,0,0)  
        elif enemy.get_health() < 50:
            color = (255,128,0)
        elif enemy.get_health() < 75:
            color = (102,204,0)

        user.set_health(enemy)
        enemy.draw(window, color)
      
###

enemies = []


user = User(USER_WIDTH, USER_WIDTH, 800 // 2, 800 // 2) 

###
while running:
    clock.tick(FPS)
    window.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    game()
    pygame.display.update()

pygame.quit()
