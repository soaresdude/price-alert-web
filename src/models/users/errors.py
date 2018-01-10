

class UserError(Exception):
    def __init__(self, message):
        self.message = message

class UserNotFoundException(UserError):
    pass


class WrongPassword(UserError):
    pass


class UserRegistered(UserError):
    pass


class InvalidEmail(UserError):
    pass