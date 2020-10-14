from typing import Tuple

import cv2
import numpy as np

from constants import colored_bounds_saturation, colored_bounds_value
from talking_color.algorithms.mask import Mask


class MaskHSV(Mask):
    def __init__(self, name: str, hue_range: Tuple[int, int]):
        super().__init__()
        self.name = name
        if hue_range[0] > hue_range[1]:
            raise ValueError("Invalid hue_range")

        if hue_range[0] < 0:
            self.extra_lower_limit = np.uint8(
                [360 + hue_range[0], colored_bounds_saturation[0], colored_bounds_value[0]])
            self.extra_upper_limit = np.uint8([0, colored_bounds_saturation[1], colored_bounds_value[1]])
            self.lower_limit = np.uint8([0, colored_bounds_saturation[0], colored_bounds_value[0]])
            self.upper_limit = np.uint8([hue_range[1], colored_bounds_saturation[1], colored_bounds_value[1]])
        else:
            self.extra_lower_limit = None
            self.extra_upper_limit = None
            self.lower_limit = np.uint8([hue_range[0], colored_bounds_saturation[0], colored_bounds_value[0]])
            self.upper_limit = np.uint8([hue_range[1], colored_bounds_saturation[1], colored_bounds_value[1]])

    def calc_mask(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, self.lower_limit, self.upper_limit)

        if self.extra_lower_limit is not None and \
                self.extra_upper_limit is not None:
            extra_mask = cv2.inRange(hsv_frame, self.extra_lower_limit, self.extra_upper_limit)
            mask = cv2.bitwise_and(mask, extra_mask)

        return mask
