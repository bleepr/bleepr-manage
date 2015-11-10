from __future__ import print_function
import csv
import numpy as np
import matplotlib as mpl
mpl.use('Agg') # Allows it to work without X server
import matplotlib.pyplot as plt
from scipy.misc import imread

class DataVisualiser(object):

    def __init__(self):
        return None

    def get_base_image(self, path):
        """
        Load a specific image to serve as the base image for heatmaps
        graphs.
        """
        print("Loading map at %s" % (path))
        self.img = imread(path)
        self.img_height = self.img.shape[0]
        self.img_width = self.img.shape[1]

    def _add_parts(self, starting, matrices, no):
        for i in range(no):
            starting = (np.concatenate((starting[0], matrices[0])),
                        np.concatenate((starting[1], matrices[1])))
        return starting

    def load_heatmap_data(self, path):
        final = (np.ndarray(0,), np.ndarray(0,))
        with open(path, "rb") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                data_matrix_x = np.random.normal(eval(row[0]), 70,
                                                 5000)
                data_matrix_y = np.random.normal(eval(row[1]), 70,
                                                 5000)
                final = self._add_parts(final,
                                       (data_matrix_x, data_matrix_y),
                                       eval(row[2]))
        return final

    def save_heatmap(self):
        x, y = self.load_heatmap_data("../share/heatmap_data.txt")
        plt.imshow(self.img, zorder=0, alpha=1)
        plt.hist2d(x, y, alpha=0.5, bins=30)
        plt.xlim([0, self.img_width])
        plt.ylim([0, self.img_height])
        plt.axis('off')
        plt.savefig("../share/heatmap.png", pad_inches=0)

def main():
    d = DataVisualiser()
    d.get_base_image('../share/test_saved.png')
    d.save_heatmap()



if __name__ == "__main__":
    main()
