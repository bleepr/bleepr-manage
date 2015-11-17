import csv
from flask import Flask, flash, redirect, url_for, request
from flask import get_flashed_messages, render_template, make_response
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import current_user, login_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'some_secret_key_wink_wink'

login_manager = LoginManager()
login_manager.init_app(app)


class UserNotFoundError(Exception):
    pass


class User(UserMixin):
    def __init__(self, id):
        self.USERS = self.load_users_from_file("users.config")
        if not id in self.USERS:
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

def get_table_data():
    return [ ["id", "Table", "Active", "Occupied", "Remaining time"],
             ["0", "1", "2"], # id
             ["red", "yellow", "green"], # table
             ["Yes", "Yes", "No"], # Active
             ["No", "Yes", "N/A"], # Occupied
             ["34", "92", "N/A"] ] # Remaining time

@app.route('/')
def index():
    if current_user.is_authenticated:
        data = get_table_data()
        return render_template('portal.html', table_data=data)
    else:
        return render_template('signin.html')


@app.route('/login')
def login():
    return '''
        <form action="/login/check" method="post">
            <p>Username: <input name="username" type="text"></p>
            <p>Password: <input name="password" type="password"></p>
            <input type="submit">
        </form>
    '''

@app.route('/settings')
def settings():
    if current_user.id == "admin":
        return render_template('settings.html')
    else:
        flash("You are not authorized!")
        return redirect(url_for('index', not_admin_setting=True))


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
    app.run(debug = True, host="0.0.0.0", port=9991)
