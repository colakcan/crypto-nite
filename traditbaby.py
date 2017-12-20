import gdax
import datetime

class gdax_data_parser():

    def __init__(self):
        self.client = gdax.PublicClient()
        self.historic_data = []

    def raw_data_parse(self, raw_data):
        previous_change = 1
        for order in raw_data:
            data = dict()
            data["raw"] = order

            processed = []
            time = self.human_time(order[0])
            avg_price = (order[4]+order[3])/2
            percent_change = 1+((order[4]-order[3])/order[3])
            change_of_change = percent_change * previous_change
            previous_change = percent_change

            processed.append(time)
            processed.append(avg_price)
            processed.append(percent_change)
            processed.append(change_of_change)
            processed.append(order[5])
            data["processed"] = processed

            self.historic_data.append(data)
            total_data = len(self.historic_data)
        print("Added "+str(total_data)+" list entries!")

    def get_history(self, granularity = 60):
        print("Getting historic data")
        raw_data = self.client.get_product_historic_rates('LTC-USD', granularity=granularity)
        print("Got Raw Data")
        self.raw_data_parse(raw_data)
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


parser = gdax_data_parser()
parser.get_history()
parser.print_processed_data()
