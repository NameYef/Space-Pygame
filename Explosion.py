import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, explosion_frames, explosion_sound, frametime):
        super().__init__()
        self.frames = explosion_frames.copy()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_index = 0
        self.frametime = frametime  # Adjust the frame rate (frames per second) to control the animation speed
        self.last_update = 0
        self.played_sound = False
        self.explosion_sound = explosion_sound
    def update(self, gametime):
        if not self.played_sound:
            self.explosion_sound.play()
            self.played_sound = True
        if gametime - self.last_update > self.frametime:
            self.frame_index += 1
            self.last_update = gametime
            
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[self.frame_index]
    def draw(self, screen):
        screen.blit(self.image, self.rect)