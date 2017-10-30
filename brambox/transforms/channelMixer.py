#
#   Copyright EAVISE
#   By Tanguy Ophoff
#

import cv2
import numpy as np

__all__ = ['ChannelMixer']


class ChannelMixer:
    """ Mix channels of multiple inputs in a single output image """

    def __init__(self, num_channels=3):
        self.num_channels = num_channels
        self.channels = [(0, i) for i in range(num_channels)]
        self.in_img = None

    def set_channels(self, channels):
        """ Set from which channels the output image should be created [list with (imageNumber, channelNumber) tupples] """
        if len(channels) != self.num_channels:
            raise ValueError('You should have one [image,channel] per output channel')
        self.channels = [(c[0], c[1]) for c in channels]

    def set_input_images(self, *imgs):
        """ Set input images """
        if len(imgs) <= 0:
            raise TypeError('You need at least one input image')
        self.in_img = imgs

    def get_output_image(self):
        """ Compute and return output image """
        m = max(self.channels, key=lambda c: c[0])[0]
        if m >= len(self.in_img):
            raise ValueError(f'One of your channels references an image that is not available ({m})')

        for c in self.channels:
            shape = self.in_img[c[0]].shape
            if len(shape) < 3:
                c_count = 1
            else:
                c_count = shape[2]
            if c[1] >= c_count:
                raise ValueError(f'One of your channels references a channel that does not exist in the input image ({c[0]},{c[1]})')

        img_splits = [cv2.split(img) for img in self.in_img]
        merge_channels = [img_splits[c[0]][c[1]] for c in self.channels]
        return cv2.merge(merge_channels)
