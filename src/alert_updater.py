from src.common.database import Database
from src.models.alerts.alert import Alert

Database.initialize()

alerts_needing_update = Alert.update_check_alert()

for alert in alerts_needing_update:
    alert.load_item_price()
    alert.send_alert()