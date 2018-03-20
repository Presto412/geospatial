"""module algoirithms/membership
"""

import os
from pprint import pprint

from PIL import Image

IMAGE1_FPATH = os.path.join("data", "cropped_1.png")
IMAGE2_FPATH = os.path.join("data", "cropped_2.png")
OUT_FPATH = os.path.join("output", "memberships.txt")

class Polygon():
    def __init__(self):
        self.membership1 = 0
        self.membership2 = 0

    def get_membership(self):
        return self.membership1, self.membership2


def calculate_membership(pixel_value, img):
    colors = img.getcolors()
    for color in colors:
        if color[1] == pixel_value:
            return float(color[0]) / float(img.width * img.height)
    return 0


def add_polygon(x, y, image, other_image):
    polygon = Polygon()
    polygon.membership1 = calculate_membership(image.getpixel((x, y)), image)
    polygon.membership2 = calculate_membership(
        image.getpixel((x, y)), other_image)
    return polygon


def main():
    """main function
    """
    image1 = Image.open(IMAGE1_FPATH).convert('L')
    image2 = Image.open(IMAGE2_FPATH).convert('L')
    width = image1.width
    height = image2.height
    polygon_list_1 = [
        add_polygon(x, y, image1, image2) for y in range(0, height)
        for x in range(0, width)
    ]
    print("list 1 done ")
    polygon_list_2 = [
        add_polygon(x, y, image2, image1) for y in range(0, height)
        for x in range(0, width)
    ]
    with open(OUT_FPATH, "w") as f:
        f.write('\n'.join('%s,%s' % i.get_membership()
                          for i in polygon_list_1 + polygon_list_2))
    # pprint([polygon.get_membership() for polygon in polygon_list_1])


if __name__ == '__main__':
    main()
