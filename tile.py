from PIL import Image
from os import getcwd, listdir


PATH = f"{getcwd()}\\tile sets\\Rooms"


def init_edges():
    global image_edges

    image_edges = {}
    edge_colours = {}
    files = listdir(PATH)
    for img_name in [i for i in files if ".png" in i or ".jpg" in i or ".jpeg" in i]:
        img = Image.open(f"{PATH}\\{img_name}")
        w, h = img.size

        vals = (0, 0.5, 0.99)
        edges = [[img.getpixel((w * i, 0)) for i in vals], [img.getpixel((w - 1, h * i)) for i in vals], [img.getpixel((w * i, h - 1)) for i in vals], [img.getpixel((0, h * i)) for i in vals]]
        
        colour_values = []
        for i in edges:
            colour_values.append([])
            for y in i:
                if y in edge_colours:
                    colour_values[-1].append(edge_colours[y])
                else:
                    edge_colours[y] = len(edge_colours)

        image_edges[img_name] = colour_values


class Tile:
    def __init__(self, img, x, y):
        self.image = img
        self.x = x
        self.y = y

        self.edges = self.get_edges()

    def get_edges(self):
        try:
            return image_edges[self.image]
        except NameError:
            init_edges()
            return image_edges[self.image]