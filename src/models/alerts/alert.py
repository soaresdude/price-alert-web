import uuid
import datetime
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, last_checked=None,_id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_item(item_id)
        self._id = uuid.uuid4().hex if _id is None else _id
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked



    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)


    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price of {} is reached".format(self.item.name),
                "text": "Deal desired was found here: {}".format(self.item.price)
            }
        )


    @classmethod
    def update_check_alert(cls, alert_timeout=AlertConstants.ALERT_TIMEOUT):
        last_update = datetime.datetime.utcnow() - datetime.timedelta(minutes=alert_timeout)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked": {"$lte": last_update}})] # Less Than or Equal to


    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, query={"_id": self._id}, data=self.json())


    def json(self):
        return {
            "_id": self._id,
            "last_checked": self.last_checked,
            "price_limit": self.price_limit,
            "user_email": self.user_email,
            "item_id": self.item._id
        }


    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.save_to_mongo()
        return self.item.pricer


    def send_alert(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def search_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, query={'user_email': user_email})]