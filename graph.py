import sys
import time
import os


class ImageDisp:
    # x-axis
    MAX_HZ = 8000
    DIV_HZ = 80

    # y-axis
    MAX_AMP = 50
    DIV_AMP = 25

    MAX_X = DIV_HZ
    MAX_Y = DIV_AMP

    def __init__(self):
        self.image_ary = \
            [[0 for i in range(self.MAX_X)] for j in range(self.MAX_Y)]

    def set_pixel(self, x, y, val):
        self.image_ary[y][x] = val

    def get_pixel(self, x, y):
        return self.image_ary[y][x]

    def disp_image(self):
        os.system('clear')
        for y in range(self.MAX_Y):
            line_x = ""
            for x in range(self.MAX_X):
                val = self.get_pixel(x, y)
                if val == 0:
                    c = "0"
                else:
                    c = "1"
                line_x += c
            print(line_x)


def main():
    image = ImageDisp()

    for f in range(10):
        image.disp_image()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
