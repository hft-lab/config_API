from enum import Enum


class BaseEnum(Enum):
    """ Base enum class. """

    @classmethod
    def to_list(cls):
        return list(map(lambda c: c.value, cls))
