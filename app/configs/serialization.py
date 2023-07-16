from marshmallow import Schema, fields


class CreateConfigsSchema(Schema):
    context = fields.String(required=True)
    exchange_1 = fields.String(required=True)
    exchange_2 = fields.String(required=True)
    coin = fields.String(missing='manual')
    bots_quantity = fields.Integer()
    target_profit = fields.Float()
    shift_use_flag = fields.Integer()
    orders_delay = fields.Float()
    max_order_usd = fields.Integer()
    max_leverage = fields.Float()
    pause_flag = fields.Integer()
    api_secret_encrypted = fields.String()
