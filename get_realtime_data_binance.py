import datetime

from binance.client import Client
from binance.websockets import BinanceSocketManager

from lib import repository
from lib.config import Binance


def process_message(msg):
    date = datetime.datetime.now()
    price = msg["p"]
    size = msg["q"]
    sql = \
        "insert into execution_history_binance values (null,'{date}','{price}','{size}')"\
        .format(date=date, price=price, size=size)
    repository.execute(database=DATABASE, sql=sql, log=False)


if __name__ == '__main__':
    DATABASE = "tradingbot"

    api_key = Binance.Api.value.KEY.value
    api_secret = Binance.Api.value.SECRET.value
    client = Client(api_key, api_secret)

    bm = BinanceSocketManager(client)
    bm.start_aggtrade_socket('BTCUSDT', process_message)
    bm.start()
