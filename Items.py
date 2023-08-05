import pygame
import random
from Player import Player
class Item(pygame.sprite.Sprite):
    def __init__(self, width, height, gametime, texture):
        super().__init__()
        self.width = random.randint(100, width - 100)
        self.height = random.randint(100, height - 100)
        self.spawn_time = gametime
        item_spritesheet = pygame.image.load(texture).convert_alpha()
        
        self.item_frames = []
        for i in range(0, item_spritesheet.get_width(), 32):
            self.item_frames.append(pygame.transform.scale(item_spritesheet.subsurface((i,0,32,32)), (29, 29)))
        
        self.image = self.item_frames[0]
        self.rect = self.image.get_rect(center=(self.width, self.height))
        self.frame_index = 0
        self.frametime = 100  # Adjust the frame rate (frames per second) to control the animation speed
        self.last_update = 0
    
    def update(self, gametime):
    
        if gametime - self.last_update > self.frametime:
            if self.frame_index == len(self.item_frames) - 1:
                self.frame_index = 0
            else:
                self.frame_index += 1 
            self.last_update = gametime

        else:
            self.image = self.item_frames[self.frame_index]
        
        if gametime - self.spawn_time > 8000:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Heart(Item):
    def __init__(self, width, height, gametime):
        super().__init__(width, height, gametime, "textures/heartitem2.png")

    def func(self, player : Player):
        if player.hp < player.maxhp:
            player.hp += 10 if player.maxhp - player.hp >= 10 else player.maxhp - player.hp

class Speed(Item):
    def __init__(self, width, height, gametime):
        super().__init__(width, height, gametime, "textures/speeditem.png")

    def func(self, player : Player):
        if player.speed < player.maxspeed and player.speed_sub < player.maxspeed:
            if player.maxspeed - player.speed >= 0.1:
                player.speed += 0.1
                player.speed_sub += 0.1
            else:
                player.speed += player.maxspeed - player.speed
                player.speed_sub += player.maxspeed - player.speed_sub
    
class Lspeed(Item):
    def __init__(self, width, height, gametime):
        super().__init__(width, height, gametime, "textures/lspeeditem.png")

    def func(self, player : Player):
        if player.lspeed < player.maxlspeed:
            player.lspeed += 0.5 if player.maxlspeed - player.lspeed >= 0.5 else player.maxlspeed - player.lspeed
        if player.mspeed < player.maxmspeed:
            player.mspeed += 0.3 if player.maxmspeed - player.mspeed >= 0.3 else player.maxmspeed - player.mspeed

class Attack(Item):
    def __init__(self, width, height, gametime):
        super().__init__(width, height, gametime, "textures/attackitem.png")
        
    def func(self, player : Player):
        if player.atk < player.maxatk:
            player.atk += 1 if player.maxatk - player.atk >= 1 else player.maxatk - player.atk
        


class Auto(Item):
    def __init__(self, width, height, gametime):
        super().__init__(width, height, gametime, "textures/autoitem.png")
    def func(self, player : Player):
        if not player.auto_unlocked:
            player.auto_attack = True
        else:
            if player.shoot_speed > player.max_shoot_speed:
                player.shoot_speed -= 10 if player.shoot_speed - player.max_shoot_speed > 10 else player.shoot_speed - player.max_shoot_speed
        player.auto_unlocked = True

class WeaponUp(Item):
    def __init__(self, width, height, gametime):
        super().__init__(width, height, gametime, "textures/weaponupitem.png")
    
    def func(self, player : Player):
            player.weapon += 1


class MissilesItem(Item):
    def __init__(self, width, height, gametime):
        super().__init__(width, height, gametime, "textures/missileitem.png")

    def func(self, player : Player):
        player.missiles_no += 1