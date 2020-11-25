import datetime

from binance.client import Client
from binance.websockets import BinanceSocketManager

from lib import repository


def process_message(msg):
    date = datetime.datetime.now()
    price = msg["p"]
    size = msg["q"]
    sql = \
        "insert into execution_history_binance values (null,'{date}','{price}','{size}')"\
        .format(date=date, price=price, size=size)
    repository.execute(database=database, sql=sql, log=False)


if __name__ == '__main__':
    database = "tradingbot"

    sql = "truncate execution_history_binance"
    repository.execute(database=database, sql=sql, log=False)

    api_key = "73okG5NvWTRxyxO8C8EEAs1oQe6kKLXuqtSyy4CFFchZXUaD1x3JKqAFeNoQLIGr"
    api_secret = "kMGWhaOChKDLYb28bEPrLMveuJSXeXqdL1WhzvaGrkzBTjaTOkPTanhkujBCybBv"
    client = Client(api_key, api_secret)

    bm = BinanceSocketManager(client)
    bm.start_aggtrade_socket('BTCUSDT', process_message)
    bm.start()
