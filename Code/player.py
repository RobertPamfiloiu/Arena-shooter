import pygame

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('..','Image', 'Player', 'down', 'frame_0_1.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-10, 0)

        #movement section
        self.direction = pygame.Vector2()
        self.speed = 300
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, delta_time):
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.rect.center = self.hitbox_rect.center
                    elif self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                        self.rect.center = self.hitbox_rect.center

    def update(self, delta_time):
        self.input()
        self.move(delta_time)