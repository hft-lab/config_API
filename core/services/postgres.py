from asyncpg import create_pool
from config import Config


async def setup_postgres(app):
    app['db'] = await create_pool(**Config.POSTGRES)
    print("Backend has initialized postgres connection's pool")


async def clean_postgres(app):
    await app['db'].close()
