import sys
import time
import os


class ImageConsole:
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

    def clear(self):
        for y in range(self.MAX_Y):
            for x in range(self.MAX_X):
                self.set_pixel(x, y, 0)

    def show(self):
        os.system('clear')
        for y in range(self.MAX_Y):
            line_x = ""
            for x in range(self.MAX_X):
                val = self.get_pixel(x, y)
                if val == 0:
                    c = " "
                else:
                    c = "A"
                line_x += c
            print(line_x)


def main():
    image = ImageConsole()

    for f in range(10):
        image.show()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
