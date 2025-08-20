from random import randint, choice

import pygame
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        _player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        _player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [_player_walk_1, _player_walk_2]
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0


    def player_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300


    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type = 'fly'):
        super().__init__()

        if type == 'fly':
            self.frames = [pygame.image.load('graphics/Fly/Fly1.png').convert_alpha(),
                           pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()]
            y_pos = 210
        else:
            self.frames = [pygame.image.load('graphics/snail/snail1.png').convert_alpha(),
                           pygame.image.load('graphics/snail/snail2.png').convert_alpha()]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright=(randint(900, 1100), y_pos))


    def animation_state(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]


    def move(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


    def update(self):
        self.animation_state()
        self.move()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_font = pygame.font.Font('font/Pixeltype.ttf', 40)
    score_surf = score_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(midtop=(screen.get_width() / 2, 20))
    screen.blit(score_surf, score_rect)
    return current_time


# def collisions(player, obstacle_list):
#     if obstacle_list:
#         for rect in obstacle_list:
#             if rect.colliderect(player):
#                 return True
#     return False


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

#Player group
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacle group
obstacle_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                player_gravity = 0
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        # Blit background
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        # Blit score
        score = display_score()

        # Player Instance
        player.draw(screen)
        player.update()

        # Draw obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Check collisions
        #game_active = not collisions(player_rect, obstacle_rect_list)

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

        player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
        player_stand = pygame.transform.rotozoom(player_stand, 15, 2)
        player_stand_rect = player_stand.get_rect(center=(400, 200))
        screen.blit(player_stand, player_stand_rect)

    pygame.display.update()
    clock.tick(60)
