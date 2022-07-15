# function calculate and aggregrate input to trade stat result
def calculate_trade_stat(data: list[dict], side: str):
    side_data = list(filter(lambda item: item['side'] == side, data))
    result = {
        'time_from': min(data, key=lambda item: item['traded_at'])['traded_at'],
        'time_to': max(data, key=lambda item: item['traded_at'])['traded_at'],
        'symbol': side_data[0]['symbol'],
        'side': side
    }

    sum_price_volume = 0
    total_volume = 0
    for item in side_data:
        sum_price_volume += float(item['price']) * float(item['volume'])
        total_volume += float(item['volume'])

    result['volume'] = total_volume
    result['weight_avg_price'] = sum_price_volume / total_volume
    return result


# function calculate volume imbalance and agrregrate to result
def calculate_volume_imbalance(data: list[dict]):
    buy_volume = 0
    sell_volume = 0

    for item in data:
        if item['side'] == 'buy':
            buy_volume += float(item['volume'])
        else:
            sell_volume += float(item['volume'])

    result = {
        'time_from': min(data, key=lambda item: item['traded_at'])['traded_at'],
        'time_to': max(data, key=lambda item: item['traded_at'])['traded_at'],
        'symbol': data[0]['symbol'],
        'volume_imbalance': buy_volume/(buy_volume + sell_volume) - .5
    }
    return result
