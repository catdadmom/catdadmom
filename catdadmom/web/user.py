""":mod:`catdadmom.web.user` --- User pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import bcrypt
from flask import (Blueprint, abort, flash, redirect, g, render_template,
                   request, url_for, session as secure_cookie)
from werkzeug.local import LocalProxy
from sqlalchemy.exc import IntegrityError

from ..db import session
from .models.user import User
from .models.location import Location
from .models.animal import Animal
from .models.picture import Picture
from .models.animallocation import AnimalLocation


bp = Blueprint('user', __name__)


def get_current_user():
    """Gets the currently signed in user."""
    try:
        login = secure_cookie['login']
    except KeyError:
        user = None
    else:
        user = session.query(User).filter_by(login=login).first()
    g.current_user = user
    return user


def set_current_user(user):
    """Sets the currently signed in user."""
    if not user:
        del secure_cookie['login']
    else:
        secure_cookie['login'] = user.login
    g.current_user = user


#: (:class:`~werkzeug.local.LocalProxy` of :class:`~catdadmom.models.user.User`)
#: The currently signed in user.
current_user = LocalProxy(get_current_user)


@bp.app_context_processor
def inject_current_user():
    """Injects :data:`current_user` to templates."""
    return {'current_user': current_user}


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/', methods=['POST'])
def signup():
    """Signs up the user."""
    if current_user:
        abort(403)
    user = User(login=request.form['login'], email=request.form['email'],
                password_hash=bcrypt.hashpw(
                    request.form['password'].encode('utf-8'),
                    bcrypt.gensalt()))
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        flash('User already exists')
        return redirect(url_for('user.signup_form'))
    else:
        set_current_user(user)
        return redirect(url_for('user.home'))


@bp.route('/signup/')
def signup_form():
    """Sign up form."""
    if current_user:
        abort(403)
    return render_template('signup.html')


@bp.route('/login/')
def login_form():
    """Login form."""
    if current_user:
        abort(403)
    return render_template('login.html')


@bp.route('/login/', methods=['POST'])
def login():
    """Logs in the user."""
    if current_user:
        abort(403)
    query = session.query(User).filter((User.login == request.form['login']) |
                                       (User.email == request.form['login']))
    user = query.first()
    if not user:
        flash('No such user.')
        return redirect(url_for('user.login_form'))
    password_hash = bcrypt.hashpw(request.form['password'].encode('utf-8'),
                                  user.password_hash.encode('utf-8'))
    if password_hash != user.password_hash:
        flash('Incorrect password.')
        return redirect(url_for('user.login_form'))
    else:
        set_current_user(user)
        return redirect(url_for('user.home'))


@bp.route('/logout/')
def logout():
    set_current_user(None)
    return redirect(url_for('user.home'))
