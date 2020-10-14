import cv2

from talking_color.camera.camera import Camera, CAMERA_WIDTH, CAMERA_HEIGHT


class Webcam(Camera):
    """
    Adapted from OpenCV-Python Tutorials
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
    """

    def __init__(self, window_name="Webcam", algorithm=None):
        super().__init__(window_name, algorithm)
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
            new_frame = self.algorithm.run(frame).labelled_frame
            # draw output of webcam
            cv2.imshow(self.window_name, new_frame)

            # allow exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def process_image(self):
        # capture image and get np array
        _, frame = self.capture.read()

        # process image
        frame = self.algorithm.run(frame).labelled_frame

        # display the image on screen
        cv2.imshow("Image", frame)
        # also output with text and audio
        self.output_sound(frame)

        # allow exit when any key is pressed
        print("Press any key to exit.")
        cv2.waitKey(0)

    def destroy(self):
        # release the capture
        self.capture.release()
