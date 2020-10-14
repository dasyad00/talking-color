from collections import namedtuple
import cv2

from talking_color.algorithms.color_detect import ColorDetect
from talking_color.algorithms.mask_hsv import MaskHSV
from talking_color.camera import Webcam, PiCamera, Camera

ColorRGB = namedtuple("ColorRGB", ["R", "G", "B"])
ColorHSV = namedtuple("ColorHSV", ["H", "S", "V"])

if __name__ == "__main__":
    import sys

    hue_colors = {
        "red": (-45, 15),
        "orange": (15, 45),
        "yellow": (45, 75),
        "green": (75, 150),
        # "cyan": (150, 210),
        # "blue": (210, 255),
        "blue": (150, 255),
        "purple": (255, 285),
        "pink": (285, 315)
    }
    hsv_masks = [
        MaskHSV(name, hue_range)
        for name, hue_range in hue_colors.items()
    ]

    camera: Camera
    # Define camera
    if "-d" in sys.argv:
        # Debug mode - use webcam
        camera = Webcam(
            color_detect=ColorDetect()
        )
    else:
        # Normal mode - attempt to use RPi camera
        camera = PiCamera(
            color_detect=ColorDetect()
        )

    for mask in hsv_masks:
        camera.add_mask(mask)

    if "-v" in sys.argv:
        # Drawing loop
        camera.process_video()
    else:
        # Single image
        camera.process_image()

    # When everything done, release the capture
    camera.destroy()
    # Destroy all windows 
    cv2.destroyAllWindows()
