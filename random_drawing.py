import pygame
import random
from sys import exit

WIDTH = 800
HEIGHT = 800

pygame.init()
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jingtian Hu's REAL first pygame project!")
clock = pygame.time.Clock()

# more init
next_clr_matrix = [[0 for y in range(HEIGHT)] for x in range(WIDTH)] # a dummy init to prefill the matrix
for x in range(WIDTH):
    for y in range(HEIGHT):
        r = int(random.random() * (255 + 1))
        g = int(random.random() * (255 + 1))
        b = int(random.random() * (255 + 1))
        color = pygame.Color(r, g, b)
        main_screen.set_at((x, y), color)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            num_of_pixels = 0
            r_total = 0
            g_total = 0
            b_total = 0
            for d_x in [-1, 0, 1]:
                for d_y in [-1, 0, 1]:
                    try:
                        color = main_screen.get_at((x + d_x, y + d_y))
                        num_of_pixels += 1
                    except:
                        color = pygame.Color(0, 0, 0)
                    finally:
                        r_total += color.r
                        g_total += color.g
                        b_total += color.b
            next_clr_matrix[x][y] = pygame.Color(int(r_total / num_of_pixels), int(g_total / num_of_pixels), int(b_total / num_of_pixels))
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            main_screen.set_at((x, y), next_clr_matrix[x][y])

    # for x in range(WIDTH):
    #     for y in range(HEIGHT):
    #         r = int(random.random() * (255 + 1))
    #         g = int(random.random() * (255 + 1))
    #         b = int(random.random() * (255 + 1))
    #         color = pygame.Color(r, g, b)
    #         main_screen.set_at((x, y), color)

    # actions
    pygame.display.update()
    clock.tick(60) # a ceiling to the framerate