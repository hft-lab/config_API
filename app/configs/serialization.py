from marshmallow import Schema, fields

from core.enums import Coins, Exchanges


class CreateConfigsSchema(Schema):
    exchange_1 = fields.String(required=True, validate=lambda x: x.upper() in Exchanges.to_list())
    exchange_2 = fields.String(required=True, validate=lambda x: x.upper() in Exchanges.to_list())
    coin = fields.String(required=True, validate=lambda x: x.upper() in Coins.to_list())
    target_profit = fields.Float(validate=lambda x: -0.01 <= x <= 0.01)
    shift_use_flag = fields.Integer(validate=lambda x: x in [0, 1])
    orders_delay = fields.Integer(validate=lambda x: x > 0)
    max_order_usd = fields.Integer(validate=lambda x: x > 0)
    max_leverage = fields.Float(validate=lambda x: 0 < x < 5)
