import pygame


class Timer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.number = 0
        self.image = pygame.image.load(f"TimerNumbers/timer_{self.number}.png")
        self.image = pygame.transform.scale(self.image, (26, 46))
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])

    def update(self, number):
        self.number = number
        self.image = pygame.image.load(f"TimerNumbers/timer_{self.number}.png")
        self.image = pygame.transform.scale(self.image, (26, 46))