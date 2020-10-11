from collections import namedtuple
import cv2

from mask import Mask, MaskHSV
from camera import Webcam

ColorRGB = namedtuple("ColorRGB", ["R", "G", "B"])
ColorHSV = namedtuple("ColorHSV", ["H", "S", "V"])

if __name__ == "__main__":
    import sys

    # Define windows
    camera = Webcam()

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

    # rgb_colors = {
    #     "white": (255, 255, 255),
    #     "black": (0, 0, 0),
    #     "red": (255, 0, 0),
    #     "yellow": (255, 255, 0),
    #     "green": (0, 255, 0),
    #     "blue": (0, 0, 255),
    #     "purple": (128, 0, 128),
    #     "orange": (255, 165, 0)
    # }
    # color_masks = [
    #     Mask(
    #         name=name,
    #         color_rgb=ColorRGB(color[0], color[1], color[2])
    #     )
    #     for name, color in rgb_colors.items()
    # ]
    # for color in color_masks:
    for mask in hsv_masks:
        camera.add_mask(mask)

    if "-v" in sys.argv:
        # Drawing loop
        while True:
            camera.draw_loop()

            # allow exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        # Take image
        camera.draw()
        # allow exit when 'q' is pressed
        cv2.waitKey(0)

    # When everything done, release the capture
    camera.destroy()
    # Destroy all windows 
    cv2.destroyAllWindows()
