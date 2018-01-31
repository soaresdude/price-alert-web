import uuid
from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "tag_name": self.tag_name,
            "url_prefix": self.url_prefix,
            "query": self.query
        }

    @classmethod
    def get_store(cls, store_id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, query={"_id": store_id}))

    def save_to_mongo(self):
        Database.insert(StoreConstants.COLLECTION, data=self.json())

    @classmethod
    def search_store_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, query={"name": store_name}))

    @classmethod
    def search_store_by_prefix(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION,
                                       query={"url_prefix": {
                                           "$regex": "^{}".format(url_prefix)}}))  # regexp for the store prefix

    # TODO Deprecated method. Use search_store instead
    @classmethod
    def search_store_by_url(cls, store_url):
        for char in range(0, len(store_url) + 1):
            try:
                return cls(**Database.find_one(StoreConstants.COLLECTION,
                                               query={"url_prefix": {
                                                   "$regex": '^{}'.format(store_url)}}))  # regexp for the store prefix
            except:
                raise StoreErrors.StoreNotFound("Store not found!")  # all methods in python return None by default

    @classmethod
    def search_store(cls, store_id=None, store_name=None, url_prefix=None, store_url=None):
        if store_url:
            for char in range(0, len(store_url) + 1):
                try:
                    store = cls.search_store_by_prefix(store_url[:char])
                    return store
                except:
                    raise StoreErrors.StoreNotFound("Store not found!") # all methods in python return None by default
        elif store_id:
            return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": store_id}))
        elif store_name:
            cls.find_one_store(query_name='name', query=store_name)
        elif url_prefix:
            cls.find_one_store(query_name='url_prefix', query="{'$regex': '^{}'.format(url_prefix)}")
        else:
            raise StoreErrors.StoreNotFound("Wrong parameters!")

    @classmethod
    def find_one_store(cls, query_name, query):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"{}".format(query_name): query}))