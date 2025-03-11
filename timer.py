import pygame

class Timer:
    """Represents a single digit of the timer display

    ---Attributes---
    x: int
        x coordinate of upper left corner of the image
    y: int
        y coordinate of upper left corner of the image
    number: int
        The digit that is displayed
    image: Surface
        The image to display for the digit
    image_size: Tuple[int, int]
        The size of the image in pixels
    rect: Pygame.Rect
        The rectangle of the image
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.number = 0
        self.image = pygame.image.load(f"TimerNumbers/timer_{self.number}.png")
        self.image = pygame.transform.scale(self.image, (26, 46))
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])

    def update(self, number: int):
        """Updates the image with the updated digit
        
        ---Parameters---
        number: int
            The digit that should be displayed
        """
        self.number = number
        self.image = pygame.image.load(f"TimerNumbers/timer_{self.number}.png")
        self.image = pygame.transform.scale(self.image, (26, 46))