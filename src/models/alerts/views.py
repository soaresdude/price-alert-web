from flask import Blueprint, render_template, request, session, redirect, url_for
from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/')
def index():
    return "Alert's index"

@alert_blueprint.route('/new', methods=['POST', 'GET'])
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(name, url)
        item.save_to_mongo() # saves before the alert because of the self.item = Item.get_item(item_id), that must have an entry before initialize alert object

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price() # load price already has save_to_mongo

    return render_template('alerts/new_alert.jinja2')


@alert_blueprint.route('/edit/<string:edit_id>', methods=['POST', 'GET'])
@user_decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_one_alert("_id", alert_id)
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])

        alert.price_limit = price_limit
        alert.save_to_mongo()

        return redirect(url_for('users.user_alerts'))
    return render_template('alerts/edit_alert.jinja2', alert_id=alert)


@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_alert(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    Alert.find_alert(alert_id).delete()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_alert(alert_id).activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_alert()
    render_template('alerts/alert.jinja2', alert=alert)


@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.find_alert(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))

