import argparse
import os
from random import randint
import cv2.cv2 as cv2

from ocr_util import create_digit_sequence

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, required=True,
                    help='The path you would save the image(s). (required)')
parser.add_argument('--num', type=int, default=1,
                    help='The amount of images you would create. (default: 1)')
parser.add_argument('--digits', type=int, required=True,
                    help='The number of the digits of every number you would create. (required)')
parser.add_argument('--width', type=int, required=True,
                    help='The image width (in pixel). (required)')
parser.add_argument('--min_spacing', type=int, default=0,
                    help='The minimum spacing between digits (in pixel). (default: 0)')
parser.add_argument('--max_spacing', type=int, default=28,
                    help='The maximum spacing between digits (in pixel). (default: 28)')
parser.add_argument('--form', type=str, default='jpg',
                    help='The image format. (default: jpg)')

args = parser.parse_args()

path = args.path
num = args.num
digits = args.digits
width = args.width
min_spacing = args.min_spacing
max_spacing = args.max_spacing
form = args.form

if(not os.path.isdir(path)):
    os.mkdir(path)

for i in range(num):
    number = ''
    for j in range(digits):
        number += str(randint(0, 9))

    img = create_digit_sequence(number, width, min_spacing, max_spacing)
    img_path = os.path.join(path, '{}_{}.{}'.format(i, number, form))
    cv2.imwrite(img_path, img)
