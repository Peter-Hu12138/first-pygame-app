import pygame
import random
from objects import *
from sys import exit

def get_curr_time():
    return pygame.time.get_ticks() - start_time

def get_curr_score():
    return int(get_curr_time() / 500)

def display_text_at(screen_displaying, text, font, x, y):
    score_surface = font.render(text, 1, "cyan")
    score_rect = score_surface.get_rect(center=(x, y))
    pygame.draw.rect(screen_displaying, "pink", score_rect)
    pygame.draw.rect(screen_displaying, "pink", score_rect, width=10)
    screen_displaying.blit(score_surface, score_rect)

WIDTH = 800
HEIGHT = 400

pygame.init()
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jingtian Hu's REAL first pygame project!")
clock = pygame.time.Clock()
game_font = pygame.font.Font("./font/Pixeltype.ttf", 50)
start_time = 0

over_text_surf = game_font.render("OVER - press esc to start over", 1, "cyan")
over_text_rect = over_text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 5))

# more init
game_state = "STR"
"""
ONG - onoging
PAU - paused
STR - start
OVR - over
"""
# load and init images and rects and vars
sky_surface = pygame.image.load("./graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load("./graphics/ground.png").convert_alpha()
ground_rect = ground_surface.get_rect(topleft=(0, 300))

obstacle_manager = Manager(WIDTH)
snail = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
snail_rect = snail.get_rect(bottomleft=(800, 300))
snail_speed = 1
snail_respawning_prob = 0.01
bird = pygame.image.load("./graphics/Fly/Fly1.png").convert_alpha()
obstacle_manager.add_object(bird, 8, 100)
obstacle_manager.add_object(snail, 2, 300)


player_over_surf = pygame.transform.rotozoom(pygame.image.load("./graphics/Player/player_stand.png"), 0, 2).convert_alpha()
player_stand_surf = pygame.image.load("./graphics/Player/player_stand.png").convert_alpha()
player_surface = player_stand_surf
player_rect = player_surface.get_rect(bottomleft=(100, 300))
player_walk_1 = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("./graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_walk_index = 0
player_jump = pygame.image.load("./graphics/Player/jump.png").convert_alpha()
player_vy = 0

# game settings and constants
FASTER_SNAIL = True
JUMP_V = 15
GRAVITY_CONSTANT = 0.8

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)
speed_timer = pygame.USEREVENT + 2
pygame.time.set_timer(speed_timer, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state == "ONG":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and event.button == pygame.BUTTON_LEFT:
                    player_vy = -JUMP_V

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_vy -= JUMP_V
            
            if event.type == obstacle_timer:
                obstacle_manager.spawn()
                print("spwaning")
                print(f"number of obstacles {obstacle_manager.obstacles.__len__()}") 
            if event.type == speed_timer:
                obstacle_manager.update_speed()
        elif game_state == "OVR":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "ONG"
                # reset game
                obstacle_manager.reset()
                player_rect = player_surface.get_rect(bottomleft=(100, 300))
                player_vy = 0
                start_time = pygame.time.get_ticks()
        elif game_state == "STR":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                game_state = "ONG"
                start_time = pygame.time.get_ticks()
        
        

    if game_state == "ONG":
        
        mos_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        main_screen.blit(sky_surface, (0, 0))
        main_screen.blit(ground_surface, ground_rect)

        display_text_at(main_screen, f"score: {get_curr_score()}", game_font, WIDTH // 2, 50)
        # main_screen.blit(snail, snail_rect)
        obstacle_manager.update_position()
        obstacle_manager.draw(main_screen)
        main_screen.blit(player_surface, player_rect)
        
        # if snail_rect.right <= 0: # replace snail if out frame
        #     snail_rect.left = 800
        # else:
        #     snail_rect.left -= snail_speed

        # if FASTER_SNAIL:
        #     snail_speed += 0.01

        if player_rect.left > WIDTH: # replace player if out frame
            player_rect.right = 0
        elif player_rect.right < 0:
            player_rect.left = WIDTH
        
        # move player according to input
        if keys[pygame.K_d]:
            player_rect.left += 4
        if keys[pygame.K_a]:
            player_rect.left -= 4

        if player_rect.bottom < 300:
            player_vy += GRAVITY_CONSTANT
            player_surface = player_jump
        else: # readjust the position to be on the ground
            if keys[pygame.K_a] and keys[pygame.K_d]:
                player_surface = player_stand_surf
            elif keys[pygame.K_d]:
                player_walk_index += 0.05
                player_surface = player_walk[int(player_walk_index) % 2]
            elif keys[pygame.K_a]:
                player_walk_index -= 0.05
                player_surface = player_walk[int(player_walk_index) % 2]
            else:
                player_surface = player_stand_surf
            

            if player_vy > 0: # on the ground falling results in a stop
                player_vy = 0
                player_rect.bottom = 300


        if obstacle_manager.any_collide_with(player_rect):
            game_state = "OVR"
            score = get_curr_score()

        player_rect.bottom += player_vy
    elif game_state == "OVR":
        main_screen.fill("pink")
        main_screen.blit(player_over_surf, player_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        display_text_at(main_screen, f"score: {score}", game_font, WIDTH // 2, HEIGHT * 4 // 5)
        main_screen.blit(over_text_surf, over_text_rect)
    elif game_state == "STR":
        main_screen.fill("pink")
        main_screen.blit(player_over_surf, player_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        display_text_at(main_screen, f"PixelRunner", game_font, WIDTH // 2, HEIGHT * 1 // 5)
        display_text_at(main_screen, "Press the key s to start", game_font, WIDTH // 2, HEIGHT * 5 // 6)
    


    # actions
    pygame.display.update()
    clock.tick(60) # a ceiling to the framerate