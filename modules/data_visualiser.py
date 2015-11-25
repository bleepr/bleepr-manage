from __future__ import print_function
from operator import add
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
        x, y = self.load_heatmap_data("share/heatmap_data.txt")
        plt.imshow(self.img, zorder=0, alpha=1)
        plt.hist2d(x, y, alpha=0.5, bins=30)
        plt.xlim([0, self.img_width])
        plt.ylim([0, self.img_height])
        plt.axis('off')
        plt.savefig("static/heatmap.png", pad_inches=0)
        plt.close()

    def save_order_hist(self):
        morning = [11, 15, 40, 20, 30, 10, 26, 70, 60, 40, 10, 20]
        afternoon = [21, 35, 53, 30, 32, 15, 38, 71, 45, 39, 18, 21]
        evening = [30, 32, 73, 20, 12, 35, 58, 21, 24, 89, 12, 33]
        y = map(add, morning, afternoon)
        y = map(add, y, evening)
        x = range(1, 13)
        plt.plot(x, y, color='r')
        plt.xlim(1, 12)
        plt.ylim(0, 200)
        plt.title('Total order history of the past 12 months')
        plt.savefig("static/ord_hist.png", pad_inches=0)
        plt.close()

        plt.plot(x, morning, color='c')
        plt.xlim(1, 12)
        plt.ylim(0, 200)
        plt.title('History of morning orders in the past 12 months')
        plt.savefig("static/ord_hist_morn.png", pad_inches=0)
        plt.close()

        plt.plot(x, afternoon, color='g')
        plt.xlim(1, 12)
        plt.ylim(0, 200)
        plt.title('History of afternoon orders in the past 12 months')
        plt.savefig("static/ord_hist_after.png", pad_inches=0)
        plt.close()

        plt.plot(x, evening, color='b')
        plt.xlim(1, 12)
        plt.ylim(0, 200)
        plt.title('History of evening orders in the past 12 months')
        plt.savefig("static/ord_hist_even.png", pad_inches=0)
        plt.close()

    def save_happiness(self):
        good = [3, 4, 5, 6, 8, 10, 3, 5, 2, 10,
                9, 8, 7, 8, 7, 5, 1, 2, 6, 7,
                4, 3, 4, 1, 1, 0, 10, 6, 6, 6]
        bad  = [0, 1, 0, 2, 0, 0, 5, 3, 0, 0,
                1, 1, 3, 4, 2, 3, 4, 5, 2, 1,
                2, 3, 4, 5, 6, 7, 0, 1, 0, 0]

        x = range(1, 31)
        plt.plot(x, good, color='g')
        plt.plot(x, bad, color='r')
        plt.xlim(1, 12)
        plt.ylim(0, 20)
        plt.title('Happiness (green) history vs unhappiness history (red) in the past month.')
        plt.savefig("static/happ.png", pad_inches=0)
        plt.close()

def main():
    d = DataVisualiser()
    d.get_base_image('../share/base_image.png')
    d.save_heatmap()



if __name__ == "__main__":
    main()
