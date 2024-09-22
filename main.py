import pygame
import time
import random
from tile import Tile

# add win checker
# add timer
# add flags left
# add menu screen (options for board size and number of mines)
# add auto resize window

# reveals the tile the player clicked on
def check_grid(grid, position, flag):
    for row in grid:
        for tile in row:
            if tile.rect.collidepoint(position):
                if flag:
                    tile.flag_tile()
                    # puts a flag on the tile
                elif tile.reveal(True) == "mine":
                    return True
                else:
                    return False

# generates the tiles' numbers
def give_numbers(grid):
    y = 0
    for row in grid:
        x = 0
        for tile in row:
            tile_surrounding_update = [[True, True, True],
                                      [True, False, True],
                                      [True, True, True]]
            if tile.type == "mine":
                # checks if tile is on the border to not update out of the list
                if x == 0:
                    tile_surrounding_update[0][0] = False
                    tile_surrounding_update[1][0] = False
                    tile_surrounding_update[2][0] = False
                elif x == len(row) - 1:
                    tile_surrounding_update[0][2] = False
                    tile_surrounding_update[1][2] = False
                    tile_surrounding_update[2][2] = False
                if y == 0:
                    tile_surrounding_update[0] = [False, False, False]
                elif y == len(grid) - 1:
                    tile_surrounding_update[2] = [False, False, False]

                y_check = -1
                for tile_row in tile_surrounding_update:
                    x_check = -1
                    for check in tile_row:
                        if check == True:
                            if grid[y + y_check][x + x_check].type != "mine":
                                # increments the number of the tile if there is a mine
                                grid[y + y_check][x + x_check].type += 1
                        x_check += 1
                    y_check += 1
            x += 1
        y += 1
    return grid

# reveals all tiles when you lose
def reveal_mine_locations(grid):
    for row in grid:
        for tile in row:
            tile.reveal(False)

# generates the inital grid
def generate_grid(number_of_mines, grid_height, grid_length):
    grid = []
    y = 0
    # generates base grid
    for i in range(grid_height):
        row = []
        x = 0
        for j in range(grid_length):
            # tiles are offset for top bar
            t = Tile(100 + x * 16, 100 + y * 16, 0)
            row.append(t)
            x += 1
        grid.append(row)
        y += 1
    # randomly assigns mines
    for i in range(number_of_mines):
        y = random.randint(0, grid_height - 1)
        x = random.randint(0, grid_length - 1)
        while grid[y][x].type == "mine":
            y = random.randint(0, grid_height - 1)
            x = random.randint(0, grid_length - 1)
        if grid[y][x].type != "mine":
            grid[y][x] = Tile(grid[y][x].x, grid[y][x].y, "mine")
        x = 0
    return grid

# reveals the surrounding tiles if the tile that was uncovered was blank
def reveal_surrounding_tiles(grid):
    blank_tile_revealed = True
    while blank_tile_revealed:
        blank_tile_revealed = False
        y = 0
        for row in grid:
            x = 0
            for tile in row:
                # where to check relative to the tile
                tile_surrounding_update = [[True, True, True],
                                        [True, False, True],
                                        [True, True, True]]
                if tile.type == 0 and tile.revealed:
                    # checks if tile is on the border to not update out of the list
                    if x == 0:
                        tile_surrounding_update[0][0] = False
                        tile_surrounding_update[1][0] = False
                        tile_surrounding_update[2][0] = False
                    elif x == len(row) - 1:
                        tile_surrounding_update[0][2] = False
                        tile_surrounding_update[1][2] = False
                        tile_surrounding_update[2][2] = False
                    if y == 0:
                        tile_surrounding_update[0] = [False, False, False]
                    elif y == len(grid) - 1:
                        tile_surrounding_update[2] = [False, False, False]

                    y_check = -1
                    for tile_row in tile_surrounding_update:
                        x_check = -1
                        for check in tile_row:
                            if check == True:
                                tile_check = grid[y + y_check][x + x_check]
                                # continues to check surrounding tiles if the tile hasn't been revealed, is blank, and isn't flagged
                                if tile_check.type == 0 and not tile_check.revealed and not tile_check.flagged:
                                    blank_tile_revealed = True
                                grid[y + y_check][x + x_check].reveal(True)
                            x_check += 1
                        y_check += 1
                x += 1
            y += 1


# pygame setup
pygame.init()
pygame.font.init()

# font setup
input_font = pygame.font.SysFont("Times", 15)
pygame.display.set_caption("Minesweeper!")

# set up variables for the display
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
# minimum screen sizes
min_screen_height = 100
min_screen_width = 100

# variable setup
menu_screen = True
height = 20
length = 20
BOARD_SIZE = (height, length)
number_of_mines = 60
flags_left = number_of_mines
run = True
win = False
lose = False
grid = generate_grid(number_of_mines, height, length)
grid = give_numbers(grid)
# message = input_font.render("TEST", True, (255, 255, 255))

while run:
    # --- Main event loop --- #
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # checks for left mouse click
                if not lose:
                    # checks to see if the player has lost
                    lose = check_grid(grid, event.pos, False)
                    reveal_surrounding_tiles(grid)
                if lose:
                    # reveals all tiles if the player lost
                    reveal_mine_locations(grid)

            if event.button == 3:
                # checks for right mouse click
                if not lose:    # prevents player from updating flags when the game is lost
                    check_grid(grid, event.pos, True)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (win or lose):
                menu_screen = True
                BOARD_SIZE = (height, length)
                run = True
                win = False
                lose = False
                grid = generate_grid(number_of_mines, height, length)
                grid = give_numbers(grid)
                flags_left = number_of_mines
                # restarts game if space is pressed after game end



    screen.fill((143, 143, 143))
    # NO BLIT ZONE ABOVE
    for row in grid:
        for tile in row:
            screen.blit(tile.image, tile.rect)
    # blits all tiles

    pygame.display.update()