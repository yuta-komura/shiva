import statistics
import time

import matplotlib.pyplot as plt

from lib import math, repository

tests = ["", 2]
while True:
    for t in tests:
        print("-------------------------------------------------")
        title = "forwardtest_entry{t}".format(t=t)
        print(title)
        print("-------------------------------------------------")

        asset = 1000000

        sql = """
                select
                    *
                from
                    forwardtest_entry{t}
                order by
                    date
                """.format(t=t)

        fe = repository.read_sql(database="tradingbot", sql=sql)
        if fe.empty:
            print("empty")
            time.sleep(10)
            continue

        start_time = fe.loc[0]["date"]
        finish_time = fe.loc[len(fe) - 1]["date"]

        profits = []
        elapsed_secs = []
        for i in range(len(fe)):
            if i == 0:
                continue

            entry_position = fe.iloc[i - 1]
            close_position = fe.iloc[i]

            if entry_position["side"] == "BUY" and (
                    close_position["side"] == "SELL" or close_position["side"] == "CLOSE"):

                amount = asset / entry_position["price"]
                profit = (amount * close_position["price"]) - asset

                elapsed_sec = (
                    close_position["date"] -
                    entry_position["date"]).seconds
                elapsed_secs.append(elapsed_sec)

                profits.append(profit)
                asset += profit

            if entry_position["side"] == "SELL" and (
                    close_position["side"] == "BUY" or close_position["side"] == "CLOSE"):

                amount = asset / entry_position["price"]
                profit = asset - (amount * close_position["price"])

                elapsed_sec = (
                    close_position["date"] -
                    entry_position["date"]).seconds
                elapsed_secs.append(elapsed_sec)

                profits.append(profit)
                asset += profit

        wins = []
        loses = []
        for i in range(len(profits)):
            if profits[i] > 0:
                wins.append(profits[i])
            elif profits[i] < 0:
                loses.append(profits[i])

        pf = None
        if sum(loses) != 0:
            pf = abs(sum(wins) / sum(loses))
        wp = None
        if len(wins) + len(loses) != 0:
            wp = len(wins) / (len(wins) + len(loses)) * 100

        print(str(start_time).split(".")[0],
              "〜", str(finish_time).split(".")[0])
        print("profit", int(sum(profits)))
        if pf:
            print("pf", math.round_down(pf, -2))
        if wp:
            print("wp", math.round_down(wp, 0), "%")
        if elapsed_secs:
            median_elapsed_sec = statistics.median(elapsed_secs)
            print("median elapsed_sec", math.round_down(median_elapsed_sec, 0))

        print("trading cnt", len(profits))

    time.sleep(10)

# ps = []
# p = 0
# for i in range(len(profits)):
#     ps.append(p)
#     p += profits[i]

# fig = plt.figure(figsize=(48, 24), dpi=50)
# ax1 = fig.add_subplot(1, 1, 1)
# ax1.plot(list(range(len(ps))), ps)
# plt.show()


# ###########################################################
# first_data = fe.iloc[0]
# first_date = first_data["date"]
# last_data = fe.iloc[len(fe) - 1]
# last_date = last_data["date"]

# sql = """
#         select
#             *
#         from
#             bitflyer_btc_ohlc_1M
#         where
#             Date >= '{first_date}'
#             and Date <= '{last_date}'
#         order by
#             Date
#         """.format(first_date=first_date, last_date=last_date)
# bo = repository.read_sql(database="tradingbot", sql=sql)

# buy_data = \
#     bo[bo["Date"].isin(fe[fe["side"] == "BUY"]["date"])].reset_index()
# sell_data = \
#     bo[bo["Date"].isin(fe[fe["side"] == "SELL"]["date"])].reset_index()
# close_data = \
#     bo[bo["Date"].isin(fe[fe["side"] == "CLOSE"]["date"])].reset_index()

# buy_points = buy_data["index"]
# sell_points = sell_data["index"]
# close_points = close_data["index"]

# Date_list = list(bo["Date"])
# Price_list = list(bo["Close"])

# fig = plt.figure(figsize=(48, 24), dpi=50)
# ax1 = fig.add_subplot(1, 1, 1)

# ax1.plot(
#     Date_list,
#     Price_list,
#     color="black",
#     linewidth="1")
# ax1.plot(
#     Date_list,
#     Price_list,
#     marker="^",
#     alpha=0.7,
#     color="black",
#     ms=15,
#     linestyle='None',
#     markeredgecolor="blue",
#     markerfacecolor="blue",
#     markevery=buy_points)
# ax1.plot(
#     Date_list,
#     Price_list,
#     marker="v",
#     alpha=0.7,
#     color="black",
#     ms=15,
#     linestyle='None',
#     markeredgecolor="red",
#     markerfacecolor="red",
#     markevery=sell_points)
# ax1.plot(
#     Date_list,
#     Price_list,
#     marker="D",
#     alpha=0.7,
#     color="black",
#     ms=15,
#     linestyle='None',
#     markeredgecolor="gold",
#     markerfacecolor="gold",
#     markevery=close_points)

# plt.show()
