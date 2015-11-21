from __future__ import print_function
import requests
import json

class DataManager(object):

    def __init__(self):
        self.url = ""

    def get_data(self):
        r = requests.get(self.url)
        print(r.status_code)
        print(r.headers['content-type'])
        return r.json()

    def insert_datum(self, data):
        print(data.json())

        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}

        r = requests.post(self.url, data=data.json(),
                          headers=headers)

        if(r.status_code != 406):
            raise Exception("POST response received was %s" % r.status_code)


    def edit_datum(self, id):
        return

    def delete_datum(self, id):
        r = requests.delete(self.url + "/" + str(id))
        if (r.status_code != 204):
            raise Exception("DELETE response received was %s" % r.status_code)

    def clear_database(self):
        data = self.get_data()
        for d in data:
            self.delete_datum(d["id"])

class Table(object):
    def __init__(self, x, y, width, height, name):
        self.name = name
        self.position_x = x
        self.position_y = y
        self.width = width
        self.height = height

    def json(self):
        return json.dumps(self.__dict__)


class Costumer(object):
    def __init__(self, first_name, last_name, phone, email, cards):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.cards = cards

    def json(self):
        return json.dumps(self.__dict__)


class TableDataManager(DataManager):

    def __init__(self):
        self.url = "http://bleepr.io/tables"


class CostumersDataManager(DataManager):
    # TOFIX: cards don't get added
    def __init__(self):
        self.url = "http://bleepr.io/customers"


class CardsDataManager(DataManager):

    def __init__(self):
        self.url = "http://bleepr.io/cards"


def slip_costumers():
    cd = CostumersDataManager()
    c = Costumer("Nantas", "Nardelli", "07592385707",
                 "nantas.nardelli+slip@gmail.com", [{"id":"1215573"}])
    cd.insert_datum(c)
    c = Costumer("Theo", "Scott", "01234567890", "theo.scott@gmail.com",
                 [{"id":"1231147"}])
    cd.insert_datum(c)


def slip_tables():
    dt = TableDataManager()
    dt.clear_database()
    t = Table(45,249,80,485, "One")
    dt.insert_datum(t)
    t = Table(300,60,180,100, "Two")
    dt.insert_datum(t)
    t = Table(480,60,180,100, "Three")
    dt.insert_datum(t)
    t = Table(220,440,180,100, "Four")
    dt.insert_datum(t)
    t = Table(400,440,180,100, "Five")
    dt.insert_datum(t)
    t = Table(300,250,180,100, "Six")
    dt.insert_datum(t)

def main():
    # slip_tables()
    slip_costumers()

if __name__ == "__main__":
    main()
