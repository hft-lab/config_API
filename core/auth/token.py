import hashlib

from config import Config


class UserToken:

    @staticmethod
    def encode_values(token) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(token.encode('utf-8'))
        return sha256_hash.hexdigest()


    def check_token(self, token: str) -> bool:
        return self.encode_values(token) in [self.encode_values(x) for x in Config.USERS_TOKENS.values()]
