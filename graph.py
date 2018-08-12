import sys
import time
import os

# x-axis
max_hz = 8000
div_hz = 80
max_x = div_hz
step_hz = max_hz / div_hz

# y-axis
max_amp = 50
div_amp = 25
max_y = div_amp
step_amp = max_amp / div_amp

image_ary = [[0 for i in range(max_x)] for j in range(max_y)]

def set_pixel(x, y, val):
    image_ary[y][x] = val

def get_pixel(x, y):
    return image_ary[y][x]

def disp_image():
    os.system('clear')
    for y in range(max_y):
        line_x = ""
        for x in range(max_x):
            val = get_pixel(x, y)
            if val == 0:
                c = "0"
            else:
                c = "1"
            line_x += c
        print(line_x)

print(image_ary)

for y in range(max_y):
    set_pixel(2, y, 1)

for f in range(10):
    disp_image()
    time.sleep(0.5)