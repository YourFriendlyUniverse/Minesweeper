import pygame


class Tile:
    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.type = tile_type
        # type can be "mine", 0, 1, 2, 3, 4, 5, 6, 7 or 8
        self.revealed = False
        self.flagged = False
        self.image = pygame.image.load("tile_unrevealed.png")
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])

    def reveal(self, was_clicked):
        if not self.flagged and not self.revealed:
            self.revealed = True
            self.image = pygame.image.load(f"tile_{self.type}.png")

            if self.type == "mine" and was_clicked:
                self.revealed = True
                self.image = pygame.image.load(f"tile_mine_revealed.png")

            return self.type

    def flag_tile(self):
        if not self.flagged and not self.revealed:
            self.flagged = True
            self.image = pygame.image.load("tile_flagged.png")

        elif self.flagged and not self.revealed:
            self.flagged = False
            self.image = pygame.image.load("tile_unrevealed.png")
