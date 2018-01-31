from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.validate_login(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))  # werkzeug redirect

        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.jinja2")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))  # werkzeug redirect

        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.jinja2")

@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.search_email(session['email'])
    alerts = user.get_user_alerts()
    render_template("users/alerts.jinja2", alerts=alerts)

@user_blueprint.route('/logout') # doesn't need @user_decorators.requires_login because this option is only available when logged in
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass