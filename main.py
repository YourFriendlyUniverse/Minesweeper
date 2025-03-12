import pygame
import time
import random
from tile import Tile
from timer import Timer

# TODO:
# add win checker
# add flags/mines left
# add menu screen (options for board size and number of mines)

# returns the x and y of the clicked tile, returns -1 for both values if a tile isn't clicked
def collided_tile_index(grid: list, position) -> tuple[int, int]:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (grid[y][x].rect.collidepoint(position)):
                return y, x
    return -1, -1

# reveals the tile the player clicked on
def check_grid(grid: list, position, flag: bool):
    y, x = collided_tile_index(grid, position)
    # if tile was clicked
    if y != -1 and x != -1:
        if flag:
            grid[y][x].flag_tile()
            # puts a flag on the tile
        elif grid[y][x].reveal(True) == "mine":
            return True
        else:
            return False

# generates the tiles' numbers for the surrounding number of mines
def give_numbers(grid: list):
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
def reveal_mine_locations(grid: list):
    for row in grid:
        for tile in row:
            tile.reveal(False)

# generates the inital grid
def generate_grid(number_of_mines: int, grid_height: int, grid_length: int) -> list:
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
def reveal_surrounding_tiles(grid: list):
    blank_tile_revealed = True
    while blank_tile_revealed:
        blank_tile_revealed = False
        y = 0
        for row in grid:
            x = 0
            for tile in row:
                # where to check relative to the center tile
                tile_surrounding_update = [[True, True, True],
                                        [True, False, True],
                                        [True, True, True]]
                if tile.type == 0 and tile.revealed:
                    # checks if tile is on the border to not get out of bounds error
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

                    # the y position of the tile to check, relative to the center tile
                    y_check = -1
                    # loops through all the surrounding tiles, and reveals them if they aren't on the border
                    for tile_row in tile_surrounding_update:
                        # the x position of the tile to check, relative to the center tile
                        x_check = -1
                        for check in tile_row:
                            if check:
                                # coordinites of the tile to check
                                tile_check = grid[y + y_check][x + x_check]
                                # allows the function to continue to check tiles if the tile that's going to be revealed hasn't been revealed, is blank, and isn't flagged
                                if tile_check.type == 0 and not tile_check.revealed and not tile_check.flagged:
                                    blank_tile_revealed = True
                                grid[y + y_check][x + x_check].reveal(True)
                            x_check += 1
                        y_check += 1
                x += 1
            y += 1

# reveals all unflagged tiles around an uncovered tile, given that the # of flags around it is equal to its number, returns True if a mine was uncovered, False otherwise
def chord(grid : list, position) -> bool:
    # where to check relative to the center tile
    tile_surrounding_update = [[True, True, True],
                                [True, False, True],
                                [True, True, True]]
    y, x = collided_tile_index(grid, position)
    # if a tile was clicked
    if (y != -1 and x != -1):
        if grid[y][x].revealed:
            mine_revealed = False
            # checks if tile is on the border to not get out of bounds error
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

            surrounding_flags = 0
            # the y position of the tile to check, relative to the center tile
            y_check = -1
            # loops through all the surrounding tiles, and checks if they're flagged and if so, adds 1 to the total surrounding number of flags
            for tile_row in tile_surrounding_update:
                # the x position of the tile to check, relative to the center tile
                x_check = -1
                for check in tile_row:
                    if check:
                        if grid[y + y_check][x + x_check].flagged:
                            surrounding_flags += 1
                    x_check += 1
                y_check += 1

            # if the number of flags matches the tile's number
            if grid[y][x].type == surrounding_flags:
                # the relative y position of the tile to reveal from the center tile
                y_rel_reveal = -1
                # loops thrugh all surrounding tiles, revealing all of them and checking if a mine was revealed
                for reveal_row in tile_surrounding_update:
                    # the relative x position of the tile to reveal from the center tile
                    x_rel_reveal = -1
                    for reveal in reveal_row:
                        # if the tile can be revealed and isnt flagged
                        if reveal and grid[y + y_rel_reveal][x + x_rel_reveal].flagged == False:
                            grid[y + y_rel_reveal][x + x_rel_reveal].reveal(True)
                            if (grid[y + y_rel_reveal][x + x_rel_reveal].type == "mine"):
                                mine_revealed = True
                        x_rel_reveal += 1
                    y_rel_reveal += 1
            return mine_revealed
    return False

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
# time variables
time_start = time.time()
time_ones_display = 0
time_tens_display = 0
time_hundreds_display = 0
# board size
height = 20
length = 20
BOARD_SIZE = (height, length)
# gameplay variables
menu_screen = True
number_of_mines = 60
flags_left = number_of_mines
run = True
win = False
lose = False
grid = generate_grid(number_of_mines, height, length)
grid = give_numbers(grid)
timer_numbers = []

for i in range(3):
    timer_numbers.append(Timer(26 * i, 0))

while run:
    # --- Main event loop --- #
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed_buttons = pygame.mouse.get_pressed()
            # checks if both right and left mouse buttons are down
            if (event.button == 1 or event.button == 3) and (mouse_pressed_buttons[0] and mouse_pressed_buttons[2]):
                if not lose:
                    lose = chord(grid, event.pos)
                    reveal_surrounding_tiles(grid)
                if lose:
                    # reveals all tiles if the player lost
                    reveal_mine_locations(grid)

            if event.button == 1:
                # checks for left mouse click
                if not lose:
                    # checks to see if the player has lost
                    lose = check_grid(grid, event.pos, False)
                    reveal_surrounding_tiles(grid)
                if lose:
                    # reveals all tiles if the player lost
                    reveal_mine_locations(grid)

            elif event.button == 3:
                # checks for right mouse click
                if not lose:    # prevents player from updating flags when the game is lost
                    check_grid(grid, event.pos, True)

        elif event.type == pygame.KEYDOWN:
            # restarts game if space is pressed after game end            
            if event.key == pygame.K_SPACE and (win or lose):
                menu_screen = True
                BOARD_SIZE = (height, length)
                run = True
                win = False
                lose = False
                grid = generate_grid(number_of_mines, height, length)
                grid = give_numbers(grid)
                flags_left = number_of_mines
                time_start = time.time()
                time_ones_display = 0
                time_tens_display = 0
                time_hundreds_display = 0
    if not (lose or win):
        time_running = round(time.time() - time_start)

    # timer calculation
    time_ones_display = time_running % 10
    time_tens_display = int((time_running % 100 - time_ones_display) / 10)
    time_hundreds_display = int((time_running % 1000 - time_tens_display - time_ones_display) / 100)
    # timer update
    timer_numbers[2].update(time_ones_display)
    timer_numbers[1].update(time_tens_display)
    timer_numbers[0].update(time_hundreds_display)

    screen.fill((143, 143, 143))
    # NO BLIT ZONE ABOVE
    # blits all tiles
    for row in grid:
        for tile in row:
            screen.blit(tile.image, tile.rect)
    # blits in timer
    for i in range(len(timer_numbers)):
        screen.blit(timer_numbers[i].image, timer_numbers[i].rect)

    pygame.display.update()