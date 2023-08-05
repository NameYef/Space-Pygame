import pygame
import sys
from pygame.math import Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()


        # Resize the image
        self.image = pygame.transform.scale(pygame.image.load("textures/NicePng_spaceship-png_138961.png").convert_alpha(), (60, 36))


        # Set the position of the sprite
        self.rect = self.image.get_rect(center=(pos))
        self.x_position = float(self.rect.x)
        self.y_position = float(self.rect.y)


        self.lasers = pygame.sprite.Group()

        self.laser_fired = False

        self.dir = "up"

        self.angle = 0
        self.weapon = 1
    def update(self,width,height):
        # Add your update logic here
        keys = pygame.key.get_pressed()
        speed = 1  # Adjust the speed as needed
 
        if keys[pygame.K_w]:
            self.rect.y -= speed 
            self.dir = "up"
            self.angle = 0
        if keys[pygame.K_s]:
            self.rect.y += speed
            self.dir = "down" 
            self.angle = 180
        if keys[pygame.K_a]:
            self.rect.x -= speed 
            self.dir = "left"
            self.angle = 90
        if keys[pygame.K_d]:
            self.rect.x += speed 
            self.dir = "right"
            self.angle = 270
        if keys[pygame.K_w] and keys[pygame.K_a]:
            self.dir = "left up"
            self.angle = 45
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.dir = "right up"
            self.angle = 315
        if keys[pygame.K_s] and keys[pygame.K_a]:
            self.dir = "left down"
            self.angle = 135
        if keys[pygame.K_s] and keys[pygame.K_d]:
            self.dir = "right down"
            self.angle = 225


        if keys[pygame.K_SPACE] and not self.laser_fired:
            self.shoot()
            self.laser_fired = True
        elif not keys[pygame.K_SPACE]:
            self.laser_fired = False


        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right> width:
            self.rect.right = width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > height:
            self.rect.bottom = height


        if keys[pygame.K_1]:
            self.weapon = 1
        if keys[pygame.K_2]:
            self.weapon = 2

        self.lasers.update()
        

    def draw(self, surface):
        # Draw the sprite on the given surface
        rotated_image = pygame.transform.rotate(self.image, self.angle)

        # Get the rotated rectangle of the spaceship image
        rotated_rect = rotated_image.get_rect(center=self.rect.center)

        # Draw the rotated spaceship on the given surface
        surface.blit(rotated_image, rotated_rect)
        # surface.blit(self.image, self.rect)
        self.lasers.draw(surface)
    def shoot(self):
        if self.weapon == 1:
            laser1 = Laser(self.rect.centerx,self.rect.centery, self.dir)
            self.lasers.add(laser1)
        if self.weapon == 2:
            if self.dir == "left" or self.dir == "right":
                laser1 = Laser(self.rect.centerx,self.rect.centery, self.dir)
                laser2 = Laser(self.rect.centerx,self.rect.centery + 15, self.dir)
                laser3 = Laser(self.rect.centerx,self.rect.centery - 15, self.dir)
                self.lasers.add([laser1,laser2, laser3])
            else:
                laser1 = Laser(self.rect.centerx,self.rect.centery, self.dir)
                laser2 = Laser(self.rect.centerx + 15,self.rect.centery , self.dir)
                laser3 = Laser(self.rect.centerx - 15,self.rect.centery , self.dir)
                self.lasers.add([laser1,laser2, laser3])



class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        super().__init__()


        # Resize the image
        self.image = pygame.transform.scale(pygame.image.load("textures/laser2.png").convert_alpha(), (10, 30))

        # Set the position of the sprite
        self.rect = self.image.get_rect(center=(x,y))
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 2
        if dir == "up":
            self.speed_y = -self.speed
        if dir == "down":
            self.speed_y = self.speed
        if dir == "left":
            self.speed_x = -self.speed
        if dir == "right":
            self.speed_x = self.speed
        if dir == "left up":
            self.speed_y = -self.speed
            self.speed_x = -self.speed
        if dir == "right up":
            self.speed_y = -self.speed
            self.speed_x = self.speed
        if dir == "left down":
            self.speed_y = self.speed
            self.speed_x = -self.speed
        if dir == "right down":
            self.speed_y = self.speed
            self.speed_x = self.speed
    def update(self):
        # Add your update logic here
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        

        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()





# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
# Set the window dimensions
WIDTH = 1600
HEIGHT = 1000

# Set up the window display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Template")

# Game loop
if __name__ == "__main__":
    player = Player((300, 500))
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        player.update(WIDTH,HEIGHT)
        screen.fill((0, 0, 0))
        player.draw(screen)
        print(f"{player.rect.x} {player.rect.y} {player.dir}")
        
        clock.tick()
        pygame.display.flip()
