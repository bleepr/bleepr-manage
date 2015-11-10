from __future__ import print_function
import random
import csv
from PIL import Image, ImageDraw

class Table(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_bounding_points(self):
        x_0 = self.x - (self.width / 2)
        y_0 = self.y - (self.height / 2)
        x_1 = self.x + (self.width / 2)
        y_1 = self.y + (self.height / 2)
        print([x_0, y_0, x_1, y_1])
        return [x_0, y_0, x_1, y_1]

class Renderer(object):

    def __init__(self, mode="text", data_path=None):
        self.mode = mode
        self.data_path = data_path
        self.tables = list()
        self.colours = ["#F44336", # red
                        "#E91E63", # pink
                        "#9C27B0", # purple
                        "#673AB7", # deep purple
                        "#3F51B5", # indigo
                        "#2196F3", # blue
                        "#03A9F4", # light blue
                        "#00BCD4", # cyan
                        "#009688", # teal
                        "#4CAF50", # green
                        "#8BC34A", # light green
                        "#CDDC39", # lime
                        "#FFEB3B", # yellow
                        "#FFC107", # amber
                        "#FF9800", # orange
                        "#FF5722", # deep orange
                        "#795548", # brown
                        "#9E9E9E"] # grey

    def load_map(self, path):
        """
        Load a specific image to serve as the base map.
        """
        print("Loading map at %s" % (path))
        self.im = Image.open(path)
        self.draw = ImageDraw.Draw(self.im)
        print("Format: %s\nSize: %s\nMode: %s" %
              (self.im.format, self.im.size, self.im.mode))

    def load_data(self, path=None):
        """
        Load the restaurant data depending on the mode.
        """
        if self.mode == "text":
            self._load_text(path)
        elif self.mode == "db":
            return NotImplementedError

    def _load_text(self, path):
        with open(path, "rb") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                t = Table(eval(row[0]),
                          eval(row[1]),
                          eval(row[2]),
                          eval(row[3]))
                self.tables.append(t)

    def _draw_table(self, table):
        rcolour = random.choice(self.colours)
        self.draw.rectangle(table.get_bounding_points(),
                            outline="#000000", fill=rcolour)
        return None

    def add_tables(self):
        """
        Add the tables to the map object.
        Returns True if at least one table has been added.
        """
        flag = False
        for t in self.tables:
            flag = True
            self._draw_table(t)
        return flag

    def save_map(self, path):
        self.im.save(path, "PNG")


def main():
    r = Renderer()
    r.load_map("../share/test_map.png")
    r.load_data("../share/slip_room.txt")
    r.add_tables()
    r.save_map("../share/test_saved.png")



if __name__ == "__main__":
    main()
