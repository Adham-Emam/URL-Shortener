from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from config import Config
from form import LoginForm, RegistrationForm, URLForm
from models import db,  bcrypt, User, Url
from dotenv import load_dotenv
import random
import string
import re

app = Flask(__name__)
app.config.from_object(Config)

load_dotenv()

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


FIRST_REQUEST = True


@app.before_request
def create_tables():
    global FIRST_REQUEST
    if FIRST_REQUEST:
        db.create_all()
        FIRST_REQUEST = False


BASE62 = string.ascii_letters + string.digits


def generate_base62_id(length=8):
    return ''.join(random.choices(BASE62, k=length))


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = URLForm()
    current_url = request.url

    if form.validate_on_submit():
        url = form.url.data
        shorten_url = generate_base62_id(10)
        new_url = Url(url=url, shorten_url=shorten_url,
                      user_id=current_user.id)
        db.session.add(new_url)
        db.session.commit()
        return redirect(url_for('index'))

    urls = Url.query.filter_by(user_id=current_user.id).all()

    for url in urls:
        url.url = re.search(
            r'^https?://(?:www\.)?([^/.]+)', url.url).group(1).capitalize()

        url.shorten_url = current_url + url.shorten_url

    return render_template('index.html', form=form, urls=urls)


@app.route('/<string:encode>')
def shorten_link(encode):
    shorten_url_entry = Url.query.filter_by(
        user_id=current_user.id, shorten_url=encode).first_or_404()

    return redirect(shorten_url_entry.url)


@app.route('/delete_url/<int:url_id>')
def delete_url(url_id):
    url = Url.query.get_or_404(url_id)
    db.session.delete(url)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login_form.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('login_form.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
