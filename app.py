import csv
import requests
import dateutil.parser

from flask import Flask, flash, redirect, url_for, request
from flask import get_flashed_messages, render_template, make_response
from flask.ext.login import LoginManager, UserMixin, login_required
from flask.ext.login import current_user, login_user, logout_user
from modules import renderer

from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)

class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO
    def tzname(self, dt):
        return "UTC"
    def dst(self, dt):
        return ZERO

utc = UTC()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'some_secret_key_wink_wink'

login_manager = LoginManager()
login_manager.login_view="signin"
login_manager.init_app(app)

r = renderer.Renderer(mode="api")

def refresh_table_image():
    r.load_map("share/base_image.png")
    r.load_data()
    r.add_tables()
    r.save_map("static/status.png")

class UserNotFoundError(Exception):
    pass


class User(UserMixin):
    def __init__(self, id):
        self.USERS = self.load_users_from_file("users.config")
        if id not in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]

    def load_users_from_file(self, config):
        users = {}
        with open(config, "rb") as csvfile:
            rows = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in rows:
                print row[0], row[1]
                users[row[0]] = row[1]
        return users

    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None


@login_manager.user_loader
def load_user(id):
    return User.get(id)


def add_user_to_config(user, password, config):
    fd = open(config, 'a')
    fd.write("\n" + user + " " + password)
    fd.close()


def get_dashboard_table_data():
    data = ["Bleepr id", "Table", "Active", "Occupied", "Time Spent", "Remaining time"]
    ids = []
    tables = []
    active = []
    occupied = []
    remaining_time = []
    time_spent = []
    bls = (requests.get("http://bleepr.io/bleeprs")).json()
    curs = (requests.get("http://bleepr.io/tables/occupied")).json()
    tabls = (requests.get("http://bleepr.io/tables")).json()

    for bl in bls:
        ids.append(bl['id'])
        i = next(index for (index, d) in enumerate(tabls)
                 if d["id"] == bl['table_id'])
        tables.append(tabls[i]["name"])
        active.append(bl['is_active'])
        if bl['table_id'] in curs['tables']:
            occupied.append("Yes")
        elif bl['is_active']:
            occupied.append("No")
        else:
            occupied.append("N/A")
        if bl['table_id'] not in curs['tables']:
            remaining_time.append("N/A")
        else:
            url = "http://bleepr.io/tables/" + str(bl['table_id']) + "/occupancies/current"
            print(url)
            oc = (requests.get(url)).json()
            print("###########################")
            print(oc)
            if not oc[0]["end"]:
                remaining_time.append("N/A")
            else:
                d = dateutil.parser.parse(oc[0]["end"]) - datetime.now(utc)
                minutes = int((d.total_seconds() % 3600) / 60)
                remaining_time.append(str(minutes) + " mins")
        if bl['table_id'] not in curs['tables']:
            remaining_time.append("N/A")
        else:
            url = "http://bleepr.io/tables/" + str(bl['table_id']) + "/occupancies/current"
            print(url)
            oc = (requests.get(url)).json()
            d  = datetime.now(utc) - dateutil.parser.parse(oc[0]["start"])
            minutes = int((d.total_seconds() % 3600) / 60)
            time_spent.append(str(minutes) + " mins")
    return [data, ids, tables, active, occupied, time_spent, remaining_time]

def get_settings_table_data():
    bls = (requests.get("http://bleepr.io/bleeprs")).json()
    ids = []
    tabls = []
    activs = []
    for bl in bls:
        ids.append(bl['id'])
        tabls.append(bl['table_id'])
        activs.append(bl['is_active'])
    return [ ["Id", "Table", "Active"], ids, tabls, activs ]


@app.route('/')
@login_required
def index():
    refresh_table_image()
    data = get_dashboard_table_data()
    return render_template('portal.html', table_data=data)


@app.route('/analytics')
@login_required
def analytics():
    if current_user.id == "admin":
        return render_template('analytics.html')
    else:
        flash("You are not authorized!")
        return redirect(url_for('index', not_admin_analytics=True))


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/settings')
@login_required
def settings():
    if current_user.id == "admin":
        data = get_settings_table_data()
        return render_template('settings.html', table_data=data)
    else:
        flash("You are not authorized!")
        return redirect(url_for('index', not_admin_settings=True))


@app.route('/login/check', methods=['post'])
def login_check():
    user = User.get(request.form['username'])
    print user
    if (user and user.password == request.form['password']):
        login_user(user)
    else:
        flash('Username or password incorrect')

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/settings/add_user', methods=['post'])
def add_user():
    add_user_to_config(request.form['username'],
                       request.form['password'],
                       'users.config')
    return render_template('settings.html', added_user=True)


@app.route('/settings/export_data', methods=['post'])
def export_data():
    csv = """"some_data_here"""
    response = make_response(csv)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; \
    filename=bleepr_data.csv"
    return response

if __name__ == '__main__':
    app.run(debug = True, host="127.0.0.1", port=9991)
