import pygame
import math
from Laser import Laser, Missile

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        

        # Resize the image
        self.normal_image = pygame.transform.scale(pygame.image.load("textures/player.png").convert_alpha(), (50, 30))
        self.hit_image = pygame.transform.scale(pygame.image.load("textures/player_hit.png").convert_alpha(), (50, 30))
        self.image = self.normal_image
        self.limage = pygame.image.load("textures/plaser1.png").convert_alpha()
        self.mimage = pygame.transform.scale(pygame.image.load("textures/missile.png").convert_alpha(), (30, 10))


        # Set the position of the sprite
        self.rect = self.image.get_rect(center=pos)
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)


        self.lasers = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        self.lasersound = pygame.mixer.Sound("sounds/playerlaser2.mp3")
        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.ogg")

        # for missiles
        sprites_per_row = 10
        sprites_per_column = 8

        self.explosion_image = pygame.image.load("textures/missile_explosion1.png").convert_alpha()
        sprite_width = self.explosion_image.get_width() // sprites_per_row
        sprite_height = self.explosion_image.get_height() // sprites_per_column
        self.missile_frames = []
        for row in range(sprites_per_column):
            for col in range(sprites_per_row):
                a = col * sprite_width
                b = row * sprite_height
                sprite_rect = pygame.Rect(a, b, sprite_width, sprite_height)
                sprite = pygame.transform.scale(self.explosion_image.subsurface(sprite_rect), (250,250))
                self.missile_frames.append(sprite)

        # player properties
        self.auto_unlocked = False
        self.laser_fired = False
        self.missile_fired = False
        self.crash = False
        self.damaged = False

        self.dir = "up"


        self.angle = 0
        self.weapon = 1
        self.missiles_no = 3
        self.last_shoot = 0
        self.last_missile_shoot = 0
        self.hit_by_laser = 0
       
        self.speed_sub = 0.8
        self.speed = 0.8
        self.maxspeed = 1.75 
        self.lspeed = 1.5
        self.mspeed = 1.5 
        self.maxlspeed = 12 
        self.maxmspeed = 5 
        self.hp = 1
        self.maxhp = 1000
        self.atk = 1
        self.matk = 10
        self.maxatk = 15
        self.shoot_speed = 200
        self.max_shoot_speed = 30
        self.missile_cooldown = 1000
        self.auto_attack = False

    def update(self,width,height, gametime, dt, target_fps, missile_explosion):
        
        if self.crash:
            self.speed =  self.speed_sub * 0.25
        else:
            self.speed = self.speed_sub
        
        if gametime - self.hit_by_laser > 100 and self.damaged:
            self.damaged = False
            
        if self.damaged:
            self.image = self.hit_image
        else:
            self.image = self.normal_image


        keys = pygame.key.get_pressed()
         # Adjust the speed as needed
 
        if keys[pygame.K_w] and keys[pygame.K_a]:
            self.x -= self.speed * (math.sqrt(2)/2) * dt * target_fps
            self.y -= self.speed * (math.sqrt(2)/2) * dt * target_fps
            self.dir = "left up"
            self.angle = 45
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            self.x += self.speed * (math.sqrt(2)/2) * dt * target_fps 
            self.y -= self.speed * (math.sqrt(2)/2) * dt * target_fps 
            self.dir = "right up"
            self.angle = 315
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            self.x -= self.speed * (math.sqrt(2)/2) * dt * target_fps 
            self.y += self.speed * (math.sqrt(2)/2) * dt * target_fps 
            self.dir = "left down"
            self.angle = 135
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            self.x += self.speed * (math.sqrt(2)/2) * dt * target_fps 
            self.y += self.speed * (math.sqrt(2)/2) * dt * target_fps 
            self.dir = "right down"
            self.angle = 225
        elif keys[pygame.K_w]:
            self.y -= self.speed * dt * target_fps
            self.dir = "up"
            self.angle = 0
        elif keys[pygame.K_s]:
            self.y += self.speed * dt * target_fps 
            self.dir = "down" 
            self.angle = 180
        elif keys[pygame.K_a]:
            self.x -= self.speed * dt * target_fps 
            self.dir = "left"
            self.angle = 90
        elif keys[pygame.K_d]:
            self.x += self.speed * dt * target_fps 
            self.dir = "right"
            self.angle = 270
        
        self.rect.centerx = self.x
        self.rect.centery = self.y

        if (keys[pygame.K_SPACE]) and (not self.laser_fired) and (not self.auto_attack):
            self.shoot()
            self.lasersound.play()
            self.laser_fired = True
        elif not keys[pygame.K_SPACE] and not self.auto_attack:
            self.laser_fired = False
        
        if keys[pygame.K_LSHIFT] and self.missiles_no != 0 and (not self.missile_fired):
            self.matk = self.atk * 15
            self.missiles_no -= 1
            self.last_missile_shoot = gametime
            self.missile_fired = True
            # print(self.rect.centerx, " ", self.rect.centery)
            self.missiles.add(Missile(self.mimage, self.rect.centerx, self.rect.centery, self))
        elif not keys[pygame.K_LSHIFT]:
            if gametime - self.last_missile_shoot > self.missile_cooldown:
                self.missile_fired = False

        if self.auto_attack:
            if gametime - self.last_shoot > self.shoot_speed:
                self.last_shoot = gametime
                self.shoot()
                if self.shoot_speed >= 50:
                    self.lasersound.play() 

        # print(self.missiles_no)


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


        # if keys[pygame.K_1]:
        #     self.weapon = 1
        # if keys[pygame.K_2]:
        #     self.weapon = 2
        # if keys[pygame.K_3]:
        #     self.weapon = 3

        self.lasers.update(width, height, dt, target_fps)
        self.missiles.update(width, height, missile_explosion, dt, target_fps)
        missile_explosion.update(gametime)
        # print(self.dir)

    

    def draw(self, surface, offset):
        # Draw the sprite on the given surface
        rotated_image = pygame.transform.rotate(self.image, self.angle)

        self.x += offset[0]
        self.y += offset[1]

        # Get the rotated rectangle of the spaceship image
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        rotated_rect = rotated_image.get_rect(center = (self.rect.centerx, self.rect.centery))

        self.x -= offset[0]
        self.y -= offset[1]
        # Draw the rotated spaceship on the given surface
        surface.blit(rotated_image, rotated_rect)
        # surface.blit(self.image, self.rect)
        for i in self.lasers:
            i.draw(surface, offset)
        
        for i in self.missiles:
            i.draw(surface, offset)



    def shoot(self):
        if self.weapon == 1:
            laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
            self.lasers.add(laser1)
        elif self.weapon == 2:
            if self.dir == "left" or self.dir == "right":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery + 7, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx,self.rect.centery - 7, self, 0, "left")
                self.lasers.add(laser1, laser2)
            if self.dir == "up" or self.dir == "down":
                laser1 = Laser(self.limage, self.rect.centerx - 7,self.rect.centery, self, 0, "middle")   # right beam for NW to E, left beam for SE to W
                laser2 = Laser(self.limage, self.rect.centerx + 7,self.rect.centery, self, 0, "middle")
                self.lasers.add(laser1, laser2)
            if self.dir == "right up" or self.dir == "right down":
                laser1 = Laser(self.limage, self.rect.centerx + 7,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx - 7,self.rect.centery, self, 0, "middle")
                self.lasers.add(laser1 , laser2)
            if self.dir == "left up" or self.dir == "left down":
                laser1 = Laser(self.limage, self.rect.centerx + 7,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx - 7,self.rect.centery, self, 0, "middle")
                self.lasers.add(laser1 , laser2)
        elif self.weapon == 3:
            if self.dir == "left" or self.dir == "right":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx,self.rect.centery + 15, self, 5, "right")  # right beam for NW to E, left beam for SE to W
                laser3 = Laser(self.limage, self.rect.centerx,self.rect.centery - 15, self, 5, "left")
                self.lasers.add(laser1, laser2, laser3)
            if self.dir == "up" or self.dir == "down":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx - 15,self.rect.centery, self, 5, "right")   # right beam for NW to E, left beam for SE to W
                laser3 = Laser(self.limage, self.rect.centerx + 15,self.rect.centery, self, 5, "left")
                self.lasers.add(laser1, laser2, laser3)
            if self.dir == "right up" or self.dir == "right down":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx + 15,self.rect.centery, self, 5, "right")
                laser3 = Laser(self.limage, self.rect.centerx - 15,self.rect.centery, self, 5, "left")
                self.lasers.add(laser1 , laser2, laser3)
            if self.dir == "left up" or self.dir == "left down":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx + 15,self.rect.centery, self, 5, "left")
                laser3 = Laser(self.limage, self.rect.centerx - 15,self.rect.centery, self, 5, "right")
                self.lasers.add(laser1 , laser2, laser3)
        elif self.weapon == 4:
            if self.dir == "left" or self.dir == "right":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx,self.rect.centery + 15, self, 3, "right")  # right beam for NW to E, left beam for SE to W
                laser3 = Laser(self.limage, self.rect.centerx,self.rect.centery - 15, self, 3, "left")
                laser4 = Laser(self.limage, self.rect.centerx,self.rect.centery + 30, self, 8, "right")
                laser5 = Laser(self.limage, self.rect.centerx,self.rect.centery - 30, self, 8, "left")
                self.lasers.add(laser1, laser2, laser3, laser4, laser5)
            if self.dir == "up" or self.dir == "down":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx - 15,self.rect.centery, self, 3, "right")   # right beam for NW to E, left beam for SE to W
                laser3 = Laser(self.limage, self.rect.centerx + 15,self.rect.centery, self, 3, "left")
                laser4 = Laser(self.limage, self.rect.centerx - 30,self.rect.centery, self, 8, "right")
                laser5 = Laser(self.limage, self.rect.centerx + 30,self.rect.centery, self, 8, "left")
                self.lasers.add(laser1, laser2, laser3, laser4, laser5)
            if self.dir == "right up" or self.dir == "right down":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx + 15,self.rect.centery, self, 3, "right")
                laser3 = Laser(self.limage, self.rect.centerx - 15,self.rect.centery, self, 3, "left")
                laser4 = Laser(self.limage, self.rect.centerx + 30,self.rect.centery, self, 8, "right")
                laser5 = Laser(self.limage, self.rect.centerx - 30,self.rect.centery, self, 8, "left")
                self.lasers.add(laser1, laser2, laser3, laser4, laser5)
            if self.dir == "left up" or self.dir == "left down":
                laser1 = Laser(self.limage, self.rect.centerx,self.rect.centery, self, 0, "middle")
                laser2 = Laser(self.limage, self.rect.centerx - 15,self.rect.centery, self, 3, "right")
                laser3 = Laser(self.limage, self.rect.centerx + 15,self.rect.centery, self, 3, "left")
                laser4 = Laser(self.limage, self.rect.centerx - 30,self.rect.centery, self, 8, "right")
                laser5 = Laser(self.limage, self.rect.centerx + 30,self.rect.centery, self, 8, "left")
                self.lasers.add(laser1, laser2, laser3, laser4, laser5)
           
