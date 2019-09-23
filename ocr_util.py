import mnist
import numpy as np
from random import choice, randint
import cv2.cv2 as cv2


class DigitGenerator:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._images = mnist.train_images()
        self._lables = mnist.train_labels()
        self._digit_pool = dict()
        for i in range(10):
            self._digit_pool[i] = []
        for i in range(len(self._lables)):
            self._digit_pool[self._lables[i]].append(i)

    def gen_digit(self, digit: str):
        """ A function that create an image representing the given DIGIT, 
        which is randomly sampled from the MNIST dataset.
        The white areas on left and right sides are cropped.
        Returns an NumPy array representing the image.
        Parameters
        ----------
        digit: str
        A string representing the digit, e.g. "1"
        """
        img = self._images[choice(self._digit_pool[int(digit)])]
        left = right = 0
        for i in range(img.shape[1]):
            if(sum(img[:, i]) != 0):
                left = i
                break
        for i in reversed(range(img.shape[1])):
            if(sum(img[:, i]) != 0):
                right = i+1
                break
        return img[:, left:right]


def create_digit_sequence(number: str, image_width: int, min_spacing: int, max_spacing: int):
    """ A function that create an image representing the given number,
    with random spacing between the digits.
    Each digit is randomly sampled from the MNIST dataset.
    Returns an NumPy array representing the image.
    Parameters
    ----------
    number: str
    A string representing the number, e.g. "14543"
    image_width: int
    The image width (in pixel).
    min_spacing: int
    The minimum spacing between digits (in pixel).
    max_spacing: int
    The maximum spacing between digits (in pixel).
    """

    # The value of the params must be legal
    assert(min_spacing <= max_spacing)
    assert(image_width >= (len(number)-1)*min_spacing+len(number))

    dg = DigitGenerator()
    dig_imgs = []
    for i in number:
        dig_imgs.append(dg.gen_digit(i))

    total_digit_width = 0
    for i in dig_imgs:
        total_digit_width += i.shape[1]

    row_num = dig_imgs[0].shape[0]

    if(image_width <= (total_digit_width+(len(number)-1)*min_spacing)):
        alpha = (image_width-(len(number)-1)*min_spacing)/total_digit_width
        seq_img = cv2.resize(
            dig_imgs[0], (int(dig_imgs[0].shape[1]*alpha), row_num))
        for i in range(1, len(dig_imgs)):
            seq_img = np.concatenate(
                (seq_img, np.zeros([row_num, min_spacing])), axis=1)
            seq_img = np.concatenate((seq_img, cv2.resize(
                dig_imgs[i], (int(dig_imgs[i].shape[1]*alpha), row_num))), axis=1)
    else:
        cur_max_spacing = min(
            max_spacing, (image_width-total_digit_width)//(len(number)-1))
        seq_img = dig_imgs[0]
        for i in range(1, len(dig_imgs)):
            seq_img = np.concatenate(
                (seq_img, np.zeros([row_num, randint(min_spacing, cur_max_spacing)])), axis=1)
            seq_img = np.concatenate((seq_img, dig_imgs[i]), axis=1)

    if(seq_img.shape[1] < image_width):
        padding_left = (image_width-seq_img.shape[1])//2
        padding_right = image_width-seq_img.shape[1]-padding_left
        seq_img = np.concatenate(
            (np.zeros([row_num, padding_left]), seq_img, np.zeros([row_num, padding_right])), axis=1)

    return seq_img
