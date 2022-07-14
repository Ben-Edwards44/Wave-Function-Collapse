from PIL import Image
from os import getcwd, listdir


PATH = f"{getcwd()}\\tile sets\\Rooms"


def get_images(path):
    images = []
    files = listdir(path)
    for i in [i for i in files if ".png" in i or ".jpg" in i or ".jpeg" in i]:
        images.append(i)

    return images


def rotate(image_name):
    image = Image.open(f"{PATH}\\{image_name}")

    for i in range(90, 271, 90):
        new = image.rotate(i)
        new.save(f"{PATH}\\{i}_{image_name}")


def main():
    images = get_images(PATH)

    for i in images:
        rotate(i)


main()