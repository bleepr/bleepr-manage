from __future__ import print_function
import requests
import json

class Table(object):
    def __init__(self, x, y, width, height, name):
        self.name = name
        self.position_x = x
        self.position_y = y
        self.width = width
        self.height = height

    def json(self):
        return json.dumps(self.__dict__)


class DataTableGenerator(object):

    def __init__(self):
        self.url = "http://bleepr.io/tables"

    def get_tables(self):
        r = requests.get(self.url)
        print(r.status_code)
        print(r.headers['content-type'])
        return r.json()

    def insert_table(self, table):
        print(table.json())

        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}

        r = requests.post(self.url, data=table.json(),
                          headers=headers)

        if(r.status_code != 406):
            raise Exception("POST response received was %s" % r.status_code)


    def edit_table(self, id):
        return

    def delete_table(self, id):
        r = requests.delete(self.url + "/" + str(id))
        if (r.status_code != 204):
            raise Exception("DELETE response received was %s" % r.status_code)

    def clear_database(self):
        data = self.get_tables()
        for d in data:
            self.delete_table(d["id"])


class CostumerDataGenerator(object):

    def get_costumers(self):
        return None

    def insert_costumer(self, costumer):
        return None

    def edit_costumer(self, id):
        return None

    def delete_costumer(self, id):
        return None


class CardsDataGenerator(object):

    def get_cards(self):
        return None

    def insert_card(self, card):
        return None

    def edit_card(self, id):
        return None

    def delete_card(self, id):
        return


def slip():
    dt = DataTableGenerator()
    dt.clear_database()
    t = Table(45,249,80,485, "One")
    dt.insert_table(t)
    t = Table(300,60,180,100, "Two")
    dt.insert_table(t)
    t = Table(480,60,180,100, "Three")
    dt.insert_table(t)
    t = Table(220,440,180,100, "Four")
    dt.insert_table(t)
    t = Table(400,440,180,100, "Five")
    dt.insert_table(t)
    t = Table(300,250,180,100, "Six")
    dt.insert_table(t)

def main():
    slip()

if __name__ == "__main__":
    main()
