from __future__ import print_function
from PIL import Image, ImageDraw

class Table(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Renderer(object):

    def __init__(self, mode="text", data_path=None):
        self.mode = mode
        self.data_path = data_path

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
            return None
        elif self.mode == "db":
            return NotImplementedError

    def _draw_table(self, table):
        self.draw.line((0,0) + self.im.size, fill=128)
        self.draw.line((0, self.im.size[1], self.im.size[0], 0),
                       fill=128)
        return None

    def add_tables(self):
        t = Table(0, 0, 10, 10)
        self._draw_table(t)

    def save_map(self, path):
        self.im.save(path, "PNG")


def main():
    r = Renderer()
    r.load_map("../share/test_map.png")
    r.load_data("../share/data_table.txt")
    r.add_tables()
    r.save_map("../share/test_saved.png")



if __name__ == "__main__":
    main()
