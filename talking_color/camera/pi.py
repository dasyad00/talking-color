import cv2

from talking_color.algorithms.mask import Mask
from talking_color.camera.camera import Camera, CAMERA_WIDTH, CAMERA_HEIGHT


class PiCamera(Camera):
    """
    Adapted from PyImageSearch
    https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
    """

    def __init__(self, window_name="PiCamera", color_detect=None):
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
        super().__init__(window_name, color_detect)

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
