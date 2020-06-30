import pygame
import math 
import random
from pygame import mixer


pygame.init()
height = 600
width = 800
screen = pygame.display.set_mode((width, height))
color_light = (170, 170, 170)
color_dark = (100, 100, 100)


# Function for displaying text
def draw_text(text, size, color, surface, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
    textObj = font.render(text, True, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)


# Function for making buttons
def button(x1, x2, y1, y2, btn_width, btn_height):
    # stores the (x,y) coordinates into the variable as a tuple
    mouse = pygame.mouse.get_pos()
    # if mouse is hovered on a button it changes to lighter shade
    if x1 <= mouse[0] <= x2 and y1 <= mouse[1] <= y2:
        pygame.draw.rect(screen, color_light, [x1, y1, btn_width, btn_height])
    else:
        pygame.draw.rect(screen, color_dark, [x1, y1, btn_width, btn_height])
    

# Game menu loop
def main_menu():
    # Home background music
    mixer.music.load('audio/homeMusic.wav')
    mixer.music.play(-1)
    while True:
        background = pygame.image.load('images/background.png')
        screen.blit(background, (0, 0))
        draw_text('SPACE INVADERS', 64, (0, 107, 29), screen, 120, 100)

        button(round(width/2-100), round(width/2+100), round(height/2-25), round(height/2+25), 200, 50)
        button(round(width/2-100), round(width/2+100), round(height/2+50), round(height/2), 200, 50)
        draw_text('START GAME', 24, (255, 255, 255), screen, round(width/2-80), round(height/2-12))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if width/2-100 <= mouse[0] <= width/2+100 and height/2-25 <= mouse[1] <= height/2+25:
                    game()
        pygame.display.update()


def game():
    running = True
    # Background sound
    mixer.music.load('audio/background.wav')
    mixer.music.play(-1)
    # Player
    playerSpeed = 8
    playerImg = pygame.image.load('images/player1.png')
    playerX = round(width/2-32)
    playerY = round(height-120)
    playerX_change = 0
    def player(x, y):
        screen.blit(playerImg, (x, y))
    
    # Bullet
    bulletImg = pygame.image.load('images/bullet.png')
    bulletX = 0
    bulletY = round(width-120)
    bulletX_change = 0
    bulletY_change = 20
    bullet_state = "ready"
    def fire_bullet(x, y):
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))
    
    # Score
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    textX = 10
    textY = 10
    # Rendering score at screen
    def show_score(x, y):
        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))
    
    # Enemy
    mark = 0
    enemy_speed = 3
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6
    # Creating enemies
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('images/mob.png'))
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(enemy_speed)
        enemyY_change.append(30)
    # Rendering enemies
    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))
    # Collisions between enemy and bullet
    def is_collision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    
    while running: 
        background = pygame.image.load('images/background.png')
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    game_over()
                
                if event.key == pygame.K_RIGHT:
                    playerX_change = playerSpeed
                if event.key == pygame.K_LEFT:
                    playerX_change = -playerSpeed
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound('audio/laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        bulletY = playerY
                        fire_bullet(bulletX, bulletY)
                        bullet_state = "fire"
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
        
        for i in range(num_of_enemies):
            # Game over
            if enemyY[i] > 440:
                running = False
                game_over()
            
            if score_value == mark+10:
                mark += 10
                enemy_speed += 1    
                enemyX_change[i] += 1

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = enemy_speed
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -enemy_speed
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('audio/explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                print(score_value)
                enemyImg[random.randint(0, 5)] = pygame.image.load('images/spaceinvader2.png')
                enemyImg[random.randint(0, 5)] = pygame.image.load('images/mob.png')
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
             
            enemy(enemyX[i], enemyY[i], i)
        
        if playerX <= 0:
            playerX = 0
        elif playerX >= round(width-64):
            playerX = round(width-64)
        
        # Bullet movement
        if bulletY <= 0:
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change 
        
        show_score(textX, textY)
        playerX += playerX_change
        player(playerX, playerY)
        pygame.display.update()


def game_over():
    running = True
    while running:
        background = pygame.image.load('images/background.png')
        screen.blit(background, (0, 0))
        draw_text('GAME OVER', 64, (255, 255, 255), screen, 200, 100)

        button(round(width/2-100), round(width/2+100), round(height/2-25), round(height/2+25), 200, 50)
        draw_text('PLAY AGAIN', 24, (255, 255, 255), screen, round(width/2-74), round(height/2-12))
        button(round(width/2-100), round(width/2+100), round(height/2+50), round(height/2), 200, 50)
        draw_text('GAME MENU', 24, (255, 255, 255), screen, round(width/2-75), round(height/2+63))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if width/2-100 <= mouse[0] <= width/2+100 and height/2-25 <= mouse[1] <= height/2+25:
                    game()
                elif width/2-100 <= mouse[0] <= width/2+100 and height/2+50 <= mouse[1] <= height/2:
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()
main_menu()