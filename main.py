import math
import pygame
import random
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1500, 800))
#background sound
mixer.music.load("backgroundsong.mp3")
mixer.music.play(-1)
# background
BG = pygame.image.load("space.jpg")

# title
pygame.display.set_caption("space war")
icon = pygame.image.load("UFO.png")
pygame.display.set_icon(icon)
# player
player = pygame.image.load("spaceship.png")
playerx = 700
playery = 700
plX = 0
# enemy
enemy = []
enemyx = []
enemyy = []
enX = []
enY = []
num_enemies = 15
for i in range(num_enemies):
    enemy.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(0, 1500))
    enemyy.append(random.randint(0, 200))
    enX.append(0.8)
    enY.append(40)
# bullet
bullet = pygame.image.load("bullet.png")
bulletx = 0
bullety = 700
buX = 0
buY = 10
bullet_state = "ready"

score_value=0
font= pygame.font.Font("freesansbold.ttf",25)
textX=10
textY=9

over=pygame.font.Font("freesansbold.ttf", 70)
def GAME_OVER():
    txt = over.render("GAME OVER", True, (0, 255, 255))
    screen.blit(txt, (500,350))


def show_score(X,Y):
    score=font.render("score:" + str(score_value),True,(255,255,0))
    screen.blit(score, (X, Y))


def player_playing(X, Y):
    screen.blit(player, (X, Y))


def enemy_playing(X, Y,i):
    screen.blit(enemy[i],(X, Y))


def bullet_fire(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (X + 16, Y + 10))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False

VIDEORESIZE =1
run = True
while run:

    screen.fill((0, 0, 0))
    screen.blit(BG, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == VIDEORESIZE:
            screen =pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                plX = -5
            if event.key == pygame.K_RIGHT:
                plX = +5
            if event.key == pygame.K_SPACE:
                if bullet_state in "ready":
                    bullet_sound = mixer.Sound("bulletsound.mp3")
                    bullet_sound.play()
                    bulletx = playerx
                    bullet_fire(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                plX = 0

    # boundries of the space ship and enimy
    playerx += plX
    if playerx <= 0:
        playerx = 0
    elif playerx >= 1436:
        playerx = 1436

    for i in range(num_enemies):
        if enemyy[i] > 400:
            for j in range(num_enemies):
                enemyy[i] = 1000
            GAME_OVER()
            break
        enemyx[i] += enX[i]
        if enemyx[i] <= 0:
            enX[i] = 0.8
            enemyy[i] += enY[i]
        elif enemyx[i] >= 1436:
            enX[i] = -0.8
            enemyy[i] += enY[i]
        collusion = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collusion:
            exp = mixer.Sound("spaceship.wav")
            exp.play()
            bullety = 700
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 1500)
            enemyy[i] = random.randint(0, 200)
        enemy_playing(enemyx[i], enemyy[i], i)

    if bullety <= 0:
        bullety = 700
        bullet_state = "ready"

    if bullet_state in "fire":
        bullet_fire(bulletx, bullety)
        bullety -= buY

    player_playing(playerx, playery)
    show_score(textX,textY)
    pygame.display.update()
