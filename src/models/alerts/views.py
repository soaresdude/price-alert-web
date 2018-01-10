from flask import Blueprint

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/new', methods=['POST'])
def create_alert():
    pass

@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id):
    pass

@alert_blueprint.route('/alert/<string:alert_id>')
def get_alert_page(alert_id):
    pass

@alert_blueprint.route('/user_alert/<string:user_id>')
def get_user_alert(user_id):
    pass