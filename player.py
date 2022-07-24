import pygame
from pygame import mixer
import math
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
screen = pygame.display.set_mode((700, 950))
background = pygame.image.load('img/background.jpg')

mixer.music.load("sound/background_music.wav")
mixer.music.play(-1)


font = pygame.font.Font('freesansbold.ttf', 34)
textsurface = font.render('Game is paused', False, (255, 255, 255))
textsurface2 = font.render('Click P to continue', False, (255, 255, 255))




pygame.display.set_caption("Space Destroyer")
icon = pygame.image.load('img/logo.png')
pygame.display.set_icon(icon)
playerImage = pygame.image.load('img/player.png')
playerX = 230
playerY = 680
playerX_change = 0
playerY_change = 0

bulletImage = pygame.image.load('img/bullet.png')
bulletX = 200
bulletY = 680
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 27)
text_first = 10
text_second = 10
over_font = pygame.font.Font('freesansbold.ttf', 54)


def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
     
        screen.blit(textsurface,(210, 400))
        screen.blit(textsurface2,(200, 450))
        pygame.display.flip()
                    

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImage, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 40, y + 10))

running = True

while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
        
        speed_left = -1
        speed_right = 1
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = speed_left
            if event.key == pygame.K_RIGHT:
                playerX_change = speed_right
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("sound/fire.mp3")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
            if event.key == pygame.K_n:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_p:
                pause()

           

  
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 50:
        playerX = 50
    elif playerX >= 460:
        playerX = 460

    if bulletY <= 0:
        bulletY = 680
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    # show_score(text_first, text_second)
    pygame.display.update()

