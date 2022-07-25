# Import the pygame module
import pygame
from pygame import mixer
from globals import *
from enemy import (
    round_generator
)
from player import Player
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    KEYUP,
    K_SPACE,
    K_m,
    K_n,
    K_p,
    QUIT,
    K_RETURN,
    K_ESCAPE
)

# Initialize pygame
pygame.init()
pygame.display.set_caption('Space Shooter')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("./utils/player.png").convert_alpha()
pygame.display.set_icon(icon)
background = pygame.image.load("./utils/background.jpg")

mixer.music.load("./utils/sound/background_music.wav")
mixer.music.play(-1)

font = pygame.font.Font('freesansbold.ttf', 34)
text_surface = font.render('Game is paused', False, (255, 255, 255))
text_surface2 = font.render('Click P to continue', False, (255, 255, 255))

meni_surface = font.render('Space Shooter', False, (255, 255, 255))
start_game = font.render('Press Enter to start', False, (255, 255, 255))

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Variable to keep the main loop running
running = True

clock = pygame.time.Clock()

level = 1
round_generator(all_sprites, enemies, level)
player = Player()
all_sprites.add(player)
player_keys = {"K_LEFT": False, "K_RIGHT": False, "K_SPACE": False}


def meni():
    in_meni = True
    while in_meni:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    in_meni = False

        screen.blit(meni_surface, (210, 400))
        screen.blit(start_game, (185, 480))
        pygame.display.flip()


game_end_surface = font.render('Press ESC to close window', False, (255, 255, 255))


def dieScreen():
    in_end = True
    while in_end:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_end = False
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    in_end = False
                    pygame.quit()
                    quit()
        screen.blit(game_end_surface, (120, 400))
        pygame.display.flip()


def pause():
    paused = True
    while paused:
        screen.blit(background, (0, 0))
        pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                    paused = False

        screen.blit(text_surface, (210, 400))
        screen.blit(text_surface2, (200, 450))
        pygame.display.flip()


# Main loop
meni()
while running:
    level_surface = font.render(f"Level: {level}", False, (255, 255, 255))

    # for loop through the event queue
    for event in pygame.event.get():
        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:  # check for keydown
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_LEFT:
                player_keys["K_LEFT"] = True
            if event.key == K_RIGHT:
                player_keys["K_RIGHT"] = True
            if event.key == K_SPACE:
                player_keys["K_SPACE"] = True
            if event.key == K_m:
                mixer.music.pause()
            if event.key == K_n:
                mixer.music.unpause()
            if event.key == K_p:
                pause()

        if event.type == KEYUP:  # check for keyup
            if event.key == K_LEFT:
                player_keys["K_LEFT"] = False
            if event.key == K_RIGHT:
                player_keys["K_RIGHT"] = False
            if event.key == K_SPACE:
                player_keys["K_SPACE"] = False

    # Fill the screen with black
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Updating every Entity
    enemies.update()
    player.update(player_keys)

    # Draw every Enemy Bullet
    for enemy in enemies:
        for bullet in enemy.bullets:
            screen.blit(bullet.surf, bullet.rect)

    # Draw every player Bullet
    for bullet in player.bullets:
        screen.blit(bullet.surf, bullet.rect)

    # Draw every Entity
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check Collision
    # Check every Player Bullet with every Enemy
    for player_bullet in player.bullets:
        for enemy in enemies:
            if pygame.sprite.collide_rect(player_bullet, enemy):
                enemy.lives -= 1
                if enemy.lives == 0:
                    enemy.kill()
                player_bullet.kill()

                if len(enemies) == 0:
                    level += 1
                    round_generator(all_sprites, enemies, level)

    # Check if player collide with enemy bullet
    for enemy in enemies:
        for enemy_bullet in enemy.bullets:
            if pygame.sprite.collide_rect(player, enemy_bullet):
                enemy_bullet.kill()
                player.lives -= 1
                if player.lives == 0:
                    dieScreen()

    # Update the display
    screen.blit(level_surface, (5, 5))
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
