import time
import uuid
from datetime import datetime

from marshmallow import ValidationError

from app.configs.quires import get_last_launch, insert
from app.configs.serialization import CreateConfigsSchema
from config import Config
from core.bases.handler import BaseHandler


class CreateConfigsHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.launchers = []
        self.must_be_any_field = ['bots_quantity', 'target_profit',
                                  'shift_use_flag', 'orders_delay', 'max_order_usd',
                                  'max_leverage', 'pause_flag']

    def __prepare_payload(self, payload: dict) -> dict:
        payload['ts'] = int(time.time() * 1000)
        payload['id'] = uuid.uuid4()
        payload['datetime'] = datetime.utcnow()
        payload['api_secret_encrypted'] = self.request.headers.get('token', None)
        payload['bots_quantity'] = len(self.launchers)

        return payload

    async def __prepare_data(self, conn, exchange_1, exchange_2, coin, payload) -> None:
        data = {
            'exchange_1': exchange_1,
            'exchange_2': exchange_2,
            'coin': coin,
            'id': uuid.uuid4(),
            'ts': int(time.time() * 1000),
            'datetime': datetime.utcnow(),
            'updated_flag': 0,
            'bot_config_id': payload['id'],

        }
        no_need_update = ['context', 'api_secret_encrypted', 'bots_quantity']
        data.update({k: v for k, v in payload.items() if k not in data and k not in no_need_update})

        if last_launch_data := await get_last_launch(conn, exchange_1, exchange_2, coin):
            no_need_update = ['fee_exchange_1', 'fee_exchange_2', 'shift']
            last_launch_data = dict(last_launch_data)
            data.update({k: v for k, v in last_launch_data.items() if k not in data and k not in no_need_update and v is not None})

        self.launchers.append(data)

    async def __prepare_all_all(self, conn, payload: dict) -> None:
        already = []
        is_break = False
        for exchange_1 in Config.EXCHANGES:
            for exchange_2 in Config.EXCHANGES:
                for coin in Config.COINS:
                    if exchange_1 != exchange_2:
                        config, config_r = [exchange_1, exchange_2, coin], [exchange_2, exchange_1, coin]

                        if config not in already and config_r not in already:
                            already.append(config)
                            already.append(config_r)

                            if payload['coin'] != 'ALL':
                                coin = payload['coin']
                                is_break = True

                            await self.__prepare_data(conn, exchange_1, exchange_2, coin, payload)

                            if is_break:
                                break

    async def __prepare_exchange_all(self, conn, payload: dict) -> None:
        already = []
        is_break = False
        for exchange_2 in Config.EXCHANGES:
            for coin in Config.COINS:
                if payload['exchange_1'] != exchange_2:
                    config = [payload['exchange_1'], exchange_2, coin]
                    config_r = [exchange_2, payload['exchange_1'], coin]

                    if config not in already and config_r not in already:
                        already.append(config)
                        already.append(config_r)

                        if payload['coin'] != 'ALL':
                            coin = payload['coin']
                            is_break = True

                        await self.__prepare_data(conn, payload['exchange_1'], exchange_2, coin, payload)

                        if is_break:
                            break

    async def __prepare_all_exchange(self, conn, payload: dict) -> None:
        already = []
        is_break = False
        for exchange_1 in Config.EXCHANGES:
            for coin in Config.COINS:
                if payload['exchange_2'] != exchange_1:
                    config = [payload['exchange_2'], exchange_1, coin],
                    config_r = [exchange_1, payload['exchange_2'], coin]

                    if config not in already and config_r not in already:
                        already.append(config)
                        already.append(config_r)

                        if payload['coin'] != 'ALL':
                            coin = payload['coin']
                            is_break = True

                        await self.__prepare_data(conn, exchange_1, payload['exchange_2'], coin, payload)

                        if is_break:
                            break

    async def __prepare_exchange_exchange(self, conn, payload: dict) -> None:
        is_break = False
        for coin in Config.COINS:
            if payload['coin'] != 'ALL':
                coin = payload['coin']
                is_break = True

            await self.__prepare_data(conn, payload['exchange_1'], payload['exchange_2'], coin, payload)

            if is_break:
                break

    async def __prepare_launchers(self, conn, payload: dict) -> None:
        if payload['exchange_1'].upper() == 'ALL' and payload['exchange_2'].upper() == 'ALL':
            await self.__prepare_all_all(conn, payload)
        elif payload['exchange_1'].upper() != 'ALL' and payload['exchange_2'].upper() == 'ALL':
            await self.__prepare_exchange_all(conn, payload)
        elif payload['exchange_1'].upper() == 'ALL' and payload['exchange_2'].upper() != 'ALL':
            await self.__prepare_all_exchange(conn, payload)
        elif payload['exchange_1'].upper() != 'ALL' and payload['exchange_2'].upper() != 'ALL':
            await self.__prepare_exchange_exchange(conn, payload)

    async def handle(self):
        payload = self.__prepare_payload(self.parse(schema=CreateConfigsSchema, data=await self.request.json()))

        if any([payload.get(k, False) for k in self.must_be_any_field]):
            async with self.db_engine.acquire() as conn:
                await  self.__prepare_launchers(conn, payload)

                for data in self.launchers:
                    await insert(conn, 'bot_launches', data)

                await insert(conn, 'bot_config', payload)

            return {'code': 20, 'message': 'Config and launchers created.'}

        else:
            raise ValidationError(message='Not valid all fields')
