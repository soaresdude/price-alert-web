import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def validate_login(email, password):
        """
        Validates the login with email and password
        Check if the email's is on the db and if it's associated with that password
        :param email: The string of user email
        :param password: sha512 password hash
        :return: True if it matched or False if else
        """
        user_data = Database.find_one(collection='users', query={"email": email})
        if user_data is None:
            raise UserErrors.UserNotFoundException("User not found!")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.WrongPassword("Wrong password!")

        return True


    @staticmethod
    def register_user(email, password):
        """
        Will register the user with email and password (hashed with sha_512)
        :param email: user's email (can be invalid)
        :param password: sha_512 hashed password
        :return: True if the user has been registered, False if not (exceptions can be used)
        """
        user_data = Database.find_one(collection='users', query={"email": email})

        if user_data is not None:
            # If user_date is not None, the query has returned a filled object, so the user is already registered
            raise UserErrors.UserRegistered("User already registered.")
        if not Utils.validate_email(email):
            # Tell the user if the his email is valid or not
            raise UserErrors.InvalidEmail("Invalid email, try again.")

        User(email=email, password=Utils.encrypt_password(password)).save_to_mongo()

    def save_to_mongo(self):
        Database.insert(UserConstants.COLLECTION, data=self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }