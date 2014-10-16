""":mod:`catdadmom.web.user` --- User pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import time, os, json, base64, hmac, urllib
import bcrypt
from flask import (Blueprint, abort, flash, redirect, g, render_template,
                   request, url_for, Response, session as secure_cookie)
from werkzeug.local import LocalProxy
from sqlalchemy.exc import IntegrityError
from hashlib import sha1

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

@bp.route('/sign_s3/')
def sign_s3():

    if not current_user:
        abort(403)

    # Load necessary information into the application:
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')

    # Collect information on the file from the GET parameters of the request:
    object_name = urllib.quote_plus(request.args.get('s3_object_name'))
    mime_type = request.args.get('s3_object_type')
    ext = mime_type
    ext = ext.replace('image/','')
    object_name = str(time.time()).replace(".", "") + '.' + ext

    # Set the expiry time of the signature (in seconds) and declare the permissions of the file to be uploaded
    expires = int(time.time()+10)
    amz_headers = "x-amz-acl:public-read"

    # Generate the PUT request that JavaScript will use:
    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

    # Generate the signature with which the request can be signed:
    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
    # Remove surrounding whitespace and quote special characters:
    signature = urllib.quote_plus(signature.strip())

    # Build the URL of the file in anticipation of its imminent upload:
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

    content = json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
        'url': url
    })

    # Return the signed request and the anticipated URL back to the browser in JSON format:
    return Response(content, mimetype='text/plain; charset=x-user-defined')


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
        return redirect(url_for('user.home'))
    return render_template('signup.html')


@bp.route('/login/')
def login_form():
    """Login form."""
    if current_user:
        return redirect(url_for('user.home'))
    return render_template('login.html')


@bp.route('/login/', methods=['POST'])
def login():
    """Logs in the user."""
    if current_user:
        return redirect(url_for('user.home'))
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
    return redirect(url_for('user.login'))