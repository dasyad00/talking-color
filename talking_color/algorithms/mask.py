import numpy as np
import cv2

ID = 1
COLOR_INTERVAL = 60


class Mask:
    # Adapted from Maker.pro
    # https://maker.pro/raspberry-pi/tutorial/how-to-create-object-detection-with-opencv

    def __init__(self, name="mask", color_rgb=None):
        global ID
        self.id = ID
        ID += 1
        self.name = name
        self.color_rgb = color_rgb
        self.ratio = 0.0

    def __gt__(self, other):
        return self.ratio > other.ratio

    def __ge__(self, other):
        return self.ratio >= other.ratio

    def calc_mask(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        color_rgb = self.color_rgb
        color = np.uint8([[[
            color_rgb.B,
            color_rgb.G,
            color_rgb.R
        ]]])
        hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
        lower_limit = np.uint8([hsv_color[0][0][0] - COLOR_INTERVAL, 100, 100])
        upper_limit = np.uint8([hsv_color[0][0][0] + COLOR_INTERVAL, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_limit, upper_limit)

        return mask

    def calculate_ratio(self, frame):
        mask = self.calc_mask(frame)
        self.ratio = cv2.countNonZero(mask) / (frame.size / 3)
        return self.ratio

    @property
    def percentage(self):
        return '{:03.1f}%'.format(self.ratio * 100)

    def draw_percentage(self, frame):
        ratio = self.calculate_ratio(frame)
        percentage = '{:03.1f}%'.format(ratio * 100)

        # add text
        cv2.putText(
            frame,
            '{}: {}'.format(self.name, percentage),
            (10, 25 * self.id),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(255, 255, 255),
            lineType=2
        )
        return frame

    def draw_mask(self, frame):
        mask = self.calc_mask(frame)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow(self.name, result)


