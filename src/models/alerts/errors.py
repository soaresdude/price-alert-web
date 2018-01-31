

class AlertErrors(Exception):
    def __init__(self, message):
        self.message = message


class AlertNotFound(AlertErrors):
    pass