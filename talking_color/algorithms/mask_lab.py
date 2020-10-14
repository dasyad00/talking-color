from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2


class MaskLAB:
    """
    Adapted from PyImageSearch
    https://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/
    https://www.pyimagesearch.com/2016/02/15/determining-object-color-with-opencv/
    """

    def __init__(self):
        colors = OrderedDict({
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255)
        })

        # allocate memory for CIELAB image
        self.lab = np.zeros(
            (len(colors, 1, 3)),
            dtype="uint8"
        )
        # init color names list
        self.color_names = []

        # loop over colors dict
        for (i, (name, rgb)) in enumerate(colors.items()):
            # update CIELAB array
            self.lab[i] = rgb
            self.color_names.append(name)

        # convert CIELAB array rom the RGB color space
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def process_image(self, frame: np.ndarray):

        for row in frame:
            for pixel in row:
                pass
                pixel
            pass
        # init the minimum distance found thus far
        min_dist = (np.inf, None)

        # loop over the known CIELAB color values
        for (i, row) in enumerate(self.lab):
            # compute the distance between the current CIELAB color value
            # and a pixel
            # TODO iterate through list of pixels
            d = dist.euclidean(row[0], mean)

            # if distance is smaller tha nthe current distance,
            # then update min_dist
            if d < min_dist[0]:
                min_dist = (d, i)

        return self.color_names[min_dist[1]]
        # # blur image slightly
        # blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        # gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        # lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)

    def foo(self):
        pass
