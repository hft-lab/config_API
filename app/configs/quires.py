async def insert(conn, table_name, payload: dict):
    columns = ''
    values = ''

    for k, v in payload.items():
        columns += str(k) + ', '

        if isinstance(v, int):
            values += str(v) + ", "
        elif isinstance(v, float):
            values += str(v) + ", "
        else:
            values += "'" + str(v) + "', "

    sql = f"""
        insert into 
            {table_name}({columns[:-2]})
        values 
            ({values[:-2]})
    """

    await conn.execute(sql)


async def insert_many_launches(conn, payload):
    columns = ''
    values = ''

    for k, v in payload.items():
        columns += str(k) + ', '

        if isinstance(v, int):
            values += str(v) + ", "
        elif isinstance(v, float):
            values += str(v) + ", "
        else:
            values += "'" + str(v) + "', "

    sql = f"""
            insert into 
                bot_launches({columns[:-2]})
            values 
                {values[:-2]}
        """

    await conn.execute(sql)

async def get_last_launch(conn, exchange_1, exchange_2, coin) -> dict:
    sql = f"""
    select 
        *
    from 
        bot_launches
    where 
        exchange_1 in ('{exchange_1}', '{exchange_2}') and 
        exchange_2 in ('{exchange_1}', '{exchange_2}') and
        coin = '{coin}'
    order by 
    	datetime desc
    limit 
    	1
    """
    return await conn.fetchrow(sql)
