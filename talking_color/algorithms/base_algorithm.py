from collections import namedtuple
from typing import List

import numpy as np

ColorResult = namedtuple("ColorResult", ["name", "ratio"])


class ColorDetectionResult:
    def __init__(self, color_list: List[ColorResult], labelled_frame: np.ndarray):
        self.color_list = color_list
        self.labelled_frame = labelled_frame


class ColorDetectionAlgorithm:
    def run(self, frame) -> ColorDetectionResult:
        raise NotImplementedError
