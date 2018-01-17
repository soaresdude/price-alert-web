from flask import Flask, render_template
from src.common.database import Database

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "123"

@app.before_first_request
def init_database():
    Database.initialize()

@app.route('/')
def home():
    return render_template('home.jinja2')

from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")

from src.models.alerts.views import alert_blueprint
app.register_blueprint(alert_blueprint, url_prefix="/alerts")

from src.models.stores.views import store_blueprint
app.register_blueprint(store_blueprint, url_prefix="/stores")

