import cv2
import numpy as np
import pandas as pd
import scipy.cluster
from scipy.spatial import distance
from webcolors import hex_to_rgb

from talking_color.algorithms.base_algorithm import ColorDetectionAlgorithm, ColorResult, ColorDetectionResult


class EucledianRGB(ColorDetectionAlgorithm):
    num_clusters = 5

    def __init__(self):
        # read color training data
        df_train = pd.read_csv('colour.csv', delimiter=';')
        # initiate color rgb dataframe
        self.df_colors = self._get_processed_rgb_df(df_train)

    def run(self, frame) -> ColorDetectionResult:
        color = self.get_most_common_color(self.num_clusters, frame)
        color_name = self.calc_distance(color, self.num_clusters)
        ratio = 1.0

        cv2.putText(
            frame,
            '{}: {}'.format(color_name, ratio),
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(255, 255, 255),
            lineType=2
        )
        return ColorDetectionResult(
            [ColorResult(color_name, 1.0)],
            frame
        )

    @staticmethod
    def _get_processed_rgb_df(df_train) -> pd.DataFrame:
        # convert hex code to RGB tuple
        rgb_tuple_list = []
        df_train['RGB'] = 0
        for i in range(len(df_train)):
            # Define rgb values
            rgb_value = hex_to_rgb(df_train['Hex'][i])
            rgb_tuple_list.append(rgb_value)
        df = pd.DataFrame(rgb_tuple_list, columns=['R', 'G', 'B'])
        df_final = df_train.join(df)
        df_final['RGB'] = list(zip(df_final['R'], df_final['G'], df_final['B']))
        return df_final

    @staticmethod
    def get_most_common_color(num_clusters, frame):
        # im = Image.open(file_path)
        # im = im.resize((150, 150))  # optional, to reduce time
        # ar = np.asarray(im)
        ar = frame

        shape = ar.shape
        ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
        codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
        counts, bins = np.histogram(vecs, len(codes))  # count occurrences
        index_max = np.argmax(counts)  # find most frequent
        peak = codes[index_max]
        print(type(peak))
        return peak

    def calc_distance(self, rgb_value, k=5):
        df_colors = self.df_colors.copy()
        df_colors['distance'] = 0
        for i in range(len(df_colors)):
            color_in_list = df_colors.loc[i, 'RGB']
            df_colors.loc[i, 'distance'] = distance.euclidean(rgb_value, color_in_list)
        df_colors.sort_values(['distance'], inplace=True)
        df_colors = df_colors.reset_index()

        final_color = self.veto(df_colors, 10)

        if not final_color:
            final_color = self.majority_vote(df_colors, k)
        return final_color

    @staticmethod
    def veto(df_colors, threshold):
        """
        Calculates the color value

        if the distance between the new point and the point with the shortest distance are
        within a threshold

        eg. Given a random point rgb(0,5,0), and black rgb(0,0,0) in csv

        :param df_colors:
        :param threshold:
        :return:
        """
        # whenver within the threshold
        # print(df_colors.head(5))
        if df_colors['distance'][0] <= threshold:
            color = df_colors['Group'][0]
        else:
            color = []
        return color

    @staticmethod
    def majority_vote(df_colors, k):
        dict_of_distances = {}
        for i in range(k):
            if df_colors['Group'][i] in dict_of_distances:
                dict_of_distances[df_colors['Group'][i]] += 1
            else:
                dict_of_distances[df_colors['Group'][i]] = 1
        return max(dict_of_distances, key=dict_of_distances.get)
