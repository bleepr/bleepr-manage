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
        print("Inserting: ", data.json())

        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}

        r = requests.post(self.url, data=data.json(),
                          headers=headers)

        if(r.status_code != 406):
            raise Exception("POST response received was %s" % r.status_code)


    def edit_datum(self, id):
        return

    def delete_datum(self, id):
        print("Deleting %s" % id)
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
    def __init__(self, first_name, last_name, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    def json(self):
        return json.dumps(self.__dict__)


class Bleepr(object):
    def __init__(self, id, table_id, is_active):
        self.id = id
        # self.table_id = table_id
        self.is_active = is_active

    def json(self):
        return json.dumps(self.__dict__)

class TableDataManager(DataManager):

    def __init__(self):
        self.url = "http://bleepr.io/tables"


class CostumersDataManager(DataManager):

    def __init__(self):
        self.url = "http://bleepr.io/customers"

    def add_card(self, user_id, id):
        c = {"card": {"id": id}}

        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}

        s = self.url+ "/" + str(user_id) + "/cards"
        r = requests.post(s, data=json.dumps(c),
                          headers=headers)

        if(r.status_code != 406):
            raise Exception("POST response received was %s" % r.status_code)



class CardsDataManager(DataManager):

    def __init__(self):
        self.url = "http://bleepr.io/cards"

class BleeprsDataManager(DataManager):

    def __init__(self):
        self.url = "http://bleepr.io/bleeprs"


def slip_costumers():
    cd = CostumersDataManager()
    c = Costumer("Nantas", "Nardelli", "07592385707",
                 "nantas.nardelli+slip@gmail.com")
    cd.insert_datum(c)

def slip_bleeprs():
    bd = BleeprsDataManager()
    bd.clear_database()
    b = Bleepr("00:00:00:00:00", 45, 1)
    bd.insert_datum(b)
    b = Bleepr("00:00:00:00:01", 46, 0)
    bd.insert_datum(b)
    b = Bleepr("00:00:00:00:02", 47, 0)
    bd.insert_datum(b)
    b = Bleepr("00:00:00:00:03", 48, 0)
    bd.insert_datum(b)
    b = Bleepr("00:00:00:00:04", 49, 0)
    bd.insert_datum(b)
    b = Bleepr("00:00:00:00:05", 50, 0)
    bd.insert_datum(b)


def slip_tables():
    dt = TableDataManager()
    # WATCH OUT - Deletes occupancies as well!
    # dt.clear_database()
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
    slip_bleeprs()

if __name__ == "__main__":
    main()
