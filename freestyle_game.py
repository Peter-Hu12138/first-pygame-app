import pygame
import random
from sys import exit

WIDTH = 800
HEIGHT = 400

pygame.init()
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jingtian Hu's REAL first pygame project!")
clock = pygame.time.Clock()
game_font = pygame.font.Font("./font/Pixeltype.ttf", 50)

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

score = 0
text_surface = game_font.render(f"score: {score}", 1, "cyan")
text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))

over_text_surf = game_font.render("OVER - press esc to start over", 1, "cyan")
over_text_rect = over_text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))

snail = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
snail_rect_list = []
snail_speed = 1
snail_respawning_prob = 0.0045

player_surface = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(bottomleft=(100, 300))
player_vy = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_state == "ONG":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and event.button == pygame.BUTTON_LEFT:
                    player_vy -= 10
                    print("event type collision")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    print("jump!")
                    player_vy -= 14

        elif game_state == "OVR":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = "ONG"
                # print("state changing to ongoing")
                snail_rect = snail.get_rect(bottomleft=(800, 300))
                player_rect = player_surface.get_rect(bottomleft=(100, 300))
                player_vy = 0

    if game_state == "ONG":
        if random.random() < snail_respawning_prob:
            snail_rect_list.append(snail.get_rect(bottomleft=(800, 300)))


        mos_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        main_screen.blit(sky_surface, (0, 0))
        main_screen.blit(ground_surface, ground_rect)

        text_surface = game_font.render(f"score: {score}", 1, "cyan")
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
        pygame.draw.rect(main_screen, "pink", text_rect)
        pygame.draw.rect(main_screen, "pink", text_rect, width=10)
        score += 3
        snail_respawning_prob += 0.000005
        snail_speed = 4 + score / 500
        main_screen.blit(text_surface, text_rect)
        for snail_rect in snail_rect_list:
            main_screen.blit(snail, snail_rect)
        main_screen.blit(player_surface, player_rect)

        for snail_rect in snail_rect_list:
            if player_rect.colliderect(snail_rect):
                game_state = "OVR"
                score = 0
                snail_rect_list = []
                snail_rect = None

        for snail_rect in snail_rect_list:
            if snail_rect.right <= 0: # replace snail if out frame
                snail_rect_list.remove(snail_rect)
            else:
                snail_rect.left -= snail_speed

        if player_rect.left > WIDTH: # replace player if out frame
            player_rect.right = 0
        elif player_rect.right < 0:
            player_rect.left = WIDTH
        
        if keys[pygame.K_d]:
            player_rect.left += 6
            print("d pressed")
        elif keys[pygame.K_a]:
            player_rect.left -= 6

        if player_rect.bottom < 300:
            player_vy += 0.7
        else:
            if player_vy > 0:
                player_vy = 0

        if player_rect.colliderect(ground_rect):
            print("player colliding with ground, adjusting")
            player_rect.bottom = 300
            
        

        player_rect.bottom += player_vy
    elif game_state == "OVR":
        main_screen.fill("pink")
        main_screen.blit(over_text_surf, over_text_rect)        
    


    # actions
    pygame.display.update()
    clock.tick(60) # a ceiling to the framerate