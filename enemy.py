import random
import math
import pygame
from globals import *

'''
shooting - function
Bullet - Class
Enemy - Class
'''


# shooting - function
def shooting(ship, ship_type):
    if ship_type == "enemy1":
        ship.bullets.add(EnemyBullet(ship.rect.centerx, ship.rect.bottom - 12, (0, 5), "bullet1"))
    elif ship_type == "enemy2":
        ship.bullets.add(EnemyBullet(ship.rect.centerx, ship.rect.bottom - 4, (0, 5), "bullet2"))
    elif ship_type == "boss":  # x: 136, y: 97
        ship.bullets.add(EnemyBullet(ship.rect.centerx - 120, ship.rect.centery + 40, (-3, 5), "bullet3"))
        ship.bullets.add(EnemyBullet(ship.rect.centerx + 120, ship.rect.centery + 40, (3, 5), "bullet3"))

        ship.bullets.add(EnemyBullet(ship.rect.centerx - 90, ship.rect.centery + 51, (-3, 5), "bullet3"))
        ship.bullets.add(EnemyBullet(ship.rect.centerx + 90, ship.rect.centery + 51, (3, 5), "bullet3"))


# boss_shoot - function
def boss_shoot(ship):
    pass  # TODO - Add boss shooting


# Bullet - Class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_vector, bullet_type):
        super(EnemyBullet, self).__init__()
        self.surf = pygame.image.load(f"./utils/enemy/{bullet_type}.png").convert_alpha()
        # self.surf = pygame.Surface((10, 10))
        # self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=(x, y)
        )
        self.speed_vector = speed_vector

    def update(self):
        self.rect.move_ip(self.speed_vector)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if self.rect.left < 0:
            self.speed_vector = (-self.speed_vector[0], self.speed_vector[1])
        if self.rect.right > SCREEN_WIDTH:
            self.speed_vector = (-self.speed_vector[0], self.speed_vector[1])


# Enemy - Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, ship_type, center_x, center_y, move_dots):
        super(Enemy, self).__init__()
        self.type = ship_type
        # self.surf = pygame.Surface((45, 45))
        # self.surf.fill((255, 255, 255))
        self.lives = random.randint(1, 1)
        if ship_type == "boss":
            self.lives = 50

        self.surf = pygame.image.load(f"./utils/enemy/{ship_type}.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=(center_x, center_y)
        )
        # Moving in the start
        self.moved_dots = 0
        self.move_dots = move_dots
        self.speed = 2

        self.bullets = pygame.sprite.Group()
        self.bulletTime = random.randint(-2, 2)
        self.bulletDelay = random.randint(4, 7)
        if ship_type == "boss":
            self.bulletTime = 0
            self.bulletDelay = 1

    def update(self):
        if self.moved_dots < len(self.move_dots):
            # Find distance -> find Unit vector -> Multiply unit vector with Enemy.speed
            d_x = self.move_dots[self.moved_dots][0] - self.rect.centerx  # distance by x
            d_y = self.move_dots[self.moved_dots][1] - self.rect.centery  # distance by y
            if math.sqrt(d_x ** 2 + d_y ** 2) <= self.speed:
                self.rect.move_ip(d_x, d_y)
                self.moved_dots += 1
                return

            unit_v_x = d_x / math.sqrt(d_x ** 2 + d_y ** 2)
            unit_v_y = d_y / math.sqrt(d_x ** 2 + d_y ** 2)
            self.rect.move_ip(unit_v_x * self.speed, unit_v_y * self.speed)
            return

        if self.type == "boss":
            self.rect.move_ip(self.speed, 0)
            if self.rect.left < 0:
                self.speed = 2
            if self.rect.right > SCREEN_WIDTH:
                self.speed = -2

        self.bulletTime += 1
        if self.bulletTime >= self.bulletDelay * FPS:  # its 60 FPS :D
            shooting(self, self.type)

            self.bulletTime = 0

        for bullet in self.bullets:
            bullet.update()


def round_generator(all_sprites_group, enemies_group, n):
    board_type = random.randint(0, 0)
    if n % 3 == 0:
        new_enemy = Enemy("boss", SCREEN_WIDTH / 2, -80, [(SCREEN_WIDTH / 2, 120)])
        all_sprites_group.add(new_enemy)
        enemies_group.add(new_enemy)
        return

    if board_type == 0:  # 4 layers of 7 Enemy
        for i in range(1, 4):  # layer
            for j in range(1, 8):  # Enemy by layer
                if j < 4:
                    new_enemy = Enemy("enemy2", -80 * j, 75 * i, [(j * (SCREEN_WIDTH / 8), 75 * i)])
                    all_sprites_group.add(new_enemy)
                    enemies_group.add(new_enemy)
                if j > 4:
                    new_enemy = Enemy("enemy2", SCREEN_WIDTH + 80 * (j - 4), 75 * i, [((12 - j) * (SCREEN_WIDTH / 8),
                                                                                       75 * i)])
                    all_sprites_group.add(new_enemy)
                    enemies_group.add(new_enemy)
                elif j == 4:
                    new_enemy = Enemy("enemy1", (j * (SCREEN_WIDTH / 8)), -80 * (6 - i),
                                      [(j * (SCREEN_WIDTH / 8), 75 * i)])
                    all_sprites_group.add(new_enemy)
                    enemies_group.add(new_enemy)




'''
Enemy - 45 45
Player - 60 75
'''
