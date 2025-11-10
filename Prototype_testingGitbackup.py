"""COMP 3"""

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
fake_pickup_speed = pygame.USEREVENT + 4
fake_pickup_damage = pygame.USEREVENT + 3
GAME_EXIT = pygame.USEREVENT + 2
HEALTH_ZERO = pygame.USEREVENT + 1 

# VARIABLES
clicking = False

clipboard = [""]

current_player = [""]

current_character = [""]

current_difficulty = ["normal"]
current_colour_blind_status = ["off"]
current_health_bars_status = ["off"]
current_sfx_volume_status = ["on"]
current_music_volume_status = ["on"]


current_weapon = [""]

leaderboard_range = [0,14] #min,max 
leader_board_sorter = ["score"]
leader_board_scores = [["score",0],["survival", 0], ["accuracy", None]]
leaderboard_score_max = [0]

shots_counter = [0,0] #fired, hit

Game_runner = True
FPS = 60
current_screen = {
    'menu': True,
    'leaderboard': False,
    'characters_and_weapons': False,
    'settings': False,
    'game': False,
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

fake_pickup_indicator_timer = pygame.time.get_ticks()

health_decrease_bumper = pygame.time.get_ticks()

score = 0
survival = 0
score = 0
accuracy = 0


# RESOURCES
menu_backdrop = pygame.image.load("ACTUAL/Resources/Images/Menu/menu_img.png")
character_and_weapons_backdrop = pygame.image.load("ACTUAL/Resources/Images/Menu/game&weapons/Character.png")
city_backdrop = pygame.image.load("ACTUAL/Resources/Images/city_backdrop.PNG")
military_backdrop = pygame.image.load("ACTUAL/Resources/Images/military_back_drop.PNG")
country_side_backdrop = pygame.image.load("ACTUAL/Resources/Images/country_side_backdrop.png")
Leaderboard_backdrop = pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/Leaderboard_backdrop.png")
game_backdrop = pygame.image.load("ACTUAL/Resources/Images/Game_back_drop.png")
death_backdrop = pygame.image.load("ACTUAL/Resources/Images/Death_screen_img.png")
settings_backdrop = pygame.image.load("ACTUAL/Resources/Images/Menu/settings/settings_backdrop.png")

character_1 = pygame.image.load("ACTUAL/Resources/Images/character_1.png")
character_2 = pygame.image.load("ACTUAL/Resources/Images/character_2.png")
character_3 = pygame.image.load("ACTUAL/Resources/Images/character_3.png")

creepers_img = pygame.image.load("ACTUAL/Resources/Images/creepers_img.png")

weapon_1 = pygame.image.load("ACTUAL/Resources/Images/Menu/game&weapons/STG-44.png")
weapon_2 = pygame.image.load("ACTUAL/Resources/Images/Menu/game&weapons/Vulcan_cannon.png")
weapon_3 = pygame.image.load("ACTUAL/Resources/Images/Menu/game&weapons/GOL_Sniper_Magnum.png")

easy_button_img = pygame.image.load("ACTUAL/Resources/Images/Menu/Settings/easy_button.png")
hard_button_img = pygame.image.load("ACTUAL/Resources/Images/Menu/Settings/hard_button.png")
normal_button_img = pygame.image.load("ACTUAL/Resources/Images/Menu/Settings/_normal_button.png")
off_button_img = pygame.image.load("ACTUAL/Resources/Images/Menu/Settings/off_button.png")
on_button_img = pygame.image.load("ACTUAL/Resources/Images/Menu/Settings/on_button.png")

Jesey_ten = pygame.font.Font("ACTUAL/Resources/Images/Jersey10-Regular.ttf", 30)

indicator_imgs = [
    ["ACTUAL/Resources/Images/thirst.png",(237,4)],
    ["ACTUAL/Resources/Images/health.png",(522,4)],
    ["ACTUAL/Resources/Images/stamina.png",(237,36)],
    ["ACTUAL/Resources/Images/sanity.png",(522,43)]
]

backdrop_options = [city_backdrop, military_backdrop, country_side_backdrop]
current_game_backdrop = random.choice(backdrop_options)

character_options = [character_1,character_2,character_3]
weapon_options = [weapon_1,weapon_2,weapon_3]

current_weapon[0] = weapon_1
current_character[0] = character_1
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
        
        
        if current_screen["leaderboard"]:
            spl_intention = self.intention.split("_")
            if self.intention.lower() in ['survival_order','score_order','accuracy_order'] and spl_intention[0].lower() == leader_board_sorter[0]:
                self_rect = self.get_rect()
                pygame.draw.rect(window, (200,20,20), pygame.Rect(self_rect.x-2,self_rect.y-2,self_rect.width + 4,self_rect.height + 4))

        intention = self.intention.split(":")
        
        if current_screen["settings"]:
            settings_map = { 
            "difficulty": (current_difficulty, (255, 140, 0)),
            "colour_blind_colours": (current_colour_blind_status, (255, 140, 0)),
            "health_bars": (current_health_bars_status, (255, 140, 0)),
            "sfx_volume": (current_sfx_volume_status, (255, 140, 0)),
            "music_volume": (current_music_volume_status, (255, 140, 0))
        }
            setting_type = intention[0]
            if setting_type in settings_map and settings_map[setting_type][0][0] == intention[1]:
                pygame.draw.rect(window, settings_map[setting_type][1], self.get_rect())

        if current_screen["characters_and_weapons"]: 

            current_character_index = character_options.index(current_character[0])
            current_weapon_index = weapon_options.index(current_weapon[0])
            

            if intention[0] == "set_weapon":
                if int(intention[1]) == current_weapon_index:
                    pygame.draw.rect(window,(58,28,18),self.get_rect())
                

            if intention[0] == "set_character":
                #print(f"test {current_character_index}")
                orginal_dimensions = 126
                tangible_dimension = orginal_dimensions + 30

                if int(intention[1]) == current_character_index:
                    self.image = pygame.transform.scale(self.image,(156,156))
                    self.width,self.height = tangible_dimension,tangible_dimension                
                else:
                    self.image = pygame.transform.scale(self.image,(126,126))
                    self.width,self.height =  orginal_dimensions,orginal_dimensions

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
        global current_player

        if current_screen["leaderboard"]:
            intention = self.intention.split("_")
            if intention[0] == "scroll":
                print(leaderboard_range)
                print(leaderboard_score_max)
                if intention[1] == "up" and leaderboard_range[0] >= 1:
                    leaderboard_range[0] -= 1
                    leaderboard_range[1] -= 1

                if intention[1] == "down" and leaderboard_score_max[0] > 1 and leaderboard_range[0] <= leaderboard_score_max[0]-2:    
                    leaderboard_range[0] += 1
                    leaderboard_range[1] += 1
        
            leaderboard_range[0] = max(0, leaderboard_range[0])
            leaderboard_range[1] = leaderboard_range[0] + 14
# ...existing code...
        if current_screen["settings"]:
            try:
                toggle = self.intention.split(":")[1]
            except:
                pass

            setting_map = {
                "difficulty": current_difficulty,
                "colour_blind_colours": current_colour_blind_status,
                "health_bars": current_health_bars_status,
                "sfx_volume": current_sfx_volume_status,
                "music_volume": current_music_volume_status
            }

            setting_type = self.intention.split(":")[0]
            if setting_type in setting_map:
                setting_map[setting_type][0] = toggle

            print(setting_map)
            
        if current_screen["characters_and_weapons"] == True:

            if self.intention.split(":")[0] == "set_weapon" and clicking:
                image_clicked_i = self.intention.split(":")[1].strip()
                #print(weapon_options.index(current_weapon[0]))
                current_weapon[0] = weapon_options[int(image_clicked_i)]

            if self.intention.split(":")[0] == "set_character" and clicking:
                image_clicked_i = self.intention.split(":")[1].strip()
                

                #changes the characters based on click
                current_character[0] = character_options[int(image_clicked_i)]

        if self.intention[:2] == "go":
            
            if self.intention[3:].lower() == "game":
                current_player[0] = clipboard[0]
                reset_game()  # <-- This resets everything before starting

            for state in current_screen:
                current_screen[state] = False
            current_screen[self.intention[3:].lower()] = True

        if self.intention.endswith("_order"):
            leader_board_sorter[0] = self.intention.replace("_order", "").lower()

class Characters(Object):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)

class Enemy(Characters):
    def __init__(self, size, x_pos, y_pos):
        super().__init__(size, size, x_pos, y_pos)
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 0

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
    
    def get_speed(self):
        return self.speed

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

        #print(f"{self.rect.x} {self.rect.y}")
        # Ensure enemies stay within window bounds
        self.rect.clamp_ip(window.get_rect())

class Enemy_Walkers(Enemy):
    def __init__(self, size, x_pos, y_pos):
        super().__init__(size, x_pos, y_pos)

        self.speed = 2
        self.damage = 2

class Enemy_Crawlers(Enemy):
    def __init__(self, size, x_pos, y_pos):
        super().__init__(size, x_pos, y_pos)

        self.speed = 1.5
        self.damage = 4

class Enemy_Runners(Enemy):
    def __init__(self, size, x_pos, y_pos):
        super().__init__(size, x_pos, y_pos)

        self.speed = 2.5
        self.damage = 1


class User(Characters):
    def __init__(self, height, length, x_pos, y_pos):
        super().__init__(height, length, x_pos, y_pos)
        self.speed = 3.5
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
        elif (self.movements.x == 0 and self.movements.y == 0) and current_time - self.last_stamina_tick >= 150:
            self.stamina = min(self.stamina + 0.5, 100)
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
        global health_decrease_bumper
        health_time_passed = pygame.time.get_ticks() - health_decrease_bumper
        #print(health_time_passed)
        if pygame.Rect.colliderect(enemies.get_rect(),self.get_rect()) or enemies.get_user_enemy_col():
            if health_time_passed > 100: 
                self.health -= enemies.get_damage()
                self.health = int(self.health)
                health_decrease_bumper = pygame.time.get_ticks()
                
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
        image = pygame.Surface((picture_x,picture_y),pygame.SRCALPHA)
        image_x, image_y = 0+frame*picture_x, 0 + row * picture_y
        image.blit(image_var,(0,0),(image_x,image_y,image_x+picture_x,image_y+picture_y))
        image.set_colorkey((0,0,0))
        return image

class Pick_ups(Object):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)
        types = [
            ["antipsychotics","ACTUAL/Resources/Images/antipsycotics.png"],
            ["food","ACTUAL/Resources/Images/food.png"],
            ["damage boosts","ACTUAL/Resources/Images/damage_boosts.png"],
            ["drinks","ACTUAL/Resources/Images/drink.png"],
            ["fake",None]
            ]
        
        self.type = random.choice(types)

        if self.type[1] == None:
            self.image = types[random.randint(0,3)][1]
            
        else:
            self.image = self.type[1]
        
        self.image = pygame.image.load(self.image)


        
        
    def draw(self, screen):
        self.image = pygame.transform.scale(self.image, (self.rect.height, self.rect.width))
        window.blit(self.image,self.get_rect())



    def apply_effect(self, user):
        if self.type[0] == "antipsychotics":
            user.sanity = min(100, user.sanity + 30)
        elif self.type[0] == "food":
            user.stamina = min(100, user.stamina + 30)
        elif self.type[0] == "damage boosts":
            user.damage = min(100, user.damage + 10)
        elif self.type[0] == "drinks":
            user.thirst = min(100, user.thirst + 30)
        elif self.type[0] == "fake":
            user.sanity = max(0, user.sanity - 30)
            print("fake")
            if random.choice([True, False]):
                user.damage = max(5, user.damage - 5)
                pygame.event.post(pygame.event.Event(fake_pickup_damage))
            else:
                user.speed = max(0.5, user.speed - 0.5)
                pygame.event.post(pygame.event.Event(fake_pickup_speed))
        
class Weapon():
    def __init__(self):
        self.max_ammo = None
        self.ammo = self.max_ammo
        self.rps = None
        #self.accuracy = None
        self.damage = None
    
    def get_max_ammo(self):
        return self.max_ammo
    
    def get_ammo(self):
        return self.ammo
    
    def get_rps(self):
        return self.rps

    def get_damage(self):
        return self.damage
       
    
class weapon_one(Weapon): #ak47
    def __init__(self):
        super().__init__()
        self.damage = 20
        self.max_ammo = 20
        self.rps = 5

class weapon_two(Weapon): #machine
     def __init__(self):
        super().__init__()
        self.damage = 10
        self.max_ammo = 40
        self.rps = 10

class weapon_three(Weapon):
     def __init__(self):
        super().__init__()
        self.damage = 40
        self.max_ammo = 8
        self.rps = 1

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
    if current_screen["menu"]:
        menu()
    elif current_screen["characters_and_weapons"]:
        character_and_weapons()
    elif current_screen["leaderboard"]:
        leaderboard()
    elif current_screen["game"]:
        game()
    elif current_screen["settings"]:
        settings()
    elif current_screen["death"]:
        death()

def menu():
    window.blit(menu_backdrop, (0, 0))

    for button in menu_buttons:
        button.set_mouse_pos()
        button.click_rectangle(clicking)
        button.draw_pic(window)
        button.draw_rendered_text(window)

def character_and_weapons():
    window.fill((0,0,0))
    window.blit(character_and_weapons_backdrop, (0,0))

    for button in character_and_weapons_buttons:
        button.set_mouse_pos()
        button.click_rectangle(clicking)
        button.draw_pic(window)
        
def settings():
    window.fill((0,0,0))
    window.blit(settings_backdrop, (0,0))

    for button in settings_buttons:
        button.set_mouse_pos()
        button.click_rectangle(clicking)
        button.draw_pic(window)


def leaderboard():
    window.blit(Leaderboard_backdrop, (0, 0))
    entries = []

    for button in leaderboard_buttons:
        button.set_mouse_pos()
        button.click_rectangle(clicking)
        button.draw_pic(window)
  
    y_offset = 300

    score_file = open("leaderboard","r")
    

    for line in score_file:   
        entry = ast.literal_eval(line.strip())  # Safely convert string to list
        score_dict = {item[0].lower(): item[1] for item in entry}
        entries.append(score_dict)

    leaderboard_score_max[0] = len(entries)
    
    entries_sorted = sorted(entries,
        key = lambda x: float(x.get(leader_board_sorter[0])),
        reverse= True
    )

    try:
        for each_line in range(leaderboard_range[0],leaderboard_range[1]):
            name = entries_sorted[each_line].get("name")
            if not name.strip(): name = "UNKNOWN"
            sort_value = entries_sorted[each_line].get(leader_board_sorter[0], "N/A")

            value = Jesey_ten.render(str(name), True, (255, 255, 255))
            window.blit(value, (41, y_offset))

            value = Jesey_ten.render(str(sort_value), True, (255, 255, 255))
            window.blit(value, (400, y_offset))

            y_offset += 30
    except:
        pass

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
    
    current_player[0] = clipboard[0]
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

    #
    for each_indicator in indicator_imgs:
        window.blit(pygame.image.load(each_indicator[0]),(each_indicator[1]))
    
    # Improved bullet firing: only fire once per click, left or right mouse button
    mouse_buttons = pygame.mouse.get_pressed()
    global last_mouse_state
    if 'last_mouse_state' not in globals():
        last_mouse_state = (False, False, False)
    # Fire on left or right click (button 0 or 2), only on the transition from not pressed to pressed
    if (mouse_buttons[0] and not last_mouse_state[0]) or (mouse_buttons[2] and not last_mouse_state[2]):
        bullets.append(Bullet(user.get_rect().center, pygame.mouse.get_pos()))
        shots_counter[0] += 1
        
    last_mouse_state = mouse_buttons
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

    pygame.draw.rect(window,(0,0,0), user.get_rect())

    user.draw_animation(window, current_character[0], current_frame, user.direction_row)
    
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

            enemy_type = random.choice(['walkers','crawlers','runners'])
            print(enemy_type)

            if enemy_type == 'walkers':
               enemies.append(Enemy_Walkers(ENEMY_SIZE, x, y))
            elif enemy_type == 'crawlers':
                enemies.append(Enemy_Crawlers(ENEMY_SIZE, x, y))
            elif enemy_type == 'runners':
                enemies.append(Enemy_Runners(ENEMY_SIZE, x, y))
            else:
                pass

        enemy_spawn_timer = pygame.time.get_ticks()

    global pickup_spawn_timer, pickup_spawn_delay

    if pygame.time.get_ticks() - pickup_spawn_timer > pickup_spawn_delay:
        pickup_x = random.randint(game_rect.left, game_rect.right - 20)
        pickup_y = random.randint(game_rect.top, game_rect.bottom - 20)
        pick_ups.append(Pick_ups(60, 60, pickup_x, pickup_y))
        
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
            ["Name", current_player[0]],
            ["survival", str(round(leader_board_scores[1][1], 1))],
            ["score", int(leader_board_scores[0][1])],
            ["accuracy", int(leader_board_scores[2][1])]
        ]

        with open("leaderboard", "a") as file:
            file.write(str(score_entry) + "/n")
        
        death_logged = True
    
    window.blit(death_backdrop, (0, 0))

    go_back = Buttons("go menu",186,40,42,724,pygame.image.load("ACTUAL/Resources/Images/Menu/Game_start_button_img.png"))
    go_back.set_mouse_pos()

    # Display text stats
    name_text = Jesey_ten.render(f"Name: {current_player[0]}", True, (255, 255, 255))
    score_text = Jesey_ten.render(f"Score: {int(leader_board_scores[0][1])}", True, (255, 0, 0))
    survival_text = Jesey_ten.render(f"Survival Time: {round(leader_board_scores[1][1], 1)}s", True, (255, 255, 0))
    accuracy_text = Jesey_ten.render(f"Accuracy: {int(leader_board_scores[2][1])}%", True, (0, 255, 0))

    window.blit(name_text, (50, 400))
    window.blit(score_text, (50, 440))
    window.blit(survival_text, (50, 480))
    window.blit(accuracy_text, (50, 520))

    # Blit user character at exact position
    window.blit(current_character[0], (603, 634), (0, 0, 64, 64))

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



###################### Menu Buttons Setup

menu_buttons = [
    Buttons('go_game', 186, 40, 307, 234, pygame.image.load("ACTUAL/Resources/Images/Menu/Game_start_button_img.png")),
    Buttons('Name', 152, 44, 324, 512, pygame.image.load("ACTUAL/Resources/Images/Menu/name_button_img.png")),
    Buttons('go_Leaderboard', 174, 44, 313, 564, pygame.image.load("ACTUAL/Resources/Images/Menu/leaderboard_button_img.png")),
    Buttons('go_Characters_and_weapons', 298, 45, 251, 616, pygame.image.load("ACTUAL/Resources/Images/Menu/character_and_weapons_buttons_img.png")),
    Buttons('go_Settings', 120, 44, 340, 670, pygame.image.load("ACTUAL/Resources/Images/Menu/settings_button_img.png")),
    Buttons('Exit', 35, 31, 9, 14, pygame.image.load("ACTUAL/Resources/Images/Menu/Exit_button_png.png"))
]

######Leaderboard buttons

leaderboard_buttons = [
    Buttons('survival_order', 148, 27, 161, 189, pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/Survival_time_order_button_img.png")),
    Buttons('Score_order', 149, 27, 326, 189, pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/Total_score_order_button_img.png")),
    Buttons('Accuracy_order', 148, 27, 492, 189, pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/Accuracy_order_button_img.png")),
    Buttons('go_menu', 102, 47, 662, 741, pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/Back_button_img.png")),
    Buttons('scroll_down',38,44,77,741,pygame.transform.flip(pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/arrow.png"),False,True)),
    Buttons('scroll_up',38,44,31,741,pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/arrow.png"))
]


###

character_and_weapons_buttons = [
    Buttons("go_menu",102, 47, 662, 741, pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/Back_button_img.png")),
    Buttons(f"set_character:0", 126,126,80,530,pygame.transform.scale(User.get_sprite_animation(character_1,0,64,64,0),(126,126))),
    Buttons(f"set_character:1", 126,126,320,530,pygame.transform.scale(User.get_sprite_animation(character_2,0,64,64,0),(126,126))),
    Buttons(f"set_character:2", 126,126,580,530,pygame.transform.scale(User.get_sprite_animation(character_3,0,64,64,0),(126,126))),
    Buttons(f"set_weapon:0", 197, 74, 39,245, weapon_1),
    Buttons(f"set_weapon:1", 169, 106,315,229,weapon_2 ),
    Buttons(f"set_weapon:2", 209,57,538,262, weapon_3)
]

settings_buttons = [
    Buttons("go_menu",102, 47, 662, 741, pygame.image.load("ACTUAL/Resources/Images/Menu/Leaderboard/Back_button_img.png")),
    
    Buttons("difficulty:easy",95,29,353,318,easy_button_img),
    Buttons("difficulty:normal",95,29,460,318,normal_button_img),
    Buttons("difficulty:hard",95,29,567,318,hard_button_img),

    Buttons("colour_blind_colours:on",95,29,353,359,on_button_img),
    Buttons("colour_blind_colours:off",95,29,460,359,off_button_img),

    Buttons("health_bars:on",95,29,353,399,on_button_img),
    Buttons("health_bars:off",95,29,460,399,off_button_img),

    Buttons("sfx_volume:on",95,29,353,439,on_button_img),
    Buttons("sfx_volume:off",95,29,460,439,off_button_img),

    Buttons("music_volume:on",95,29,353,479,on_button_img),
    Buttons("music_volume:off",95,29,460,479,off_button_img)
]

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

    cursor_image = pygame.image.load("ACTUAL/Resources/Images/curser.png")
    cursor_image = pygame.transform.scale(cursor_image, (20, 20))
    curser = Object(20, 20, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == GAME_EXIT:
            Game_runner = False
            pygame.quit()
            sys.exit()

        if event.type == fake_pickup_speed:
            fake_pickup_speed = pygame.time.get_ticks() 

        if event.type == fake_pickup_damage:
            fake_pickup_speed = pygame.time.get_ticks()


        if event.type == HEALTH_ZERO:
            for state in current_screen:
                current_screen[state] = False
            current_screen["death"] = True 

        if event.type == MOUSEBUTTONDOWN :
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
