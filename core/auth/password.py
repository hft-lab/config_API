from argon2 import PasswordHasher, exceptions

from app.core.exceptions import AuthorizationError


class UserPassword:

    @classmethod
    def password_hash(cls, password):
        return PasswordHasher().hash(password=password)

    @classmethod
    def verify(cls, password_hash, password):
        try:
            return PasswordHasher().verify(hash=password_hash, password=password)
        except exceptions.VerifyMismatchError:
            raise AuthorizationError(messages={'message': 'Wrong credentials'})
