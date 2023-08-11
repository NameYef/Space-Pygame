import pygame
import random
import math
from Player import Player
from Laser import Laser
from Gamemanager import width, height


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, hit_image, scale, hp, atk, speed, lspeed, shoot_speed, difficulty_factor : dict):
        super().__init__()
        self.x = 0
        self.y = 0
        self.sides = ["top", "left", "right", "down"]
        self.side = random.choice(self.sides)
        self.width = width
        self.height = height
        if self.side == "top":
            self.x = random.randint(-10,self.width + 10)
            self.y = 0
        if self.side == "left":
            self.x = 0
            self.y = random.randint(-10,self.height + 10)
        if self.side == "right":
            self.x = self.width + 40
            self.y = random.randint(-10,self.height + 10)
        if self.side == "down":
            self.x = random.randint(-10,self.width + 10)
            self.y = self.height + 40
        
        self.dir = ""
        self.normal_image = pygame.transform.scale(pygame.image.load(image).convert_alpha(),scale)
        self.hit_image = pygame.transform.scale(pygame.image.load(hit_image).convert_alpha(),scale)
        self.image = self.normal_image
        self.limage = pygame.image.load("textures/elaser.png").convert_alpha()
        # Set the position of the sprite
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.angle = 0
        self.last_shoot = 0

        
        self.speed = speed 
        self.lspeed = lspeed * difficulty_factor["lspeed"]
        self.shoot_speed = shoot_speed * difficulty_factor["shoot_speed"]
        self.hp = hp * difficulty_factor["hp"]
        self.atk = atk * difficulty_factor["atk"]
        self.max_shoot_speed = 1500
        if self.shoot_speed <= self.max_shoot_speed:
            self.shoot_speed = self.max_shoot_speed
        self.hit_by_explosion = False
        self.damaged = False
        self.hit_by_laser = 0
        self.timeswitch = False
        self.last_hit_by_explosion = 0

    def update(self, player: Player, elasers, gametime, dt, target_fps):
        if self.hp <= 0:
            self.kill()

        if gametime - self.hit_by_laser > 100 and self.damaged:
            self.damaged = False
            
        if self.damaged:
            self.image = self.hit_image
        else:
            self.image = self.normal_image

 # Find direction vector (dx, dy) between enemy and player.
        dx, dy = self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery
        dist = math.hypot(dx, dy)
        self.angle = int(math.degrees(math.atan2(dx, dy)))

        if dist != 0:
            dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        # self.x += -dx * self.speed if dx > 0 else dx * self.speed
        # self.y += -dy * self.speed if dy > 0 else dy * self.speed
        if dx == 0 and dy != 0:
            self.y += self.speed if dy < 0 else -self.speed
        if dy == 0 and dx != 0:
            self.x += self.speed if dx < 0 else -self.speed
        if dx > 0 and dy > 0:
            self.x -= dx * self.speed * dt * target_fps
            self.y -= dy * self.speed * dt * target_fps
        if dx > 0 and dy < 0:
            self.x -= dx * self.speed * dt * target_fps
            self.y -= dy * self.speed * dt * target_fps
        if dx < 0 and dy > 0:
            self.x -= dx * self.speed * dt * target_fps
            self.y -= dy * self.speed * dt * target_fps
            self.angle += 360
        if dx < 0 and dy < 0:
            self.x -= dx * self.speed * dt * target_fps
            self.y -= dy * self.speed * dt * target_fps
            self.angle += 360

        if self.angle in range(0,31) or self.angle in range(331,360):
            self.dir = "up"
        if self.angle in range(31,61):
            self.dir = "left up"
        if self.angle in range(61, 121):
            self.dir = "left"
        if self.angle in range(121,151):
            self.dir = "left down"
        if self.angle in range(151,211):
            self.dir = "down"
        if self.angle in range(211,241):
            self.dir = "right down"
        if self.angle in range(241, 301):
            self.dir = "right"
        if self.angle in range(301, 331):
            self.dir = "right up"
        # print(self.angle)
        # print(self.dir)
        self.rect.centerx = self.x
        self.rect.centery = self.y

        
        self.shoot(elasers, gametime)

        if self.hit_by_explosion and not self.timeswitch:
            self.last_hit_by_explosion = gametime
            self.timeswitch = True
        
        if gametime - self.last_hit_by_explosion >= 2000:
            self.hit_by_explosion = False

        
        
    def draw(self, surface, offset):
        # Rotate the enemy image
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.x += offset[0]
        self.y += offset[1]
        # Get the rotated rectangle of the enemy image
        rotated_rect = rotated_image.get_rect(center=(int(self.x),int(self.y)))

        # Draw the rotated enemy on the given surface
        self.x -= offset[0]
        self.y -= offset[1]
        surface.blit(rotated_image, rotated_rect)

    def shoot(self, elasers, gametime):
        # print(current_time - self.last_shoot)
        if gametime - self.last_shoot > self.shoot_speed:
            self.last_shoot = gametime
            laser = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
            elasers.add(laser)
            
        # print(self.elasers.sprites())

class Fighter(Enemy):
    def __init__(self, difficulty_factor):
        super().__init__("textures/enemy_basic.png", "textures/enemy_basic_hit.png", (36,33), 2, 1, 0.03, 0.5, 3000, difficulty_factor)

class Kamikaze(Enemy):
    def __init__(self, difficulty_factor):
        super().__init__("textures/enemy1.png", "textures/enemy1_hit.png", (36,33), 3, 10, 0.5, 0, 0, difficulty_factor)
        self.speed *= difficulty_factor["speed"]

    def shoot(self, elasers, gametime):
        pass
    
class Elite(Enemy):
    def __init__(self, difficulty_factor):
        super().__init__("textures/enemy_elite.png", "textures/enemy_elite_hit.png", (45,49), 5, 2, 0.05, 0.65, 3000, difficulty_factor)
        self.limage = pygame.image.load("textures/elaser_elite.png").convert_alpha()
    def shoot(self, elasers, gametime):
        if gametime - self.last_shoot > self.shoot_speed:
            self.last_shoot = gametime
            if self.dir == "left" or self.dir == "right":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery + 5, self, 5, "right")  # right beam for NW to E, left beam for SE to W
                laser2 = Laser(self.limage, self.rect.centerx,self.rect.centery - 5, self, 5, "left")
                elasers.add(laser1, laser2)
            if self.dir == "up" or self.dir == "down":
                laser1 = Laser(self.limage, self.rect.centerx - 5,self.rect.centery, self, 5, "right")   # right beam for NW to E, left beam for SE to W
                laser2 = Laser(self.limage, self.rect.centerx + 5,self.rect.centery, self, 5, "left")
                elasers.add(laser1, laser2)
            if self.dir == "right up" or self.dir == "right down":
                laser1 = Laser(self.limage, self.rect.centerx + 5,self.rect.centery, self, 5, "right")
                laser2 = Laser(self.limage, self.rect.centerx - 5,self.rect.centery, self, 5, "left")
                elasers.add(laser1 , laser2)
            if self.dir == "left up" or self.dir == "left down":
                laser1 = Laser(self.limage, self.rect.centerx + 5,self.rect.centery, self, 5, "left")
                laser2 = Laser(self.limage, self.rect.centerx - 5,self.rect.centery, self, 5, "right")
                elasers.add(laser1 , laser2)



class EnemyBig(Enemy):
    def __init__(self, difficulty_factor):
        super().__init__("textures/enemy_big.png","textures/enemy_big_hit.png",(105,129), 150, 3, 0.01, 0.5, 3500, difficulty_factor)
        self.limage = pygame.image.load("textures/elaser_big.png").convert_alpha()

    def shoot(self, elasers, gametime):
        # print(current_time - self.last_shoot)
        if gametime - self.last_shoot > self.shoot_speed:
            self.last_shoot = gametime
            if self.dir == "left" or self.dir == "right":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx,self.rect.centery + 20, self, 0, "middle")  # right beam for NW to E, left beam for SE to W
                laser3 = Laser(self.limage, self.rect.centerx,self.rect.centery - 20, self, 0, "middle")
                laser4 = Laser(self.limage, self.rect.centerx,self.rect.centery + 40, self, 0, "middle")  # right beam for NW to E, left beam for SE to W
                laser5 = Laser(self.limage, self.rect.centerx,self.rect.centery - 40, self, 0, "middle")
                elasers.add(laser1, laser2, laser3, laser4, laser5)
            if self.dir == "up" or self.dir == "down":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx - 20,self.rect.centery, self, 0, "middle")   # right beam for NW to E, left beam for SE to W
                laser3 = Laser(self.limage, self.rect.centerx + 20,self.rect.centery, self, 0, "middle")
                laser4 = Laser(self.limage, self.rect.centerx + 40,self.rect.centery, self, 0, "middle")
                laser5 = Laser(self.limage, self.rect.centerx - 40,self.rect.centery, self, 0, "middle")
                elasers.add(laser1, laser2, laser3, laser4, laser5)
            if self.dir == "right up" or self.dir == "right down":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx + 20,self.rect.centery, self, 0, "middle")
                laser3 = Laser(self.limage, self.rect.centerx - 20,self.rect.centery, self, 0, "middle")
                laser4 = Laser(self.limage, self.rect.centerx + 40,self.rect.centery, self, 0, "middle")
                laser5 = Laser(self.limage, self.rect.centerx - 40,self.rect.centery, self, 0, "middle")
                elasers.add(laser1, laser2, laser3, laser4, laser5)
            if self.dir == "left up" or self.dir == "left down":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx + 20,self.rect.centery, self, 0, "middle")
                laser3 = Laser(self.limage, self.rect.centerx - 20,self.rect.centery, self, 0, "middle")
                laser4 = Laser(self.limage, self.rect.centerx + 40,self.rect.centery, self, 0, "middle")
                laser5 = Laser(self.limage, self.rect.centerx - 40,self.rect.centery, self, 0, "middle")
                elasers.add(laser1, laser2, laser3, laser4, laser5)

            
        # print(self.elasers.sprites())