import pygame
import sys
import random
import math
# Initialize Pygame
pygame.init()

# Set the window dimensions
WIDTH = 800
HEIGHT = 600

# Set up the window display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


        # Resize the image
        self.image = pygame.transform.scale(pygame.image.load("player.png").convert_alpha(), (60, 36))


        # Set the position of the sprite
        self.rect = self.image.get_rect(center=(300,500))
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        self.lasers = pygame.sprite.Group()

        self.laser_fired = False

        self.dir = "up"

        self.angle = 0
        self.weapon = 1

        self.speed = 0.6

    def update(self,width,height):
        # Add your update logic here
        keys = pygame.key.get_pressed()
         # Adjust the speed as needed
 
        if keys[pygame.K_w]:
            self.y -= self.speed 
            self.dir = "up"
            self.angle = 0
        if keys[pygame.K_s]:
            self.y += self.speed
            self.dir = "down" 
            self.angle = 180
        if keys[pygame.K_a]:
            self.x -= self.speed 
            self.dir = "left"
            self.angle = 90
        if keys[pygame.K_d]:
            self.x += self.speed 
            self.dir = "right"
            self.angle = 270
        if keys[pygame.K_w] and keys[pygame.K_a]:
            # self.x -= self.speed 
            # self.y -= self.speed 
            self.dir = "left up"
            self.angle = 45
        if keys[pygame.K_w] and keys[pygame.K_d]:
            # self.x += self.speed 
            # self.y -= self.speed 
            self.dir = "right up"
            self.angle = 315
        if keys[pygame.K_s] and keys[pygame.K_a]:
            # self.x -= self.speed 
            # self.y += self.speed 
            self.dir = "left down"
            self.angle = 135
        if keys[pygame.K_s] and keys[pygame.K_d]:
            # self.x += self.speed 
            # self.y += self.speed 
            self.dir = "right down"
            self.angle = 225

        self.rect.centerx = self.x
        self.rect.centery = self.y

        if keys[pygame.K_SPACE] and not self.laser_fired:
            self.shoot()
            self.laser_fired = True
        elif not keys[pygame.K_SPACE]:
            self.laser_fired = False

        if self.rect.x < 0:
            self.rect.x = 0
            self.x = self.rect.centerx
        if self.rect.right > width:
            self.rect.right = width
            self.x = self.rect.centerx
        if self.rect.y < 0:
            self.rect.y = 0
            self.y = self.rect.centery
        if self.rect.bottom > height:
            self.rect.bottom = height
            self.y = self.rect.centery


        if keys[pygame.K_1]:
            self.weapon = 1
        if keys[pygame.K_2]:
            self.weapon = 2

        self.lasers.update()
        

    def draw(self, surface):
        # Draw the sprite on the given surface
        rotated_image = pygame.transform.rotate(self.image, self.angle)

        # Get the rotated rectangle of the spaceship image
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        rotated_rect = rotated_image.get_rect(center = (self.rect.centerx, self.rect.centery))

        # Draw the rotated spaceship on the given surface
        surface.blit(rotated_image, rotated_rect)
        # surface.blit(self.image, self.rect)
        self.lasers.draw(surface)


    def shoot(self):
        if self.weapon == 1:
            laser1 = Laser(self.rect.centerx,self.rect.centery)
            self.lasers.add(laser1)
        if self.weapon == 2:
            if self.dir == "left" or self.dir == "right":
                laser1 = Laser(self.rect.centerx,self.rect.centery)
                laser2 = Laser(self.rect.centerx,self.rect.centery + 15)
                laser3 = Laser(self.rect.centerx,self.rect.centery - 15)
                self.lasers.add([laser1,laser2, laser3])
            else:
                laser1 = Laser(self.rect.centerx,self.rect.centery)
                laser2 = Laser(self.rect.centerx + 15,self.rect.centery)
                laser3 = Laser(self.rect.centerx - 15,self.rect.centery)
                self.lasers.add([laser1, laser2, laser3])


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.sides = ["top", "left", "right", "down"]
        self.side = random.choice(self.sides)

        if self.side == "top":
            self.x = random.randint(-10, WIDTH + 10)
            self.y = 0
        if self.side == "left":
            self.x = 0
            self.y = random.randint(-10, HEIGHT + 10)
        if self.side == "right":
            self.x = WIDTH
            self.y = random.randint(-10, HEIGHT + 10)
        if self.side == "down":
            self.x = random.randint(-10, WIDTH + 10)
            self.y = 0

        self.rect = pygame.Rect(self.x, self.y, 80, 48)
        self.angle = 0
        self.last_shoot = pygame.time.get_ticks()
        self.lasers = pygame.sprite.Group()

    def update(self, player: Player):
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = max(1, math.hypot(dx, dy))
        dx, dy = dx / dist, dy / dist
        self.rect.centerx += dx * self.speed
        self.rect.centery += dy * self.speed

        self.shoot()
        self.lasers.update()

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        surface.blit(rotated_image, self.rect)

        self.lasers.draw(surface)

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot > 2000:  # Adjust the shooting interval as needed
            self.last_shoot = current_time
            laser = Laser(self.rect.centerx, self.rect.centery)
            self.lasers.add(laser)


# Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))  # Adjust the laser dimensions as needed
        self.image.fill((255, 0, 0))  # Adjust the laser color as needed
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5  # Adjust the laser speed as needed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# Main class
class Main:
    def __init__(self):
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.last_spawn = pygame.time.get_ticks()

    def update(self):
        self.player.update(WIDTH, HEIGHT)
        self.generate_enemy()
        self.enemies.update(self.player)
        self.collision()

    def draw(self, surface):
        self.player.draw(surface)
        self.enemies.draw(surface)

    def generate_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn > 3000:  # Adjust the enemy spawn interval as needed
            self.last_spawn = current_time
            enemy = Enemy()
            self.enemies.add(enemy)

    def collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            print("Player collided with an enemy!")


# Create the main game object
game = Main()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update()

    screen.fill((0, 0, 0))
    game.draw(screen)

    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()