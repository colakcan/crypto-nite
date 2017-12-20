import gdax
class gdax_data_parser():

    def __init__(self):
        self.client = gdax.PublicClient()
        self.historic_data = []

    def raw_data_parse(self, raw_data):
        previous_change = 1
        for order in raw_data:
            processed = []

            avg_price = round((order[4]+order[3])/2,4)
            percent_change = round(1+((order[4]-order[3])/order[3]),4)
            change_of_change = round(percent_change * previous_change, 4)
            previous_change = change_of_change

            processed.append(order[0])
            processed.append(avg_price)
            processed.append(percent_change)
            processed.append(change_of_change)
            processed.append(round(order[5],4))

            self.historic_data.append(processed)
            total_data = len(self.historic_data)
        print("Got "+str(total_data)+" list entries!")

    def get_history(self):
        print("Getting historic data")
        raw_data = self.client.get_product_historic_rates('LTC-USD', granularity=60)
        print("Got Raw Data")
        self.raw_data_parse(raw_data)
        print("Cleaning up")
        return self.historic_data


parser = gdax_data_parser()
for i in parser.get_history():
    print(i)