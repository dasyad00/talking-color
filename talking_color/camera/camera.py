import time

import numpy as np

from talking_color.algorithms.color_detect import ColorDetect
from talking_color.algorithms.mask import Mask
from audio_output import say

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


class Camera:
    def __init__(self, window_name, color_detect=None):
        self.window_name = window_name
        self.masks = []
        self.color_detection: ColorDetect = color_detect

    def add_mask(self, mask: Mask):
        self.masks.append(mask)

    def get_dominant_mask(self, frame: np.ndarray):
        self.apply_masks(frame)
        return max(self.masks)

    def output_dominant_mask(self, frame: np.ndarray):
        if self.color_detection is not None:
            color = self.color_detection.get_most_common_color_name(5, frame)
            text = f"This is {color}"
        else:
            mask = self.get_dominant_mask(frame)
            text = f"{mask.name} is {mask.percentage}"
        # print output to screen
        print(text)
        # audible output
        say(text)

    def apply_masks(self, frame: np.ndarray, draw_on_frame=False):
        if self.color_detection is not None:
            return frame

        if draw_on_frame:
            for mask in self.masks:
                frame = mask.draw_percentage(frame)
        else:
            for mask in self.masks:
                mask.calculate_ratio(frame)
        return frame

    def process_video(self):
        raise NotImplementedError

    def process_image(self):
        raise NotImplementedError

    def destroy(self):
        # release the capture
        pass





