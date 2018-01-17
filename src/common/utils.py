import re
from passlib.handlers.pbkdf2 import pbkdf2_sha512


class Utils(object):

    @staticmethod
    def validate_email(email):
        email_matched = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_matched.match(email) else False

    @staticmethod
    def encrypt_password(password):
        """
        It receives the password from the form-size and encrypts it with pbkdf2
        :param password: sha512 password from the site
        :return: A sha512 pbkdf2 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks the password sent by user is equal the encrypted on the database
        :param password: sha512 password
        :param hashed_password: pbkdf2 sha512 password
        :return: True if it matches False if else
        """
        return pbkdf2_sha512.verify(password, hashed_password)