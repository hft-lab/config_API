import hashlib

from config import Config


class UserToken:

    @staticmethod
    def encode_values() -> list:
        result = []
        sha256_hash = hashlib.sha256()
        for token in Config.USERS_TOKENS.values():
            sha256_hash.update(token.encode('utf-8'))
            result.append(sha256_hash.hexdigest())

        return result


    def check_token(self, token: str) -> bool:
        return token in self.encode_values()
