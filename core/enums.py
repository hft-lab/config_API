from core.bases.enum import BaseEnum


class Coins(BaseEnum):
    ALL = 'ALL'
    ETH = 'ETH'
    BTC = 'BTC'


class Context(BaseEnum):
    MANUAL = 'manual'
    BOT_START = 'bot-start'


class Exchanges(BaseEnum):
    ALL = 'ALL'
    APOLLOX = 'APOLLOX'
    KRAKEN = 'KRAKEN'
    DYDX = 'DYDX'
    BINANCE = 'BINANCE'
