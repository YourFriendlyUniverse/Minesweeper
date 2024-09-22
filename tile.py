import pygame


class Tile:
    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.type = tile_type
        # type can be "mine", 0, 1, 2, 3, 4, 5, 6, 7 or 8
        self.revealed = False
        self.flagged = False
        self.image = pygame.image.load("Tiles/tile_unrevealed.png")
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])

    def reveal(self, was_clicked):
        # makes sure the tile isn't already revealed or flagged
        if not self.flagged and not self.revealed:
            # reveals itslef and updates its image
            self.revealed = True
            self.image = pygame.image.load(f"Tiles/tile_{self.type}.png")

            if self.type == "mine" and was_clicked:
                self.revealed = True
                self.image = pygame.image.load("Tiles/tile_mine_revealed.png")
            # returns "mine" which loses the game
            return self.type

        # only runs if the tile isnt a mine, is flagged, and was revealed because of a game loss
        elif not self.type == "mine" and not was_clicked and self.flagged:
            # shows the player they flagged the wrong tile when they lose the game
            self.image = pygame.image.load("Tiles/tile_flagged_wrong.png")

    def flag_tile(self):
        # checks if the tile is already flagged and not revealed
        if not self.flagged and not self.revealed:
            self.flagged = True
            # changes the tile into a flagged tile
            self.image = pygame.image.load("Tiles/tile_flagged.png")
        # if the tile is already flagged, it unflags the tile
        elif self.flagged and not self.revealed:
            self.flagged = False
            self.image = pygame.image.load("Tiles/tile_unrevealed.png")
