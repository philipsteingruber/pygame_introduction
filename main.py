import pygame
from sys import exit
import random


def display_score() -> int:
    ticks = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = test_font.render(f'Score: {ticks}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)
    return ticks


def move_obstacles(obstacle_list: list[pygame.Rect]) -> list[pygame.Rect]:
    for obstacle_rect in obstacle_list:
        obstacle_rect.x -= 5

        if obstacle_rect.bottom == FLOOR_HEIGHT:
            screen.blit(snail_surface, obstacle_rect)
        else:
            screen.blit(fly_surface, obstacle_rect)
    obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

    return obstacle_list


def collisions(player: pygame.Rect, obstacles: list[pygame.Rect]) -> bool:
    for obstacle_rect in obstacles:
        if obstacle_rect.colliderect(player):
            return True
    return False


def player_animation():
    global player_surface, player_index

    if player_rect.bottom < FLOOR_HEIGHT:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


WIDTH, HEIGHT = 800, 400
FLOOR_HEIGHT = 300

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

OBSTACLE_TYPES = ['fly', 'snail']
obstacle_rect_list = []

# Player
player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_surface = player_walk[player_index]
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_rect = player_surface.get_rect(midbottom=(80, FLOOR_HEIGHT))
player_gravity = 0

# Intro screen
title_surface = test_font.render('Welcome to Runnergame!', False, 'White')
title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))

instruction_surface = test_font.render('Press Spacebar to begin', False, 'White')
instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(WIDTH//2, HEIGHT//2))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == FLOOR_HEIGHT:
                    player_gravity = -20
                    print('Jump!')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(pygame.mouse.get_pos()) and player_rect.bottom == FLOOR_HEIGHT:
                    player_gravity = -20
                    print('Jump!')
            if event.type == obstacle_timer:
                if random.choice(OBSTACLE_TYPES) == 'snail':
                    obstacle_rect_list.append(snail_surface.get_rect(midbottom=(random.randint(900, 1100), FLOOR_HEIGHT)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom = (random.randint(900, 1100), FLOOR_HEIGHT - 100)))
                print(len(obstacle_rect_list))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = pygame.time.get_ticks()
                game_active = True

    if game_active:
        # Draw background and score
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, FLOOR_HEIGHT))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= FLOOR_HEIGHT:
            player_rect.bottom = FLOOR_HEIGHT
        player_animation()
        screen.blit(player_surface, player_rect)

        # Obstacle movement
        obstacle_rect_list = move_obstacles(obstacle_rect_list)

        # Collision
        if collisions(player_rect, obstacle_rect_list):
            game_active = False

    else:
        # Reset stuff
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, FLOOR_HEIGHT)
        player_gravity = 0

        # Display Game Over screen
        screen.fill((94, 129, 162))
        screen.blit(title_surface, title_rect)
        screen.blit(player_stand, player_stand_rect)

        if score > 0:
            score_message = test_font.render(f'Your last score: {score}', False, 'White')
            score_rect = score_message.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(score_message, score_rect)
        else:
            screen.blit(instruction_surface, instruction_rect)

    pygame.display.update()
    clock.tick(60)
