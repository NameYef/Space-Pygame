import pygame
import math
from Explosion import Explosion


class Laser(pygame.sprite.Sprite):
    def __init__(self, image, x, y, player, mag, way = "middle"):
        super().__init__()

       
        # Resize the image
        self.image = image # image must be horizontal
        




        # Set the position of the sprite
        self.rect = self.image.get_rect(center=(x,y))
        self.magnitude = mag
        self.way = way
        self.dir = player.dir
        self.speed_x = float(0)
        self.speed_y = float(0)
        self.speed = player.lspeed 
        self.atk = player.atk
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.angle = 0
        if self.dir == "":
            self.kill()
   
        if self.dir == "up":
            self.speed_y = -self.speed 
            self.angle = 90
        if self.dir == "down":
            self.speed_y = self.speed
            self.angle = 90
        if self.dir == "left":
            self.speed_x = -self.speed
            self.angle = 0
        if self.dir == "right":
            self.speed_x = self.speed
            self.angle = 0
        if self.dir == "left up":
            self.speed_y = -self.speed * math.sin(math.pi/4)
            self.speed_x = -self.speed * math.sin(math.pi/4)
            self.angle = 135
        if self.dir == "right up":
            self.speed_y = -self.speed * math.sin(math.pi/4)
            self.speed_x = self.speed * math.sin(math.pi/4)
            self.angle = 45
        if self.dir == "left down":
            self.speed_y = self.speed * math.sin(math.pi/4)
            self.speed_x = -self.speed * math.sin(math.pi/4)
            self.angle = 45
        if self.dir == "right down":
            self.speed_y = self.speed * math.sin(math.pi/4)
            self.speed_x = self.speed * math.sin(math.pi/4)
            self.angle = 135
    def update(self, width, height, dt, target_fps):
        # Add your update logic here
        if self.way == "middle":
            self.x += self.speed_x * dt * target_fps
            self.y += self.speed_y * dt * target_fps
        if self.way == "left":
            if self.dir == "left" or self.dir == "right":
                self.x += self.speed_x * math.cos(math.radians(self.magnitude)) * dt * target_fps
                self.y += -self.speed * math.sin(math.radians(self.magnitude)) * dt * target_fps
            elif self.dir == "up" or self.dir == "down":
                self.x += self.speed * math.sin(math.radians(self.magnitude)) * dt * target_fps
                self.y += self.speed_y * math.cos(math.radians(self.magnitude)) * dt * target_fps
            else:
                self.x += self.speed_x / math.sin(math.radians(45)) * abs(math.cos(math.radians(self.magnitude + 45))) * dt * target_fps 
                self.y += self.speed_y / math.sin(math.radians(45)) * abs(math.sin(math.radians(self.magnitude + 45))) * dt * target_fps
                # print(self.speed_x / math.sin(math.radians(45)), " ", self.speed_y / math.sin(math.radians(45)))

        if self.way == "right":
            if self.dir == "left" or self.dir == "right":
                self.x += self.speed_x * math.cos(math.radians(self.magnitude)) * dt * target_fps
                self.y += self.speed * math.sin(math.radians(self.magnitude)) * dt * target_fps
            elif self.dir == "up" or self.dir == "down":
                self.x += -self.speed * math.sin(math.radians(self.magnitude)) * dt * target_fps
                self.y += self.speed_y * math.cos(math.radians(self.magnitude)) * dt * target_fps
            else:
                self.x += self.speed_x / math.sin(math.radians(45)) * abs(math.sin(math.radians(self.magnitude + 45))) * dt * target_fps
                self.y += self.speed_y / math.sin(math.radians(45)) * abs(math.cos(math.radians(self.magnitude + 45)))  * dt * target_fps
        
        if self.rect.bottom < 0 or self.rect.top > height or self.rect.right < 0 or self.rect.left > width:
            self.kill()
        
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)


    def draw(self, screen, offset):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.x += offset[0]
        self.y += offset[1]
        # Get the rotated rectangle of the enemy image
        rotated_rect = rotated_image.get_rect(center=(int(self.x),int(self.y)))
        
        self.x -= offset[0]
        self.y -= offset[1]
        # Draw the rotated enemy on the given surface
        
        screen.blit(rotated_image, rotated_rect)

class Missile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, player):
        super().__init__()

        # sprites_per_row = 10
        # sprites_per_column = 8

        # # Resize the image
        
        # self.explosion_image = pygame.image.load("textures/missile_explosion1.png").convert_alpha()
        # sprite_width = self.explosion_image.get_width() // sprites_per_row
        # sprite_height = self.explosion_image.get_height() // sprites_per_column
        # self.frames = []
        # for row in range(sprites_per_column):
        #     for col in range(sprites_per_row):
        #         a = col * sprite_width
        #         b = row * sprite_height
        #         sprite_rect = pygame.Rect(a, b, sprite_width, sprite_height)
        #         sprite = pygame.transform.scale(self.explosion_image.subsurface(sprite_rect), (500,500))
        #         self.frames.append(sprite)

        self.explosion_sound = player.explosion_sound
        self.frames = player.missile_frames

        self.image = image # image must be horizontal
        
        # Set the position of the sprite
        self.rect = self.image.get_rect(center=(x,y))
        # print(self.rect.x, " ", self.rect.y)
        self.dir = player.dir
        self.initialx = player.rect.centerx
        self.initialy = player.rect.centery
        self.speed_x = float(0)
        self.speed_y = float(0)
        self.speed = player.mspeed
        self.atk = player.matk
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.angle = 0
        if self.dir == "":
            self.kill()
   
        if self.dir == "up":
            self.speed_y = -self.speed
            self.angle = 90
        if self.dir == "down":
            self.speed_y = self.speed
            self.angle = 270
        if self.dir == "left":
            self.speed_x = -self.speed
            self.angle = 180
        if self.dir == "right":
            self.speed_x = self.speed
            self.angle = 0
        if self.dir == "left up":
            self.speed_y = -self.speed * math.sin(math.pi/4)
            self.speed_x = -self.speed * math.sin(math.pi/4)
            self.angle = 135
        if self.dir == "right up":
            self.speed_y = -self.speed * math.sin(math.pi/4)
            self.speed_x = self.speed * math.sin(math.pi/4)
            self.angle = 45
        if self.dir == "left down":
            self.speed_y = self.speed * math.sin(math.pi/4)
            self.speed_x = -self.speed * math.sin(math.pi/4)
            self.angle = 225
        if self.dir == "right down":
            self.speed_y = self.speed * math.sin(math.pi/4)
            self.speed_x = self.speed * math.sin(math.pi/4)
            self.angle = 315

    def update(self, width, height, missile_explosion, dt, target_fps):
        # Add your update logic here
        self.x += self.speed_x * dt * target_fps
        self.y += self.speed_y * dt * target_fps
    
        if self.rect.bottom < 0 or self.rect.top > height or self.rect.right < 0 or self.rect.left > width:
            self.explode(missile_explosion)
        
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        if ((self.x - self.initialx) ** 2 + (self.y - self.initialy) ** 2) ** 0.5 >= 500:
            self.explode(missile_explosion)


    def draw(self, screen, offset):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.x += offset[0]
        self.y += offset[1]
        # Get the rotated rectangle of the enemy image
        rotated_rect = rotated_image.get_rect(center=(int(self.x),int(self.y)))

        # Draw the rotated enemy on the given surface
        self.x -= offset[0]
        self.y -= offset[1]
        screen.blit(rotated_image, rotated_rect)

    def explode(self, missile_explosion):
        missile_explosion.add(Explosion(self.rect.centerx, self.rect.centery, self.frames, self.explosion_sound, 16.67))
        self.kill()