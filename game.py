import pygame
import sys

import random
from Player import Player
from Enemy import Fighter, Kamikaze, Elite, EnemyBig
from Explosion import Explosion
from Items import Heart, Speed, Lspeed, Attack, Auto, WeaponUp, MissilesItem
from Gamemanager import GameManager, width, height


class Main():
    def __init__(self, width, height):
        
        self.width = width
        self.height = height
        self.gametime = 0
        self.time_over = 0
        self.dt = 0
        self.target_fps = 550
        self.player = Player((self.width/ 2, self.height / 2))
        self.enemies = pygame.sprite.Group()
        self.elasers = pygame.sprite.Group()
        self.missile_explosion = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.enemy_last_spawn = 0
        self.item_last_spawn = 0
        self.powerup_last_spawn = 0
        self.powerup_interval = random.randint(15,40)
        self.iframe = 800
        self.player_get_hit_time = 0
        self.difficulty = "EASY"
        self.wave = "WAVE 1"
        self.dead = False
        self.screenshake = False
        self.shake_timer = 0
        self.offset = [0,0]
        self.difficulty_factor = {"spawn": 1, "speed": 1, "lspeed": 1, "shoot_speed": 1, "hp": 1, "atk": 1}
        self.difficulty_up = 0
        self.player_oof = pygame.mixer.Sound("sounds/hit_sound.mp3")

    def update(self):
        if not self.dead:
            self.player.update(self.width, self.height, self.gametime, self.dt, self.target_fps, self.missile_explosion)
        self.enemies.update(self.player, self.elasers, self.gametime, self.dt, self.target_fps)
        self.elasers.update(self.width, self.height, self.dt, self.target_fps)
        self.explosions.update(self.gametime)
        self.items.update(self.gametime)
        self.generate_enemy()
        self.generate_items()
        self.check_collision()
        self.check_over()
        self.screen_shake()

    def generate_enemy(self):
    
        
        
        if self.difficulty == "EASY":
            if self.wave == "ENDLESS":
                if self.gametime - self.difficulty_up >= 9000:
                    self.difficulty_up = self.gametime
                    self.difficulty_factor["speed"] += 0.005
                    self.difficulty_factor["lspeed"] += 0.0025
                    self.difficulty_factor["shoot_speed"] -= 0.015
                    self.difficulty_factor["hp"] += 0.02
                    self.difficulty_factor["atk"] += 0.02
                    self.difficulty_factor["spawn"] += 0.05
                    # print(self.difficulty_factor) 
            if self.gametime / 1000 < 20:
                if self.gametime - self.enemy_last_spawn > 5000:
                    self.enemy_last_spawn = self.gametime
                    for _ in range(3):
                        self.enemies.add(Fighter(self.difficulty_factor))
                    self.wave = "WAVE 1"
                    
            elif 20 <= self.gametime / 1000 < 40:
                if self.gametime - self.enemy_last_spawn > 5000:
                    self.enemy_last_spawn = self.gametime
                    for _ in range(5):
                        self.enemies.add(Fighter(self.difficulty_factor))
                    self.wave = "WAVE 2"

            elif 40 <= self.gametime / 1000 < 60:
                if self.gametime - self.enemy_last_spawn > 6000:
                    self.enemy_last_spawn = self.gametime
                    for _ in range(4):
                        self.enemies.add(Fighter(self.difficulty_factor))
                    for _ in range(2):
                        self.enemies.add(Elite(self.difficulty_factor))
                    self.wave = "WAVE 3"
            elif 60 <= self.gametime / 1000 < 80:
                if self.gametime - self.enemy_last_spawn > 6000:
                    self.enemy_last_spawn = self.gametime
                    for _ in range(5):
                        self.enemies.add(Fighter(self.difficulty_factor))
                    for _ in range(2):
                        self.enemies.add(Elite(self.difficulty_factor))
                    self.enemies.add(Kamikaze(self.difficulty_factor))
                    self.wave = "WAVE 4"
            elif 80 <= self.gametime / 1000 < 100:
                if self.gametime - self.enemy_last_spawn > 7000:
                    self.enemy_last_spawn = self.gametime
                    for _ in range(3):
                        self.enemies.add(Elite(self.difficulty_factor))
                    for _ in range(3):
                        self.enemies.add(Kamikaze(self.difficulty_factor))
                    
                    self.wave = "WAVE 5"
            elif 100 <= self.gametime / 1000 < 120:
                if self.gametime - self.enemy_last_spawn > 7000:
                    self.enemy_last_spawn = self.gametime
                    for _ in range(7):
                        self.enemies.add(Kamikaze(self.difficulty_factor))
                    
                    self.wave = "WAVE 6"

            elif 120 <= self.gametime / 1000 < 140:
                if self.gametime - self.enemy_last_spawn > 7000:
                    self.enemy_last_spawn = self.gametime
                    for _ in range(5):
                        self.enemies.add(Fighter(self.difficulty_factor))
                    for _ in range(2):
                        self.enemies.add(Elite(self.difficulty_factor))
                    self.enemies.add(EnemyBig(self.difficulty_factor))
                    self.wave = "WAVE 7"
            elif 140 <= self.gametime / 1000 < 160:
                if self.gametime - self.enemy_last_spawn > 7000:
                    self.enemy_last_spawn = self.gametime
                    for _ in range(8):
                        self.enemies.add(Fighter(self.difficulty_factor))
                    for _ in range(6):
                        self.enemies.add(Elite(self.difficulty_factor))
                    for _ in range(3):
                        self.enemies.add(Kamikaze(self.difficulty_factor))
                    for _ in range(1):
                        self.enemies.add(EnemyBig(self.difficulty_factor))
                    self.wave = "WAVE 8"
            else:
                if self.gametime - self.enemy_last_spawn > 10000:
                    self.enemy_last_spawn = self.gametime
                    for _ in range(int(10 * self.difficulty_factor["spawn"])):
                        self.enemies.add(Fighter(self.difficulty_factor))
                    for _ in range(int(7 * self.difficulty_factor["spawn"])):
                        self.enemies.add(Elite(self.difficulty_factor))
                    for _ in range(int(5 * self.difficulty_factor["spawn"])):
                        self.enemies.add(Kamikaze(self.difficulty_factor))
                    for _ in range(int(2 * self.difficulty_factor["spawn"])):
                        self.enemies.add(EnemyBig(self.difficulty_factor))
                    self.wave = "ENDLESS"

    def draw(self, screen):
        if not self.dead:
            self.player.draw(screen, self.offset)
        for i in self.enemies:
            i.draw(screen, self.offset)
        for i in self.elasers:
            i.draw(screen, self.offset)
        self.explosions.draw(screen)
        self.items.draw(screen)
        self.missile_explosion.draw(screen)


    def check_collision(self):
        # print(self.gametime - self.player_get_hit_time)
        
        for i in self.enemies: 
            for j in self.player.lasers: # my laser hit enemy
                if pygame.sprite.collide_rect(i, j):
                    i.hit_by_laser = self.gametime
                    i.damaged = True
                    i.hp -= self.player.atk
                    j.kill()
                    if i.hp >= 1:
                        pygame.mixer.Sound("sounds/hit_sound2.wav").play()
                    if i.hp <= 0:
                        self.create_explosion(i.rect.centerx, i.rect.centery, small_explosion_frames, explosion_sound)
                        
            if pygame.sprite.collide_rect(i, self.player): # enemy player collide
                if isinstance(i, Kamikaze):
                    if (self.gametime - self.player_get_hit_time >= self.iframe):
                        self.player.hp -= i.atk
                    i.kill()
                    self.player.crash = True
                    self.screenshake = True
                    self.player.damaged = True
                    self.shake_timer = self.gametime
                    self.create_explosion(i.rect.centerx, i.rect.centery,small_explosion_frames, explosion_sound)
                    self.player_get_hit_time = self.gametime
                else:
                    if (self.gametime - self.player_get_hit_time >= self.iframe):
                        self.player_get_hit_time = self.gametime
                        self.player.hp -= i.atk * 5
                        i.hp -= self.player.atk * 1.5
                        self.player.crash = True
                        self.screenshake = True
                        self.player.damaged = True
                        self.shake_timer = self.gametime
                        self.create_explosion(i.rect.centerx, i.rect.centery, small_explosion_frames, explosion_sound)
                
        if (self.gametime - self.player_get_hit_time >= 300):
            self.screenshake = False
        
        if (self.gametime - self.player_get_hit_time >= 600):
            self.player.crash = False


        for i in self.elasers:
            if pygame.sprite.collide_rect(self.player, i): # player get hit
                self.player.hit_by_laser = self.gametime
                self.player_oof.play()
                self.player.damaged = True
                self.player.hp -= i.atk
                i.kill()
        
        for i in self.items:
            if pygame.sprite.collide_rect(self.player, i):
                pygame.mixer.Sound("sounds/shine.wav").play()
                i.func(self.player)
                i.kill()

        for i in self.player.missiles:
            if pygame.sprite.spritecollide(i, self.enemies, False):
                i.explode(self.missile_explosion)

        for i in self.missile_explosion:
            for j in self.enemies:
                if pygame.sprite.collide_rect(i, j) and not j.hit_by_explosion:
                    j.hp -= self.player.matk
                    j.hit_by_explosion = True
                    if j.hp >= 1:
                        j.hit_by_laser = self.gametime
                        j.damaged = True
                if j.hp <= 0:
                        self.create_explosion(j.rect.centerx, j.rect.centery, small_explosion_frames, explosion_sound)

        
        # pygame.sprite.groupcollide(self.player.lasers, self.elasers, True, True) # lasers cancel out each other

    def create_explosion(self, x, y, explosion_frames, explosion_sound):
        explosion = Explosion(x,y, explosion_frames, explosion_sound, 100)
        self.explosions.add(explosion)

    def check_over(self):
        global game_state
        global game_over
        if self.player.hp <= 0:
            self.player.hp = 0
            game_state = game_over

    def generate_items(self):
        if self.gametime - self.item_last_spawn > 5000:
            
            items = [Heart(self.width,self.height,self.gametime), Speed(self.width,self.height,self.gametime), Lspeed(self.width,self.height,self.gametime), Attack(self.width,self.height,self.gametime), Auto(self.width,self.height,self.gametime)]
            weights = [0.5, 0.15, 0.15, 0.15, 0.05] if self.wave != "endless" else [0.5, 0.05, 0.05, 0.2, 0.2]
            self.items.add(random.choices(population= items, weights = weights, k=1))
            
            self.item_last_spawn = self.gametime
        
    
        if self.gametime - self.powerup_last_spawn > self.powerup_interval * 1000:
            if self.player.weapon != 4:
                self.powerup_last_spawn = self.gametime
                self.powerup_interval = random.randint(35,60)
                self.items.add(WeaponUp(self.width, self.height, self.gametime))
                self.items.add(MissilesItem(self.width, self.height, self.gametime))
            else:
                 self.powerup_last_spawn = self.gametime
                 self.powerup_interval = random.randint(7,15)
                 self.items.add(MissilesItem(self.width, self.height, self.gametime))
    def screen_shake(self):
        if self.screenshake:
            elapsed_time = self.gametime - self.shake_timer
            if elapsed_time > 10:
                self.shake_time = self.gametime
                self.offset[0] = random.randint(0,16) - 8
                self.offset[1] = random.randint(0,16) - 8
        else:
            self.offset[0] = 0
            self.offset[1] = 0
        
            
    
# Initialize Pygame
pygame.init()
gamemanager = GameManager()

# Set up the window display
screen = pygame.display.set_mode((width, height))
buffer_screen = pygame.Surface((width, height))
pygame.display.set_caption("Gemu")
clock = pygame.time.Clock()
font = pygame.font.Font("gamefont.otf", 36)



set_time_paused = False
dead_animation = False
time_at_paused = 0
time_at_unpaused = 0
game_paused = "paused"
game_over = "game over"
game_running = "running"
game_state = game_running
main_game = Main(width, height)

# set up other sprites
# background image
background = pygame.transform.smoothscale(pygame.image.load("textures/bg5.png").convert(), (width, height))

# explosion sprite
explosion_spritesheet = pygame.image.load("textures/explosion.png").convert_alpha()
explosion_sound = pygame.mixer.Sound("sounds/explosion.ogg")
small_explosion_frames = []
for i in range(0, explosion_spritesheet.get_width(), 32):
    small_explosion_frames.append(explosion_spritesheet.subsurface((i,0,32,32)))


# background music
pygame.mixer.music.load("sounds/centraldogma.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

current_game_time = main_game.gametime

# Game loop
if __name__ == "__main__":
    while 1:
        main_game.dt = clock.tick(550) / 1000
        current_time = pygame.time.get_ticks()
        if (game_state != game_paused):
            gamemanager.gametime = current_time - (time_at_unpaused - time_at_paused) - (time_at_paused - current_game_time)
            main_game.gametime = gamemanager.gametime
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                print("QUIT")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game_state == game_running:
                        game_state = game_paused
                        time_at_paused = current_time
                        pygame.mixer.Sound("sounds/pause.mp3").play()
                        pygame.mixer.music.pause()
                elif event.key == pygame.K_ESCAPE and game_state == game_paused:
                        game_state = game_running
                        time_at_unpaused = current_time
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_TAB and game_state == game_over:
                        gamemanager.gametime = 0
                        time_at_unpaused = current_time
                        time_at_paused = 0
                        current_game_time = 0
                        set_time_paused = False
                        dead_animation = False
                        del main_game
                        main_game = Main(width,height)
                        game_state = game_running
                        pygame.mixer.music.set_volume(0.4)
                        pygame.mixer.music.play(-1)
                        
                if event.key == pygame.K_b and game_state == game_running:
                    if main_game.player.auto_unlocked:
                        main_game.player.auto_attack = not main_game.player.auto_attack
                        
        if game_state == game_running:
            main_game.update()
            screen.blit(background, (0 + main_game.offset[0], 0 + main_game.offset[1]))
            # screen.fill((0,0,0))
            main_game.draw(screen)
            
            # screen.fill((0,0,0))
           


        if game_state == game_paused:
            current_game_time = main_game.gametime
            screen.blit(background, (0,0))
            main_game.draw(screen)
            text = font.render("Game Paused! Press [ESC] to resume", True, (255,255,255))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            screen.blit(text, text_rect)
        
        if game_state == game_over: 
            pygame.mixer.music.stop() 
            if not set_time_paused:
                main_game.time_over = main_game.gametime
                time_at_paused = current_time
                set_time_paused = True
            main_game.explosions.update(gamemanager.gametime)
            
            screen.blit(background, (0,0))
            main_game.draw(screen)
            if current_time - time_at_paused >= 1100:
                main_game.dead = True
                main_game.player.kill()
                if not dead_animation:
                    main_game.create_explosion(main_game.player.rect.centerx, main_game.player.rect.centery, small_explosion_frames, explosion_sound)
                    dead_animation = True
            if current_time - time_at_paused >= 2000:  
                text_over = font.render("Game Over! Press [TAB] to restart", True, (255,255,255))
                text_rect = text_over.get_rect(center=(width // 2, height // 2))
                screen.blit(text_over, text_rect)
                time_over = font.render(f"Time survived: {round(main_game.time_over / 1000)}s", True, (255,255,255))
                time_rect = time_over.get_rect(center=(width // 2, height // 2 + 50))
                screen.blit(time_over, time_rect)

        text_hp = font.render("HP: " + str(round(main_game.player.hp)), True, (255, 255, 255))
        text_hp_rect = text_hp.get_rect()
        text_hp_rect.topleft = (10, 10)
        screen.blit(text_hp, text_hp_rect)

        fps = font.render(f"FPS: {int(clock.get_fps())}", True, (255,255,255))
        fps_rect = fps.get_rect()
        fps_rect.topright = (width - 30, 10)
        screen.blit(fps, fps_rect)

        # difficulty = font.render(f"Difficulty: {main_game.difficulty}", True, (255, 255, 255))
        # diff_rect = difficulty.get_rect()
        # diff_rect.topleft = (200, 10)
        # screen.blit(difficulty, diff_rect)

        level = font.render(f"Level: {main_game.wave}", True, (255, 255, 255))
        level_rect = level.get_rect()
        level_rect.topleft = (550, 10)
        screen.blit(level, level_rect)
        
        # print(f"gametime: {gamemanager.gametime}, current time:{current_time}, paused:{time_at_paused}, unpaused:{time_at_unpaused}")
        # print(f"atk: {main_game.player.atk}, matk:{main_game.player.matk}")
        pygame.display.flip()
            
            










