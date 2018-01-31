import uuid
import datetime
import requests
import src.models.alerts.constants as AlertConstants
import src.models.alerts.errors as AlertErrors
from src.common.database import Database
from src.models.items.item import Item



class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True,last_checked=None,_id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_item(item_id)
        self._id = uuid.uuid4().hex if _id is None else _id
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self.active = active



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
                                                      {"last_checked": {"$lte": last_update}, "active": True})] # Less Than or Equal to


    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, query={"_id": self._id}, data=self.json())


    def json(self):
        return {
            "_id": self._id,
            "last_checked": self.last_checked,
            "price_limit": self.price_limit,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }


    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price


    def send_alert(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def find_alert(cls, user_email=None, alert_id=None):
        if user_email:
            cls.find_all_alerts(query_name='user_email',query=user_email)
        elif alert_id:
            cls.find_one_alert(query_name='_id',query=alert_id)
        else:
            raise AlertErrors.AlertErrors("Bad parameters, try again!")

    @classmethod
    def find_one_alert(cls, query, query_name):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {'{}'.format(query_name): query}))

    @classmethod
    def find_all_alerts(cls, query, query_name):
        return [cls(**alert) for alert in Database.find(AlertConstants.COLLECTION, {'{}'.format(query_name): query})]


    def deactivate(self):
        self.active = False
        self.save_to_mongo()


    def activate(self):
        self.active = True
        self.save_to_mongo()


    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})