import os

import math

import numpy
from PIL import Image
from cv2 import cv2


def save(image, name, dir):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(ROOT_DIR, 'images/' + dir, name + ".png")
    print(filename)
    try:
        image.save(filename)
    except Exception as e:
        print(e)
    finally:
        return filename


def find_lines(image):
    pixels = image.load()  # this is not a list
    width, height = image.size
    blank_lines = []
    prev = 0
    for y in range(height):
        cur_row = 0
        for x in range(width):
            cur_pixel = pixels[x, y]
            cur_pixel_mono = sum(cur_pixel) / len(cur_pixel)
            cur_row += cur_pixel_mono

        cur_row_avg = cur_row / width
        if cur_row_avg == 255:
            if y - prev > 1:
                blank_lines.append(y)
            prev = y

    return blank_lines


def slice_image(image, out_name):
    slice_coordinates = find_lines(image)
    del slice_coordinates[::2]
    width, height = image.size
    upper = 0
    left = 0

    count = 1
    slices_images = []

    for slice in slice_coordinates:
        lower = slice + 1
        box = (left, upper, width, lower)
        current_slice = image.crop(box)
        upper = slice
        filename = save(current_slice, out_name + "{}".format(count), 'cutted')
        slices_images.append(filename)
        count += 1

    return slices_images
