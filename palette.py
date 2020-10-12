import cv2


def on_change(x):
    # trackbar change listener
    pass


class ColorPalette:
    # Adapted from OpenCV-Python Tutorials
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_trackbar/py_trackbar.html

    def __init__(self, window_name="ColorPalette"):
        # define local constants
        self.window_name = window_name

        # define blank canvas
        self._blank_image = np.zeros((300, 512, 3), np.uint8)
        # define window
        cv2.namedWindow(self.window_name)
        # trackbars for blue, green and red
        cv2.createTrackbar("R", self.window_name, 0, 255, on_change)
        cv2.createTrackbar("G", self.window_name, 0, 255, on_change)
        cv2.createTrackbar("B", self.window_name, 0, 255, on_change)

    def draw(self):
        # get trackbars
        trackbars = self.trackbar_pos

        # change color of blank canvas
        self._blank_image[:] = [
            trackbars.B,
            trackbars.G,
            trackbars.R
        ]
        # draw colored blank canvas
        cv2.imshow(self.window_name, self._blank_image)

    @property
    def trackbar_pos(self):
        return ColorRGB(
            cv2.getTrackbarPos("R", self.window_name),
            cv2.getTrackbarPos("G", self.window_name),
            cv2.getTrackbarPos("B", self.window_name)
        )
