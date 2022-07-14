import pygame
from os import listdir, getcwd
from random import randint
from tile import Tile


PATH = f"{getcwd()}\\tile sets\\Rooms"
WIDTH, HEIGHT = 600, 600
TILES_X, TILES_Y = 20, 20


def init():
    global window
    global grid
    global tile_images

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wave Function Collapse Algorithm")

    grid = [[None for _ in range(TILES_X)] for _ in range(TILES_Y)]
    tile_images = get_tiles(PATH)


def get_tiles(path):
    files = listdir(path)
    return [i for i in files if ".png" in i or ".jpg" in i or ".jpeg" in i]


def is_possible(prev_tile, new_tile):
    if prev_tile.x == new_tile.x:
        if prev_tile.y > new_tile.y:
            #above
            return prev_tile.edges[0] == new_tile.edges[2]
        else:
            #below
            return prev_tile.edges[2] == new_tile.edges[0]
    else:
        if prev_tile.x > new_tile.x:
            #left
            return prev_tile.edges[3] == new_tile.edges[1]
        else:
            #right
            return prev_tile.edges[1] == new_tile.edges[3]


def get_entropy(x, y):
    entropy = 0
    for i in tile_images:
        possible = True
        possible_tile = Tile(i, x, y)

        for j in range(-1, 2):
            for k in range(-1, 2):
                if j != 0 and k != 0:
                    continue

                if 0 <= x + j < len(grid) and 0 <= y + k < len(grid[0]):
                    if grid[x + j][y + k] != None:
                        if not is_possible(grid[x + j][y + k], possible_tile):
                            possible = False

        if possible:
            entropy += 1

        del possible_tile

    return entropy


def place_tile(x, y):
    tiles = []
    for i in tile_images:
        possible = True
        possible_tile = Tile(i, x, y)

        for j in range(-1, 2):
            for k in range(-1, 2):
                if j != 0 and k != 0:
                    continue

                if 0 <= x + j < len(grid) and 0 <= y + k < len(grid[0]):
                    if grid[x + j][y + k] != None:
                        if not is_possible(grid[x + j][y + k], possible_tile):
                            possible = False

        if possible:
            tiles.append(possible_tile)
        else:
            del possible_tile

    return tiles


def check_done():
    for i in grid:
        if None in i:
            return False

    return True


def main():
    lowest_entropy = None
    tile_x, tile_y = 0, 0

    for i, x in enumerate(grid):
        for j, k in enumerate(x):
            if k == None:
                entropy = get_entropy(i, j)

                if lowest_entropy == None or entropy < lowest_entropy:
                    lowest_entropy = entropy
                    tile_x, tile_y = i, j

    tried = []
    possible_tiles = place_tile(tile_x, tile_y)

    while len(tried) < len(possible_tiles):
        tile_inx = randint(0, len(possible_tiles) - 1)

        if tile_inx not in tried:
            tried.append(tile_inx)
            grid[tile_x][tile_y] = possible_tiles[tile_inx]
            draw_tiles()

            if not check_done():
                main()
                grid[tile_x][tile_y] = None
                draw_tiles()
            else:
                finished()


def finished():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()


def draw_tiles():
    spacing_x = WIDTH // TILES_X
    spacing_y = HEIGHT // TILES_Y

    for j, i in enumerate(grid):
        for y, x in enumerate(i):
            if x != None:
                image = pygame.image.load(f"{PATH}\\{x.image}")
                image = pygame.transform.scale(image, (spacing_x, spacing_y))

                window.blit(image, (int(x.x * spacing_x), int(x.y * spacing_y)))
            else:
                pygame.draw.rect(window, (0, 0, 0), (j * spacing_x, y * spacing_y, spacing_x, spacing_y))

    pygame.display.update()


init()
main()