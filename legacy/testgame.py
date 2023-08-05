import pygame
import sys
from Player import Player
from Enemy import Enemy
from Explosion import Explosion
from legacy.config import WIDTH, HEIGHT

class Main():
    def __init__(self):
        self.player = Player((WIDTH/ 2, HEIGHT / 2))
        self.enemies = pygame.sprite.Group()
        self.elasers = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.enemy_last_spawn = 0
        self.iframe = 300
        self.player_get_hit_time = 0
        self.difficulty = "EASY"
        self.wave = "WAVE 1"

    def update(self):
        self.player.update(WIDTH, HEIGHT)
        self.enemies.update(self.player, self.elasers)
        self.elasers.update()
        self.explosions.update()
        self.generate_enemy()
        self.check_collision()

    def generate_enemy(self):
        if self.difficulty == "EASY":
            if GAMETIME / 1000 < 20:
                if GAMETIME - self.enemy_last_spawn > 3000:
                    self.enemy_last_spawn = GAMETIME
                    enemy1 = Enemy()
                    enemy2 = Enemy()
                    self.enemies.add(enemy1,enemy2)
                    self.wave = "WAVE 1"
            elif 20 <= GAMETIME / 1000 < 40:
                if GAMETIME - self.enemy_last_spawn > 3000:
                    self.enemy_last_spawn = GAMETIME
                    enemy1 = Enemy()
                    enemy2 = Enemy()
                    enemy3 = Enemy()
                    self.enemies.add(enemy1,enemy2, enemy3)
                    self.wave = "WAVE 2"
            elif 40 <= GAMETIME / 1000 < 60:
                if GAMETIME - self.enemy_last_spawn > 2000:
                    self.enemy_last_spawn = GAMETIME
                    enemy1 = Enemy()
                    enemy2 = Enemy()
                    enemy3 = Enemy()
                    self.enemies.add(enemy1,enemy2, enemy3)
                    self.wave = "WAVE 3"
            elif 60 <= GAMETIME / 1000 < 80:
                if GAMETIME - self.enemy_last_spawn > 3000:
                    self.enemy_last_spawn = GAMETIME
                    enemy1 = Enemy()
                    enemy2 = Enemy()
                    enemy3 = Enemy()
                    enemy4 = Enemy()
                    enemy5 = Enemy()
                    self.enemies.add(enemy1,enemy2,enemy3, enemy4, enemy5)
                    self.wave = "WAVE 4"
            elif 80 <= GAMETIME / 1000 < 100:
                if GAMETIME - self.enemy_last_spawn > 4000:
                    self.enemy_last_spawn = GAMETIME
                    enemy1 = Enemy()
                    enemy2 = Enemy()
                    enemy3 = Enemy()
                    enemy4 = Enemy()
                    enemy5 = Enemy()
                    enemy6 = Enemy()
                    enemy7 = Enemy()
                    self.enemies.add(enemy1,enemy2,enemy3, enemy4, enemy5, enemy6, enemy7)
                    self.wave = "WAVE 5"
            else:
                if GAMETIME - self.enemy_last_spawn > 3000:
                    self.enemy_last_spawn = GAMETIME
                    enemy1 = Enemy()
                    enemy2 = Enemy()
                    enemy3 = Enemy()
                    enemy4 = Enemy()
                    enemy5 = Enemy()
                    enemy6 = Enemy()
                    enemy7 = Enemy()
                    self.enemies.add(enemy1,enemy2,enemy3, enemy4, enemy5, enemy6, enemy7)
                    self.wave = "ENDLESS"

    def draw(self, screen):
        self.player.draw(screen)
        for i in self.enemies:
            i.draw(screen)
        for i in self.elasers:
            i.draw(screen)
        self.explosions.draw(screen)

    def check_collision(self):
        # print(GAMETIME - self.player_get_hit_time)
        for i in self.enemies:
            if pygame.sprite.spritecollide(i, self.player.lasers, True):
                 i.hp -= self.player.atk
                 if i.hp == 0:
                    i.kill()
                    self.create_explosion(i.rect.centerx, i.rect.centery)
            if pygame.sprite.collide_rect(i, self.player) and (GAMETIME - self.player_get_hit_time >= self.iframe):
                self.player_get_hit_time = GAMETIME
                self.player.hp -= i.atk * 5
                i.hp -= self.player.atk * 1.5
                self.player.crash = True
                self.create_explosion(i.rect.centerx, i.rect.centery)
                if i.hp <= 0:
                    i.kill()
            if (GAMETIME - self.player_get_hit_time >= 1000):
                self.player.crash = False
        for i in self.elasers:
            if pygame.sprite.collide_rect(self.player, i) and (GAMETIME - self.player_get_hit_time >= self.iframe): # player get hit
                self.player.hp -= i.atk
                i.kill()
                self.player_get_hit_time = GAMETIME
        # pygame.sprite.groupcollide(self.player.lasers, self.elasers, True, True) # lasers cancel out each other


    def create_explosion(self, x, y):
        explosion = Explosion(x,y, small_explosion_frames, explosion_sound)
        self.explosions.add(explosion)
    
# Initialize Pygame
pygame.init()

# Set up the window display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Template")
clock = pygame.time.Clock()
font = pygame.font.Font("gamefont.otf", 36)


game_paused = "paused"
game_over = "game over"
game_running = "running"
game_state = game_running
main_game = Main()

# set up other sprites
# background image
background = pygame.transform.smoothscale(pygame.image.load("textures/background.png").convert(), (WIDTH,HEIGHT))

# explosion sprite
explosion_spritesheet = pygame.image.load("textures/explosion.png").convert_alpha()
explosion_sound = pygame.mixer.Sound("sounds/explosion.ogg")
small_explosion_frames = []
for i in range(0, explosion_spritesheet.get_width(), 32):
    small_explosion_frames.append(explosion_spritesheet.subsurface((i,0,32,32)))

# background music
pygame.mixer.music.load("sounds/brawl_fd.mp3")
pygame.mixer.music.play(-1)


# Game loop
if __name__ == "__main__":
    while True:
        current_time = pygame.time.get_ticks()
        if (game_state == game_running):
            GAMETIME = current_time
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

        if game_state == game_running:
            main_game.update()
            screen.blit(background, (0,0))
            main_game.draw(screen)
            
            
            text_hp = font.render("HP: " + str(main_game.player.hp), True, (255, 255, 255))
            text_hp_rect = text_hp.get_rect()
            text_hp_rect.topleft = (10, 10)
            screen.blit(text_hp, text_hp_rect)

            fps = font.render(f"FPS: {int(clock.get_fps())}", True, (255,255,255))
            fps_rect = fps.get_rect()
            fps_rect.topright = (WIDTH - 30, 10)
            screen.blit(fps, fps_rect)

            difficulty = font.render(f"Difficulty: {main_game.difficulty}", True, (255, 255, 255))
            diff_rect = difficulty.get_rect()
            diff_rect.topleft = (200, 10)
            screen.blit(difficulty, diff_rect)

            level = font.render(f"Level: {main_game.wave}", True, (255, 255, 255))
            level_rect = level.get_rect()
            level_rect.topleft = (550, 10)
            screen.blit(level, level_rect)
            
            clock.tick()
            pygame.display.flip()










