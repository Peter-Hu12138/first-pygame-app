import pygame
import random
import math
import decimal
from sys import exit

def get_distance(c):
    return c[0] ** 2 + c[1] ** 2

def quad_map(z, c):
    return ((z[0] ** 2 - z[1] ** 2) + c[0], 2 * z[0] * z[1] + c[1])

def is_candidate(c, z=(0,0), n=10):
    if n == 0:
        if get_distance(quad_map(z, c)) == 0 or get_distance(z) == 0:
            return True
        return -2 < get_distance(quad_map(z, c)) / get_distance(z) and get_distance(quad_map(z, c)) / get_distance(z) < 2
    else:
        return is_candidate(c, quad_map(z, c), n - 1)

WIDTH = 200
HEIGHT = 200

pygame.init()
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jingtian Hu's REAL first pygame project!")
clock = pygame.time.Clock()

origin = (WIDTH // 2, HEIGHT // 2)

# more init
for x in range(WIDTH // 2):
    for y in range(HEIGHT // 2):
        for s_x in [-1, 1]:
            for s_y in [-1, 1]:
                if (origin[0] + s_x * x) >= WIDTH or (origin[0] + s_x * x) < 0:
                    continue
                if (origin[1] + s_y * y) >= HEIGHT or (origin[1] + s_y * y) < 0:
                    continue
                c_n = (decimal.Decimal(s_x * x / 100),decimal.Decimal(s_y * y / 100))
                if is_candidate(c_n):
                    print(f"{c_n} is candidate")
                    main_screen.set_at((int(origin[0] + c_n[0]), int(origin[1] + c_n[1])), pygame.Color(255, 255, 255))
                else:
                    print(f"{c_n} is not candidate")
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    

    # actions
    pygame.display.update()
    clock.tick(60) # a ceiling to the framerate