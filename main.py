import random
from sys import exit

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, FLOOR_HEIGHT))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.05)

    def player_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == FLOOR_HEIGHT:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self) -> None:
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > FLOOR_HEIGHT:
            self.rect.bottom = FLOOR_HEIGHT

    def animate(self):
        if self.rect.bottom < FLOOR_HEIGHT:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self) -> None:
        self.player_input()
        self.apply_gravity()
        self.animate()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            self.y_pos = FLY_HEIGHT
        elif type == 'snail':
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            self.y_pos = FLOOR_HEIGHT

        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), self.y_pos))

    def animate(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animate()
        self.rect.x -= 5
        self.destroy()


def display_score() -> int:
    ticks = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = test_font.render(f'Score: {ticks}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)
    return ticks


def collisions() -> bool:
    colliding_sprites = pygame.sprite.spritecollide(player.sprite, obstacle_group, False)
    if colliding_sprites:
        obstacle_group.empty()
    return bool(colliding_sprites)


# Constants
WIDTH, HEIGHT = 800, 400
FLOOR_HEIGHT = 300
FLY_HEIGHT = 210
OBSTACLE_TYPES = ['snail', 'fly']

# Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.05)
background_music.play(loops=-1)

# Sprite groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Load background images
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 200)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(OBSTACLE_TYPES)))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = pygame.time.get_ticks()
                game_active = True

    if game_active:
        # Draw background and score
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, FLOOR_HEIGHT))
        score = display_score()

        # Draw/update sprites
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Check for collisions
        game_active = not collisions()
    else:
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
