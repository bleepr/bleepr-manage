from flask import Flask, flash, redirect, url_for, request
from flask import get_flashed_messages, render_template
from flask.ext.login import LoginManager, UserMixin
from flask.ext.login import current_user, login_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'some_secret_key_wink_wink'

login_manager = LoginManager()
login_manager.init_app(app)


class UserNotFoundError(Exception):
    pass


class User(UserMixin):
    '''Simple User class'''
    USERS = {
        # username: password
        'john@ed': 'lol',
        'mary': 'love peter',
        'edran' : 'edran'
    }

    def __init__(self, id):
        if not id in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]

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


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('portal.html')
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


@app.route('/login/check', methods=['post'])
def login_check():
    # validate username and password
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


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port=9991)
