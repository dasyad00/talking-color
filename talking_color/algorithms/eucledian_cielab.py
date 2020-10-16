import cv2
import pandas as pd
import numpy as np
from webcolors import hex_to_rgb

from talking_color.algorithms.eucledian_rgb import EucledianRGB


class EucledianCIELAB(EucledianRGB):
    color_space = 'LAB'

    def _get_frame_in_color_space(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    @staticmethod
    def _get_processed_df(df_train) -> pd.DataFrame:
        # parse rgb values
        rgb_values = []
        for i in range(len(df_train)):
            rgb = hex_to_rgb(df_train['Hex'][i])
            rgb_values.append([rgb.red, rgb.green, rgb.blue])
        rgb_values_array = np.array([rgb_values], dtype=np.uint8)
        # convert to CIELAB
        hsv_values_array = cv2.cvtColor(rgb_values_array, cv2.COLOR_RGB2LAB)
        df = pd.DataFrame(hsv_values_array[0], columns=['L', 'A', 'B'])
        df_final = df_train.join(df)
        df_final['LAB'] = list(zip(df_final['L'], df_final['A'], df_final['B']))
        return df_final
