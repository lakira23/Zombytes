"""COMP 3"""
#for next iteration: clicks only right click, limit teh values for teh leaderboard, the name input should only take letters and numbers
#add the logo
# IMPORTS
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS
import sys
import ast
import random
import pygame
from pygame.locals import *
from pygame import mixer

# INITIALIZATION
pygame.init()
mixer.init()

clicking = False
WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT ))
pygame.display.set_caption("ZOMBYTES")
CLOCK = pygame.time.Clock()
pygame.mouse.set_visible(False)

# CUSTOM EVENTS
GAME_EXIT = pygame.USEREVENT + 2
HEALTH_ZERO = pygame.USEREVENT + 1 

# VARIABLES
clicking = False

clipboard = [""]

leader_board_scores = [["score",0],["survival", 0], ["accuracy", None]]

shots_counter = [0,0] #fired, hit

Game_runner = True
FPS = 60
current_screen = {
    'menu': False,
    'leaderboard': False,
    'characters_and_weapons': False,
    'settings': False,
    'game': True,
    'death': False
}

pick_ups = []
enemies = []
bullets = []

death_logged = False

ENEMY_SIZE = 25
USER_WIDTH = 64
USER_HEIGHT = 64
ENEMY_GAP = 10

user_animation_timer = 0
user_animation_status = False

enemy_spawn_timer = pygame.time.get_ticks()
enemies_per_round = 1
enemy_speed_max = 2

pickup_spawn_timer = pygame.time.get_ticks()
pickup_spawn_delay = random.randint(250, 5000)

current_level = 1
level_timer = pygame.time.get_ticks()


# RESOURCES
menu_backdrop = pygame.image.load("ACTUAL/Resources/Images/Menu/menu_img.png")

city_backdrop = pygame.image.load("ACTUAL/Resources/Images/city_backdrop.PNG")

military_backdrop = pygame.image.load("ACTUAL/Resources/Images/military_back_drop.PNG")

country_side_backdrop = pygame.image.load("ACTUAL/Resources/Images/country_side_backdrop.png")

Leaderboard_backdrop = pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/Leaderboard_backdrop.png")

Jesey_ten = pygame.font.Font("ACTUAL/Resources/Images/Jersey10-Regular.ttf", 30)

game_backdrop = pygame.image.load("ACTUAL/Resources/Images/Game_back_drop.png")

death_backdrop = pygame.image.load("ACTUAL/Resources/Images/Death_screen_img.png")

female_user_img = pygame.image.load("ACTUAL/Resources/Images/_female_character_animation.png")

backdrop_options = [city_backdrop, military_backdrop, country_side_backdrop]
current_game_backdrop = random.choice(backdrop_options)


###################### Classes

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


class Buttons(Object):
    def __init__(self, intention, width, height, x_pos, y_pos, image):
        super().__init__(width, height, x_pos, y_pos)
        self.image = image
        self.intention = intention
        self.font = Jesey_ten
        self.rendered_text = None

    def click_rectangle(self, clicking):
        click_rect = pygame.Rect(self.rect.x - 2, self.rect.y - 5, self.width + 10, self.height + 10)

        if self.rect.collidepoint(pygame.mouse.get_pos()) and self.intention != "Name":
            pygame.draw.rect(window, (191, 100, 2), click_rect, 2)

            if clicking:
                if self.intention == "Exit":
                    pygame.event.post(pygame.event.Event(GAME_EXIT))
                else:
                    self.set_intention()

    def draw_pic(self, screen):
        screen.blit(self.image, self.rect)

    def draw_rendered_text(self, screen):
        if self.intention == "Name":
            if len(clipboard[0]) > 0:
                self.rendered_text = self.font.render(clipboard[0], True, (0, 0, 0))
            else:
                self.rendered_text = self.font.render("NAME", True, (0, 0, 0))
            screen.blit(self.rendered_text, (self.rect.x + 15, self.rect.y + 2)) 
    
    def draw_text_button(self,text):
        self.rendered_text = self.font.render(clipboard[0], True, (0, 0, 0))
        window.blit(self.rendered_text, (self.rect.x + 15, self.rect.y + 2)) 
    

    def set_intention(self):
        print(self.intention[:5])
        if self.intention[:2] == "go":
            
            if self.intention[3:].lower() == "game":
                reset_game()  # <-- This resets everything before starting

            for state in current_screen:
                current_screen[state] = False
            current_screen[self.intention[3:].lower()] = True

        
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

    def bullet_collision(self,user_damage):
        if self.health <= 0:
            enemies.pop(enemies.index(self))
            leader_board_scores[0][1] += 10

        for each_bullet in bullets:
            if pygame.Rect.colliderect(each_bullet.get_rect(), self.get_rect()):
                bullets.pop(bullets.index(each_bullet))
                self.health -= user_damage
                shots_counter[1] += 1

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
        self.direction_row = 0
        self.thirst = 100
        self.stamina = 100
        self.sanity = 100
        self.damage = 20
        self.health = 100
        self.movements  = pygame.math.Vector2(0,0)
        
        self.last_stat_tick = pygame.time.get_ticks()
        self.last_stamina_tick = pygame.time.get_ticks()

        self.stat_tick_delay = 1000  # 1 second
        self.last_health_tick = pygame.time.get_ticks()
    
    
    def update_pickups(self):
        for pickup in pick_ups:
            if user.get_rect().colliderect(pickup.get_rect()):
                pickup.apply_effect(self)
                pick_ups.remove(pickup)
            else:
                pickup.draw(window)

    def update_stats(self):
        current_time = pygame.time.get_ticks()

        # Decrease sanity and thirst every second
        if current_time - self.last_stat_tick >= self.stat_tick_delay:
            self.thirst = max(0, self.thirst - 1)
            self.sanity = max(0, self.sanity - 1)
            self.last_stat_tick = current_time

        # Decrease stamina if moving (every 500ms)
        if (self.movements.x != 0 or self.movements.y != 0) and current_time - self.last_stamina_tick >= 150:
            self.stamina = max(0, self.stamina - 1)
            self.last_stamina_tick = current_time

        # If any stat hits zero, decrease health slowly
        if self.thirst == 0 or self.sanity == 0 or self.stamina == 0:
            if current_time - self.last_health_tick >= 500:  # Every 0.5 seconds
                self.health = max(0, self.health - 1)
                self.last_health_tick = current_time

    def if_killed(self):
        if self.health <= 0:
            pygame.event.post(pygame.event.Event(HEALTH_ZERO))

    def get_thirst(self):
        return self.thirst
    
    def get_stamina(self):
        return self.stamina
    
    def get_sanity(self):
        return self.sanity
    
    def set_health(self,enemies):
        if pygame.Rect.colliderect(enemies.get_rect(),self.get_rect()) or enemies.get_user_enemy_col():
            self.health -= enemies.get_damage()
            self.health = int(self.health)
            print("hit",self.health)

    def get_health(self):
        return self.health
    
    
    
    def get_damage(self):
        return self.damage
    
        
    
    def handle_keys(self):
        global user_animation_status
        self.movements = pygame.math.Vector2(0, 0)
        pressed_key = pygame.key.get_pressed()

        user_animation_status = False  # assume not moving unless key is pressed

        if pressed_key[K_UP] or pressed_key[K_w]:
            self.movements.y = -self.speed
            self.direction_row = 3
            user_animation_status = True
        elif pressed_key[K_DOWN] or pressed_key[K_s]:
            self.movements.y = self.speed
            self.direction_row = 0
            user_animation_status = True

        if pressed_key[K_LEFT] or pressed_key[K_a]:
            self.movements.x = -self.speed
            self.direction_row = 1
            user_animation_status = True
        elif pressed_key[K_RIGHT] or pressed_key[K_d]:
            self.movements.x = self.speed
            self.direction_row = 2
            user_animation_status = True

    def update(self):
        self.if_killed()

        self.rect.x += int(self.movements.x)
        self.rect.y += int(self.movements.y)

        self.rect.clamp_ip(game_rect)

    def draw_animation(self, surface, sprite_sheet, frame, direction_row):
        frame_width = 64
        frame_height = 64
        sprite = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        x = frame * frame_width
        y = direction_row * frame_height
        sprite.blit(sprite_sheet, (0, 0), (x, y, frame_width, frame_height))
        surface.blit(sprite, self.rect.topleft)


    def get_sprite_animation(image_var,frame,picture_x,picture_y,row):
        image = pygame.Surface((picture_x,picture_y)).convert_alpha()
        image_x, image_y = 0+frame*picture_x, 0 + row * picture_y
        image.blit(image_var,(0,0),(image_x,image_y,image_x+picture_x,image_y+picture_y))
        image.set_colorkey((0,0,0))
        return image

class Pick_ups(Object):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)
        types = [
            "antipsychotics",
            "food",
            "damage boosts",
            "drinks",
            "fake"
            ]
        
        self.type = random.choice(types)
        self.color = (255, 255, 255) if self.type != "fake" else (255, 0, 0)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def apply_effect(self, user):
        if self.type == "antipsychotics":
            user.sanity = min(100, user.sanity + 30)
        elif self.type == "food":
            user.stamina = min(100, user.stamina + 30)
        elif self.type == "damage boosts":
            user.damage = min(100, user.damage + 10)
        elif self.type == "drinks":
            user.thirst = min(100, user.thirst + 30)
        elif self.type == "fake":
            user.sanity = max(0, user.sanity - 30)
            if random.choice([True, False]):
                user.damage = max(5, user.damage - 5)
            else:
                user.speed = max(0.5, user.speed - 0.5)
        


class Bullet():
    def __init__(self,user_pos,mouse_pos):
        self.mouse_pos = mouse_pos
        self.user_pos = user_pos

        self.colour = (255, 129, 129)

        self.start_pos = pygame.math.Vector2(self.user_pos)
        direction = pygame.math.Vector2(self.mouse_pos) - pygame.math.Vector2(self.start_pos)
        self.velocity = direction.normalize() * 5  
        self.rect = pygame.Rect(self.start_pos.x, self.start_pos.y, 5, 5)

    def get_rect(self):
        return self.rect
    
    def off_screen(self):
        if not pygame.Rect.colliderect(self.rect, game_rect):
            bullets.pop(bullets.index(self))

    def update(self):
        self.start_pos += self.velocity
        self.rect.topleft = self.start_pos

        self.off_screen()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 129, 129), self.rect)

###################### Functions

def current_screen_finder():
    if current_screen["game"]:
        game()
    elif current_screen["death"]:
        death()

     
def update_enemies(enemies,user):
    for enemy in enemies:
        enemy.bullet_collision(user.get_damage())
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
    
def update_bullets(bullets):
    for each_bullet in bullets:
        each_bullet.update()
        each_bullet.draw(window)

def next_levels(level_elapsed_time):
    if level_elapsed_time > 60*1000: 
        return True
               
def game():
    global enemy_spawn_timer, level_timer, enemies_per_round, enemy_speed_max, current_level
    
    window.blit(game_backdrop,(0,0))
    window.blit(current_game_backdrop, game_rect, area=pygame.Rect(0, 0, game_rect.width, game_rect.height))

    leader_board_scores[1][1] += 0.1
    
    score_value = leader_board_scores[0][1]
    wave_value = current_level

    score_text = Jesey_ten.render(f"SCORE : {int(score_value)}", True, (255, 0, 0))
    wave_text = Jesey_ten.render(f"NIGHT : {wave_value}", True, (255, 255, 255))

    # Get center of screen
    score_rect = score_text.get_rect(center=(WIDTH // 2, 25))
    wave_rect = wave_text.get_rect(center=(WIDTH // 2, 55))

    # Blit to screen
    window.blit(score_text, score_rect)
    window.blit(wave_text, wave_rect)
    
    if clicking:
        bullets.append(Bullet(user.get_rect().center,pygame.mouse.get_pos()))
        shots_counter[0] += 1
    enemy_elapsed_time = pygame.time.get_ticks() - enemy_spawn_timer
    level_elapsed_time = pygame.time.get_ticks() - level_timer

    global user_animation_timer

    if user_animation_status:
        user_animation_timer += 1 / 6
        if user_animation_timer >= 4:
            user_animation_timer = 0
        current_frame = int(user_animation_timer)
    else:
        current_frame = 0

    user.draw_animation(window, female_user_img, current_frame, user.direction_row)


    if level_elapsed_time > 30*1000 and len(enemies) == 0: 
        enemy_speed_max += 0.2
        enemies.clear()

        enemies_per_round += 0.5

        current_level += 1
        level_timer = pygame.time.get_ticks()

    if enemy_elapsed_time > 6 * 1000 - (current_level * 500):
        for _ in range(int(enemies_per_round)):
            x = random.randint(0, WIDTH - ENEMY_SIZE)
            y = random.randint(0, HEIGHT - ENEMY_SIZE)
            enemies.append(Enemy(ENEMY_SIZE, x, y,random.uniform(1.5,enemy_speed_max)))

        enemy_spawn_timer = pygame.time.get_ticks()

    global pickup_spawn_timer, pickup_spawn_delay

    if pygame.time.get_ticks() - pickup_spawn_timer > pickup_spawn_delay:
        pickup_x = random.randint(game_rect.left, game_rect.right - 20)
        pickup_y = random.randint(game_rect.top, game_rect.bottom - 20)
        pick_ups.append(Pick_ups(20, 20, pickup_x, pickup_y))
        
        pickup_spawn_timer = pygame.time.get_ticks()
        pickup_spawn_delay = random.randint(5000, 10000)
            
    user.handle_keys()
    user.update()
    user.update_stats()
    user.update_pickups()

    update_enemies(enemies,user)
    update_bullets(bullets)
    
    indicator_level = [
        user.get_thirst(),
        user.get_stamina(),
        user.get_health(),
        user.get_sanity()
    ]

    for each_indicator_i in range(4):
        indicators_backdrop[each_indicator_i].draw(window, (42, 34, 34))
        value = indicator_level[each_indicator_i]
        
        # Resize the indicator width
        filled_width = int((value / 100) * 216)
        indicators[each_indicator_i].width = filled_width
        indicators[each_indicator_i].rect.width = filled_width

        indicators[each_indicator_i].draw(window, indicators_colours[each_indicator_i])


def death():
    global death_logged
    if shots_counter[0] > 0:
        leader_board_scores[2][1] = (shots_counter[1] / shots_counter[0]) * 100
    else:
        leader_board_scores[2][1] = 100

    if not death_logged:
        score_entry = [
            ["survival", str(round(leader_board_scores[1][1], 1))],
            ["score", int(leader_board_scores[0][1])],
            ["accuracy", int(leader_board_scores[2][1])]
        ]

        with open("comp 3/ACTUAL/leaderboard", "a") as file:
            file.write(str(score_entry) + "\n")
        
        death_logged = True
    
    window.blit(death_backdrop, (0, 0))

    go_back = Buttons("go menu",186,40,42,724,pygame.image.load("comp 3/ACTUAL/Resources/Images/Menu/Game_start_button_img.png"))
    go_back.set_mouse_pos()

    # Display text stats
    score_text = Jesey_ten.render(f"Score: {int(leader_board_scores[0][1])}", True, (255, 0, 0))
    survival_text = Jesey_ten.render(f"Survival Time: {round(leader_board_scores[1][1], 1)}s", True, (255, 255, 0))
    accuracy_text = Jesey_ten.render(f"Accuracy: {int(leader_board_scores[2][1])}%", True, (0, 255, 0))

    window.blit(score_text, (50, 440))
    window.blit(survival_text, (50, 480))
    window.blit(accuracy_text, (50, 520))

    # Blit user character at exact position
    window.blit(female_user_img, (603, 634), (0, 0, 64, 64))

    # Blit enemy beside user

    go_back.draw_pic(window)
    go_back.click_rectangle(clicking)

def reset_game():
    global user, enemies, bullets, pick_ups
    global leader_board_scores, shots_counter
    global enemy_spawn_timer, pickup_spawn_timer, pickup_spawn_delay
    global enemies_per_round, enemy_speed_max, current_level, level_timer
    global death_logged
    death_logged = False

    # Reset player
    user = User(USER_WIDTH, USER_WIDTH, WIDTH // 2, HEIGHT // 2)

    # Clear enemies, bullets, pickups
    enemies.clear()
    bullets.clear()
    pick_ups.clear()

    backdrop_options = [city_backdrop, military_backdrop, country_side_backdrop]
    current_game_backdrop = random.choice(backdrop_options)


    # Reset scores and counters
    leader_board_scores = [["score",0],["survival", 0], ["accuracy", None]]
    shots_counter = [0, 0]

    # Reset timers and difficulty
    enemy_spawn_timer = pygame.time.get_ticks()
    pickup_spawn_timer = pygame.time.get_ticks()
    pickup_spawn_delay = random.randint(250, 5000)

    enemies_per_round = 1
    enemy_speed_max = 2
    current_level = 1
    level_timer = pygame.time.get_ticks()



#####game

user = User(USER_WIDTH, USER_WIDTH, WIDTH // 2, HEIGHT // 2) 
level_counter = Object(110,50,WIDTH//2 - 50,10)
game_rect = pygame.Rect(18,108,766,643)

indicators_backdrop = [
    Object(222,20,15,10),
    Object(222,20,15,43),
    Object(222,20,562,10),
    Object(222,20,562,43)
]

indicators = [
    Object(216,14,18,14),
    Object(216,14,18,47),
    Object(216,14,564,14),
    Object(216,14,564,47)
]

indicators_colours = [
    (49,110,131),
    (46,61,65),
    (180,19,19),
    (191,106,2)

]
###################### Main Game Loop

while Game_runner:
    window.fill((0, 0, 0))  # Clear screen before drawing
    CLOCK.tick(FPS)
    clicking = False

    cursor_image = pygame.image.load("comp 3/ACTUAL/Resources/Images/curser.png")
    cursor_image = pygame.transform.scale(cursor_image, (20, 20))
    curser = Object(20, 20, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == GAME_EXIT:
            Game_runner = False
            pygame.quit()
            sys.exit()

        if event.type == HEALTH_ZERO:
            for state in current_screen:
                current_screen[state] = False
            current_screen["death"] = True 

        if event.type == MOUSEBUTTONDOWN:
            clicking = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if current_screen['menu']:
                if event.key == pygame.K_BACKSPACE and len(clipboard[0]) > 0:
                    clipboard[0] = clipboard[0][:-1]
                elif len(clipboard[0]) < 8:
                    clipboard[0] += event.unicode

    current_screen_finder()
    window.blit(cursor_image, curser.get_rect())
    pygame.display.update()
