import gdax
import datetime


class gdax_data_parser():
    def __init__(self):
        self.client = gdax.PublicClient()
        self.historic_data = []

    def raw_data_parse(self, raw_data):
        for order in raw_data:
            data = dict()
            data["raw"] = order

            processed = []
            time = self.human_time(order[0])
            avg_price = (order[4] + order[3]) / 2
            percent_change = 1 + ((order[4] - order[3]) / order[3])

            processed.append(time)
            processed.append(avg_price)
            processed.append(percent_change)
            processed.append(order[5])
            data["processed"] = processed

            self.historic_data.append(data)
            total_data = len(self.historic_data)
        print("Added " + str(total_data) + " list entries!")

    def get_history(self, granularity=60):
        print("Getting historic data")
        raw_data = self.client.get_product_historic_rates('LTC-USD', granularity=granularity)
        print("Got Raw Data")
        self.raw_data_parse(reversed(raw_data))
        print("Cleaning up")
        return self.historic_data

    def human_time(self, epoch):
        return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')

    def print_processed_data(self):
        for i in self.historic_data:
            print(i["processed"])

    def print_raw_data(self):
        for i in self.historic_data:
            print(i["raw"])


class algorithms():
    def __init__(self, parsed_data, algorithm_name="basic_acceleration"):
        self.algorithm = algorithm_name
        self.data = parsed_data

    def run(self):
        if self.algorithm is "basic_acceleration":
            self.basic_acceleration()
        else:
            print("No algorithm selected. Valid options are: basic_acceleration")

    def basic_acceleration(self):
        self.basic_acceleration_data_analysis()
        previous_acceleration = self.past_acceleration_percentage[2]
        starting_cash = 500
        coin_buy_price = self.past_prices[2]
        coin_worth = starting_cash / coin_buy_price
        cash_worth = starting_cash
        coin_owned = True
        transaction_count = 0
        for index in range(3, len(self.data)):
            print(self.data[index]["processed"])
            # print(self.past_prices[index])
            # print(self.past_velocity[index])
            # print(self.past_acceleration[index])
            print(self.past_acceleration_percentage[index])

            if coin_owned is False \
                    and self.past_acceleration_percentage[index - 1] < 0 and self.past_acceleration_percentage[index] > 0:

                print("Buy! Because past acceleration: " + str(
                    self.past_acceleration_percentage[index - 1]) + " current acceleration: " + str(
                    self.past_acceleration_percentage[index]))
                print("Had cash amount: " + str(cash_worth))
                coin_worth = cash_worth / self.past_prices[index]
                coin_buy_price = self.past_prices[index]
                print("Bought coin amount: " + str(coin_worth))
                coin_owned = True
                transaction_count += 1
            elif coin_owned is True and coin_buy_price < self.past_prices[index] \
                    and self.past_acceleration_percentage[index - 1] > 0 and self.past_acceleration_percentage[index] < 0:

                print("Sell! Because bought at "+str(coin_buy_price)+" past acceleration: " + str(
                    self.past_acceleration_percentage[index - 1]) + " current acceleration: " + str(
                    self.past_acceleration_percentage[index]))

                print("Had coin amount: " + str(coin_worth))
                cash_worth = coin_worth * self.past_prices[index]
                print("Received cash amount: " + str(cash_worth))
                coin_owned = False
                transaction_count += 1
            print("Start date: "+str(self.data[2]["processed"][0])+" End date: "+str(self.data[-1]["processed"][0]))
            print("Starting cash: "+str(starting_cash)+" Final cash: " + str(cash_worth))
            print("Transaction count: "+str(transaction_count))

    def basic_acceleration_data_analysis(self):
        self.past_prices = []
        for data in self.data:
            self.past_prices.append(data["processed"][1])
        self.past_velocity = []
        previous_price = self.past_prices[0]
        for price in self.past_prices:
            self.past_velocity.append(price - previous_price)
            previous_price = price
        self.past_acceleration = []
        previous_velocity = self.past_velocity[0]
        for velocity in self.past_velocity:
            self.past_acceleration.append(velocity - previous_velocity)
            previous_velocity = velocity
        self.past_acceleration_percentage = []
        for index in range(len(self.past_acceleration)):
            self.past_acceleration_percentage.append(100 * self.past_acceleration[index] / self.past_prices[index])


parser = gdax_data_parser()
data = parser.get_history(60)
# parser.print_processed_data()

money_maker = algorithms(data)
money_maker.run()
