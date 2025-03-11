import pygame

class Tile:
    """Represents a single tile

    ---Attributes---
    x: int
        x coordinate of upper left corner of the image
    y: int
        y coordinate of upper left corner of the image
    type
        Denotes either the tile being a mine or amount of mines surrounding the tile, used to determine what image to show when the tile is revealed
    revealed: bool
        If the tile has been revealed
    flagged: bool
        If the tile has been flagged
    image: Surface
        The image to display for the tile
    image_size: Tuple[int, int]
        The size of the image in pixels
    rect: Pygame.Rect
        The hitbox of the tile, used to check if the tile has been clicked on
    """
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

    def reveal(self, was_clicked: bool):
        """reveals the tile type

        ---Parameters---
        was_clicked: bool
            Whether or not the tile being revealed was because it was clicked
            Only difference is in revealing mines, as if a mine is clicked, a different image is used for that tile than if it wasn't
        """
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
        """flags/unflags the tile"""
        # checks if the tile is already flagged and not revealed
        if not self.flagged and not self.revealed:
            self.flagged = True
            # changes the tile into a flagged tile
            self.image = pygame.image.load("Tiles/tile_flagged.png")
        # if the tile is already flagged, it unflags the tile
        elif self.flagged and not self.revealed:
            self.flagged = False
            self.image = pygame.image.load("Tiles/tile_unrevealed.png")
