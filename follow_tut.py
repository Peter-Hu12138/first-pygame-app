import pygame
import random
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

# more init
game_state = "ONG"
"""
ONG - onoging
PAU - paused
OVR - over
"""

sky_surface = pygame.image.load("./graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load("./graphics/ground.png").convert_alpha()
ground_rect = ground_surface.get_rect(topleft=(0, 300))

over_text_surf = game_font.render("OVER - press esc to start over", 1, "cyan")
over_text_rect = over_text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 5))

snail = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
snail_rect = snail.get_rect(bottomleft=(800, 300))
snail_speed = 1
snail_respawning_prob = 0.01

player_stand_surf = pygame.transform.rotozoom(pygame.image.load("./graphics/Player/player_stand.png"), 0, 2).convert_alpha()
player_surface = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(bottomleft=(100, 300))
player_vy = 0
JUMP_V = 15
GRAVITY_CONSTANT = 0.8

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state == "ONG":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and event.button == pygame.BUTTON_LEFT:
                    player_vy -= JUMP_V

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_vy -= JUMP_V

        elif game_state == "OVR":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "ONG"
                # reset game
                snail_rect = snail.get_rect(bottomleft=(800, 300))
                player_rect = player_surface.get_rect(bottomleft=(100, 300))
                player_vy = 0
                start_time = pygame.time.get_ticks()

    if game_state == "ONG":
        
        mos_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        main_screen.blit(sky_surface, (0, 0))
        main_screen.blit(ground_surface, ground_rect)

        display_text_at(main_screen, f"score: {get_curr_score()}", game_font, WIDTH // 2, 50)
        main_screen.blit(snail, snail_rect)
        main_screen.blit(player_surface, player_rect)
        
        if snail_rect.right <= 0: # replace snail if out frame
            snail_rect.left = 800
        else:
            snail_rect.left -= 2

        if player_rect.left > WIDTH: # replace player if out frame
            player_rect.right = 0
        elif player_rect.right < 0:
            player_rect.left = WIDTH
                
        if keys[pygame.K_d]:
            player_rect.left += 4
        elif keys[pygame.K_a]:
            player_rect.left -= 4

        if player_rect.bottom < 300:
            player_vy += GRAVITY_CONSTANT
        else: # readjust the position to be on the ground
            if player_vy > 0: # on the ground falling results in a stop
                player_vy = 0
                player_rect.bottom = 300


        if player_rect.colliderect(snail_rect):
            game_state = "OVR"
            score = get_curr_score()

        player_rect.bottom += player_vy
    elif game_state == "OVR":
        main_screen.fill("pink")
        main_screen.blit(player_stand_surf, player_stand_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        display_text_at(main_screen, f"score: {score}", game_font, WIDTH // 2, HEIGHT * 4 // 5)
        main_screen.blit(over_text_surf, over_text_rect)
    


    # actions
    pygame.display.update()
    clock.tick(60) # a ceiling to the framerate