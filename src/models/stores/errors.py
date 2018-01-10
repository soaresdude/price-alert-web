

class StoreErrors(Exception):
    def __init__(self, message):
        self.message = message


class StoreNotFound(StoreErrors):
    pass