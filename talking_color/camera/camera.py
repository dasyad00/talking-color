import numpy as np

from audio_output import say
from talking_color.algorithms.base_algorithm import ColorDetectionAlgorithm

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


class Camera:
    def __init__(self, window_name, algorithm=None):
        self.window_name = window_name
        self.algorithm: ColorDetectionAlgorithm = algorithm

    def output_sound(self, frame: np.ndarray):
        color = self.algorithm.run(frame).color_list[0]
        text = f"This is {color.name} taking up {round(color.ratio * 100, 1)}%"

        # print output to screen
        print(text)
        # audible output
        say(text)

    def process_video(self):
        raise NotImplementedError

    def process_image(self):
        raise NotImplementedError

    def destroy(self):
        # release the capture
        pass
