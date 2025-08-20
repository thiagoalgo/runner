from random import randint

import pygame
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300


    def update(self):
        self.player_input()
        self.apply_gravity()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_font = pygame.font.Font('font/Pixeltype.ttf', 40)
    score_surf = score_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(midtop=(screen.get_width() / 2, 20))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        obstacle_list = [rect for rect in obstacle_list if rect.right >= 0]
        return obstacle_list
    else:
        return []


def collisions(player, obstacle_list):
    if obstacle_list:
        for rect in obstacle_list:
            if rect.colliderect(player):
                return True
    return False


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 100)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frame_list = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frame_list[snail_frame_index]

# Fly
fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_list = [fly_1, fly_2]
fly_index = 0
fly_surf = fly_list[fly_index]

obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

#Player instance
player = pygame.sprite.GroupSingle()
player.add(Player())

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
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frame_list[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_list[fly_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                obstacle_rect_list.clear()
                player_gravity = 0
                player_rect.midbottom = (80, 300)
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
    if game_active:
        # Blit background
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        # Blit score
        score = display_score()

        # Move Obstacles
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Player update
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # Player Instance
        player.update()
        player.draw(screen)

        # Check collisions
        game_active = not collisions(player_rect, obstacle_rect_list)

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
