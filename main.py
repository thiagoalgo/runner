from random import randint

import pygame
import sys


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_font = pygame.font.Font('font/Pixeltype.ttf', 40)
    score_surf = score_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(midtop=(screen.get_width() / 2, 20))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for rect in obstacle_list:
            rect.x -= 5
            screen.blit(snail_surf, rect)
        return obstacle_list
    else:
        return []


def obstacle_collision(obstacle_list):
    for rect in obstacle_list:
        if rect.colliderect(player_rect):
            return True
    return False


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Obstacle
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
obstacle_rect_list = []

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(bottomleft = (60, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 15, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                obstacle_rect_list = 0
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))

    if game_active:
        # Blit background
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        # Blit score
        score = display_score()

        # Move
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Player update
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # Check collisions
        game_active = not obstacle_collision(obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))

        game_over_font = pygame.font.Font('font/Pixeltype.ttf', 80)
        game_over_surf = game_over_font.render('Runner', False, (111, 196, 169))
        game_over_rect = game_over_surf.get_rect(center=(screen.get_width() / 2, 50))
        screen.blit(game_over_surf, game_over_rect)

        if score > 0:
            game_over_font = pygame.font.Font('font/Pixeltype.ttf', 40)
            game_over_surf = game_over_font.render(f'Your Score: {score}', False, (111, 196, 169))
            game_over_rect = game_over_surf.get_rect(center=(screen.get_width() / 2, 330))
            screen.blit(game_over_surf, game_over_rect)

        game_over_font = pygame.font.Font('font/Pixeltype.ttf', 24)
        game_over_surf = game_over_font.render('Press [ESC] to run', False, (255, 255, 255))
        game_over_rect = game_over_surf.get_rect(center=(screen.get_width() / 2, 365))
        screen.blit(game_over_surf, game_over_rect)

        screen.blit(player_stand, player_stand_rect)

    pygame.display.update()
    clock.tick(60)
