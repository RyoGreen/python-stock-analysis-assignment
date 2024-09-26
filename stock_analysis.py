import csv

# csv cell number
CLOSE_CELL_NUM = 4
BUY_SIGNAL_CELL_NUM = 5
SELL_SIGNAL_CELL_NUM = 6

SIGNAL_NUM = "1"


def calculate_trade_percentages(file_name):
    with open(file_name, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        # Skip the first row
        next(reader)
        buy_signal_price = None
        trade_percentages = []
        # Loop through each row
        for row in reader:
            # If BUY signal is present, store the close price
            if row[BUY_SIGNAL_CELL_NUM] == SIGNAL_NUM:
                buy_signal_price = float(row[CLOSE_CELL_NUM])
            # If SELL signal is present, calculate percentage using buy and sell prices
            if row[SELL_SIGNAL_CELL_NUM] == SIGNAL_NUM and buy_signal_price is not None:
                sell_signal_price = float(row[CLOSE_CELL_NUM])
                trade_percentages.append(calculate_percentage_change(
                    buy_signal_price, sell_signal_price))
                # Reset buy signal price
                buy_signal_price = None
    return trade_percentages


# Bonus question
INIT_HALF_PRICE = 0.0
PROFIT_PERCENTAGE = 3.0


def calculate_half_sell_percentages(file_name):
    with open(file_name, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        # Skip the first row
        next(reader)
        buy_signal_price = None
        interim_sell_price = INIT_HALF_PRICE
        trade_percentages = []
        # Loop through each row
        for row in reader:
            # If a BUY signal is present, check for profit greater than 3%
            price = float(row[CLOSE_CELL_NUM])
            if buy_signal_price is not None:
                # If profit is greater than 3%, store the price for half-sell
                if calculate_percentage_change(buy_signal_price, price) > PROFIT_PERCENTAGE and price > interim_sell_price:
                    interim_sell_price = price
            # If BUY signal is present, store the close price
            if row[BUY_SIGNAL_CELL_NUM] == SIGNAL_NUM:
                buy_signal_price = float(row[CLOSE_CELL_NUM])
            # If SELL signal is present, calculate the percentage
            if row[SELL_SIGNAL_CELL_NUM] == SIGNAL_NUM and buy_signal_price is not None:
                sell_signal_price = float(row[CLOSE_CELL_NUM])
                # If profit is more than 3%, calculate with half-sell price
                if interim_sell_price != INIT_HALF_PRICE:
                    sell_signal_price = (
                        sell_signal_price + interim_sell_price) / 2

                trade_percentages.append(calculate_percentage_change(
                    buy_signal_price, sell_signal_price))

                # Reset values
                buy_signal_price = None
                interim_sell_price = INIT_HALF_PRICE
    return trade_percentages


def calculate_percentage_change(buy_signal_price, sell_signal_price):
    return round((sell_signal_price - buy_signal_price) / buy_signal_price * 100, 2)


if __name__ == "__main__":
    print("SPY percentage: ")
    print(calculate_trade_percentages("spy_data.csv"))

    print("DIA percentage: ")
    print(calculate_trade_percentages("dia_data.csv"))

    print("(Bonus) SPY percentage: ")
    print(calculate_half_sell_percentages("spy_data.csv"))
