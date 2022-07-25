import pygame
from pygame import mixer
from globals import *
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_SPACE
)


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(PlayerBullet, self).__init__()
        self.surf = pygame.image.load("./utils/bullet.png").convert_alpha()
        # self.surf = pygame.Surface((16, 16))
        # self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=(x, y)
        )
        self.bulletSpeed = 6

    def update(self):
        self.rect.move_ip(0, -self.bulletSpeed)
        if self.rect.bottom < 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("utils/player.png")
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/2, 850)
        )
        self.lives = 3
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.bulletTime = 0
        self.bulletDelay = 0.3
        self.bullet_sound = mixer.Sound("utils/sound/fire.mp3")

    def update(self, keys):
        if keys["K_LEFT"]:
            self.rect.move_ip(-self.speed, 0)
        if keys["K_RIGHT"]:
            self.rect.move_ip(self.speed, 0)
        if keys["K_SPACE"]:
            if self.bulletTime >= self.bulletDelay * FPS:
                self.bullet_sound.play()
                self.bulletTime = 0
                self.bullets.add(PlayerBullet(self.rect.centerx, self.rect.top))

        if self.rect.left < 35:  # left side of the window
            self.rect.left = 35
        elif self.rect.right > SCREEN_WIDTH - 35:  # right side of the window
            self.rect.right = SCREEN_WIDTH - 35

        for bullet in self.bullets:
            bullet.update()

        self.bulletTime += 1

