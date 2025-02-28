from dataclasses import dataclass
import pygame
import random

class Obstacle:
    surf: pygame.surface.Surface
    rect: pygame.rect.Rect
    speed: float

    def __init__(self, surf: pygame.surface.Surface, rect: pygame.rect.Rect, speed: float):
        self.surf = surf
        self.rect = rect
        self.speed = speed
    
    def move(self) -> None:
        self.rect.left -= self.speed


    def out_boundary(self) -> bool:
        return self.rect.right <= -100
    
    

@dataclass
class Setting:
    surf: pygame.Surface
    speed: float
    spawn_height: int

    def update_speed(self) -> None:
        if self.speed <= 15:
            self.speed *= 1.000001
        else:
            self.speed += 0.00005

class Manager:
    obstacles: list[Obstacle]
    run_time_settings: list[Setting]
    initial_settings: list[Setting]
    display_width: int

    def __init__(self, width: int):
        self.obstacles = []
        self.run_time_settings = []
        self.initial_settings = []
        self.display_width = width

    def add_object(self, surf: pygame.surface.Surface, speed: float, spwan_height: int):
        self.run_time_settings.append(Setting(surf, speed, spwan_height))
        self.initial_settings.append(Setting(surf, speed, spwan_height))

    def spawn(self):
        rand_setting = self.run_time_settings[random.randint(0, len(self.run_time_settings) - 1)]
        spwaned_surf = rand_setting.surf
        spwaned_x_pos = random.randint(self.display_width * 1.1 // 1, self.display_width * 1.2 // 1)
        initial_rect = spwaned_surf.get_rect(bottomleft=(spwaned_x_pos, rand_setting.spawn_height))
        new_obstacle = Obstacle(surf=spwaned_surf, rect=initial_rect, speed=rand_setting.speed)
        self.obstacles.append(new_obstacle)

    def update_position(self):
        for obstacle in self.obstacles[:]: # iterate over a clone reference list to avoid weird remove-iteration problem
            obstacle.move()
            if obstacle.out_boundary(): # remove if object out of frame
                self.obstacles.remove(obstacle)

    def update_speed(self):
        for object in self.run_time_settings:
            object.speed += 0.005
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            screen.blit(obstacle.surf, obstacle.rect)

    def reset(self):
        self.obstacles = []

    def any_collide_with(self, rect: pygame.Rect):
        for obstacle in self.obstacles:
            if obstacle.rect.colliderect(rect):
                return True
        return False