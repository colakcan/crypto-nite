import gdax
class gdax_data_parser():

    def __init__(self):
        self.client = gdax.PublicClient()

    def data_cleanup(self, orderBook):
        trackingList = []
        for order in orderBook:
            processed = []

            avg_price = round((order[4]+order[3])/2,2)
            percent_change = round(100*((order[4]-order[3])/order[3]),2)

            processed.append(order[0])
            processed.append(avg_price)
            processed.append(percent_change)
            processed.append(round(order[5],2))

            trackingList.append(processed)

        return trackingList

    def get_history(self):
        print("Getting historic data")
        historic_data = self.client.get_product_historic_rates('LTC-USD', granularity=60)
        print("Cleaning up")
        return self.data_cleanup(historic_data)



parser = gdax_data_parser()
print(parser.get_history())