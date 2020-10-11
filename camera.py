import cv2
from mask import Mask
from audio_output import say


class Camera:
    def __init__(self, window_name):
        self.window_name = window_name
        self.masks = []
        self.frame = None
        super().__init__()

    def add_mask(self, mask: Mask):
        self.masks.append(mask)

    def apply_masks(self):
        for mask in self.masks:
            self.frame = mask.draw_percentage(self.frame)

    def draw(self):
        # capture webcam input
        _, self.frame = self._cap.read()
        self.apply_masks()
        self.dominant_mask = max(self.masks)

    def draw_loop(self):
        # capture webcam input
        _, self.frame = self._cap.read()
        self.apply_masks()
        self.dominant_mask = max(self.masks)

    def destroy(self):
        # release the capture
        pass


class Webcam(Camera):
    # Adapted from OpenCV-Python Tutorials
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
    def __init__(self, window_name="Webcam"):
        super().__init__(window_name)
        # define webcam input
        self._cap = cv2.VideoCapture(0)
        # define window size
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def draw_loop(self):
        super().draw_loop()
        # draw output of webcam
        cv2.imshow(self.window_name, self.frame)

    def draw(self):
        super().draw()
        # audible output
        mask = self.dominant_mask
        text = f"{mask.name} is {mask.percentage}"
        print(text)
        say(text)

    def destroy(self):
        # release the capture
        self._cap.release()
