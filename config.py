import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    API_URL = os.getenv('API_URL')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    EXCHANGES = os.getenv('EXCHANGES').split(',')
    COINS = os.getenv('COINS').split(',')

    POSTGRES = {
        'database': os.getenv('POSTGRES_NAME'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
    }

    USERS_TOKENS = {
        'dmitry_t': os.getenv('DMITRY_T'),
        'nikita_c': os.getenv('NIKITA_C'),
        'ihor_l': os.getenv('IHOR_L'),
        'system': os.getenv('SYSTEM')
    }
