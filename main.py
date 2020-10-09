from collections import namedtuple
import cv2

from mask import Mask
from camera import Webcam

ColorRGB = namedtuple("ColorRGB", ["R", "G", "B"])
ColorHSV = namedtuple("ColorHSV", ["H", "S", "V"])

if __name__ == "__main__":
    # Define windows
    camera = Webcam()

    colors = {
            "white" : (255,255,255),
            "black" : (0,0,0),
            "red" : (255,0,0),
            "yellow" : (255,255,0),
            "green" : (0,255,0),
            "blue" : (0,0,255),
            "purple" : (128,0,128),
            "orange" : (255,165,0)
            }
    color_masks = [
            Mask(
                name=name, 
                color_rgb=ColorRGB(color[0], color[1], color[2])
                )
            for name, color in colors.items()
            ]
    for color in color_masks:
        camera.add_mask(color)
    # Drawing loop
    while(True):
        camera.draw()

        # allow exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    camera.destroy()
    # Destroy all windows 
    cv2.destroyAllWindows()
