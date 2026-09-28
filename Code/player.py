import pygame

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state, self.frame_index = 'down', 0
        self.image = pygame.image.load(join('..','Image', 'Player', 'down', 'frame_0_1.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-10, -30)

        #movement section
        self.direction = pygame.Vector2()
        self.speed = 300
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('..','Image', 'Player', state)):
                if file_names:
                    for file_name in sorted(file_names, key = lambda name: name.split('.')[0]):
                        full_path = join(folder_path, file_name)
                        surface = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surface)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
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

    def animate(self, delta_time):
        #get state
        if self.direction.y != 0:
            self.state = 'up' if self.direction.y < 0 else 'down'

        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        #actual animation
        self.frame_index = self.frame_index + 5 * delta_time if self.direction else 1
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        #

    def update(self, delta_time):
        self.input()
        self.move(delta_time)
        self.animate(delta_time)