import time

import cv2
import numpy as np
from mask import Mask
from audio_output import say

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


class Camera:
    def __init__(self, window_name):
        self.window_name = window_name
        self.masks = []

    def add_mask(self, mask: Mask):
        self.masks.append(mask)

    def get_dominant_mask(self, frame: np.ndarray):
        self.apply_masks(frame)
        return max(self.masks)

    def output_dominant_mask(self, frame: np.ndarray):
        mask = self.get_dominant_mask(frame)
        text = f"{mask.name} is {mask.percentage}"
        # print output to screen
        print(text)
        # audible output
        say(text)

    def apply_masks(self, frame: np.ndarray, draw_on_frame=False):
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


class Webcam(Camera):
    """
    Adapted from OpenCV-Python Tutorials
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
    """

    def __init__(self, window_name="Webcam"):
        super().__init__(window_name)
        # define webcam input
        self.capture = cv2.VideoCapture(0)
        # define window size
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    def process_video(self):
        # begin frame loop
        while True:
            _, frame = self.capture.read()

            # annotate frame
            drawn_frame = self.apply_masks(frame, draw_on_frame=True)
            # draw output of webcam
            cv2.imshow(self.window_name, drawn_frame)

            # allow exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def process_image(self):
        # capture image and get np array
        _, frame = self.capture.read()

        # process image
        self.apply_masks(frame)

        # display the image on screen
        cv2.imshow("Image", frame)
        # also output with text and audio
        self.output_dominant_mask(frame)

        # allow exit when any key is pressed
        print("Press any key to exit.")
        cv2.waitKey(0)

    def destroy(self):
        # release the capture
        self.capture.release()


class PiCamera(Camera):
    """
    Adapted from PyImageSearch
    https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
    """

    def __init__(self, window_name="PiCamera"):
        # Ensure object is created in RPi
        if not self.can_run():
            raise RuntimeError("PiCamera only allowed to be run via RPi. "
                               "Please use camera.Webcam for testing purposes.")

        from picamera.array import PiRGBArray
        from picamera import PiCamera

        # define camera
        self.camera = PiCamera()
        self.camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
        self.camera.framerate = 30
        # grab reference to the raw camera capture
        self.rawCapture = PiRGBArray(self.camera)

        # Allow camera to warm up
        time.sleep(0.1)
        super().__init__(window_name)

    @staticmethod
    def can_run() -> bool:
        import os
        return os.uname()[4][:3] == "arm"

    def add_mask(self, mask: Mask):
        super().add_mask(mask)

    def draw(self):
        self.camera.capture(self.rawCapture, format="bgr")
        image = self.rawCapture.array

    def process_video(self):
        # begin frame loop
        for frame in self.camera.capture_continuous(
                self.rawCapture,
                format="bgr",
                use_video_port=True
        ):
            # grab the raw numpy array representing the image
            image = frame.array

            self.apply_masks(image)

            # show the frame
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # allow exit when 'q' is pressed
            if key == ord("q"):
                break

    def process_image(self):
        # capture image and get np array
        self.camera.capture(self.rawCapture, format="bgr")
        image = self.rawCapture.array

        # process image
        self.apply_masks(image)

        # display the image on screen
        cv2.imshow("Image", image)
        # also output with text and audio
        self.output_dominant_mask(image)

        # allow exit when any key is pressed
        print("Press any key to exit.")
        cv2.waitKey(0)
