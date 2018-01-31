from functools import wraps
from flask import session, redirect, url_for, request


def requires_login(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return function(*args, **kwargs)
    return decorated_function