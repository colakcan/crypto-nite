import gdax


def track_orders(orderBook):
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


client = gdax.PublicClient()
orderz = client.get_product_historic_rates('LTC-USD', granularity=60)
cleanOrderz = track_orders(orderz)