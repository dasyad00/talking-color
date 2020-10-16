import cv2

from talking_color.algorithms.eucledian_cielab import EucledianCIELAB
from talking_color.algorithms.eucledian_hsv import EucledianHSV
from talking_color.algorithms.eucledian_rgb import EucledianRGB
from talking_color.algorithms.mask import MaskAlgorithm
from talking_color.algorithms.mask_hsv import MaskHSV
from talking_color.camera import Webcam, PiCamera, Camera


def run():
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

    # algorithm = EucledianRGB()
    # algorithm = EucledianHSV()
    algorithm = EucledianCIELAB()
    # algorithm = MaskAlgorithm(hsv_masks)
    camera: Camera
    # Define camera
    if "-d" in sys.argv:
        # Debug mode - use webcam
        camera = Webcam(algorithm=algorithm)
    else:
        # Normal mode - attempt to use RPi camera
        camera = PiCamera(algorithm=algorithm)

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


if __name__ == "__main__":
    run()
