from domain.logic.util.preprocessing import group_list_dict
from domain.logic.util.validation import validate_quote_base
from domain.logic.util.calculation import calculate_trade_stat, calculate_volume_imbalance
from domain.registry import Registry
from .exception.binance_exception import \
    BinanceSymbolNotFound, \
    BinanceSymbolAlreadyExist, \
    BinanceUnprocessableEntity


_BINANCE_STATUS_MODIFIED = 202
_BINANCE_STATUS_OK = 200
_BINANCE_STATUS_ERR_NOTFOUND = 404
_BINANCE_STATUS_ERR_EXIST = 455

_BINANCE_ERR_MSG_ENTITY_UNPROCESSING = "invalid entities"


# subscribe to binance symbol
async def binance_subscribe(symbol_: str):
    resp = await Registry().binance.subscribe(symbol_)

    if resp['status_code'] == _BINANCE_STATUS_ERR_EXIST:
        raise BinanceSymbolAlreadyExist(resp['msg'])


# unsubscribe to binance symbol
async def binance_unsubscribe(symbol_: str):
    resp = await Registry().binance.unsubscribe(symbol_)

    if resp['status_code'] == _BINANCE_STATUS_ERR_NOTFOUND:
        raise BinanceSymbolNotFound(resp['msg'])


# get all subscribed symbols
async def binance_symbols():
    resp = await Registry().binance.get_symbols()
    return resp['data']


# get raw trades
async def binance_raw_trades(symbol_: str, since_: int, to_: int):
    if not validate_quote_base(symbol_):
        raise BinanceUnprocessableEntity(_BINANCE_ERR_MSG_ENTITY_UNPROCESSING)

    resp = await Registry().binance.get_trades(symbol_, since_, to_)
    data = resp['data']
    if not len(data):
        return []

    result = group_list_dict(resp['data'], "symbol")
    return result


# get trades stat
async def binance_trades_stat(symbol_: str, since_: int, to_: int, side_: str):
    if not validate_quote_base(symbol_):
        raise BinanceUnprocessableEntity(_BINANCE_ERR_MSG_ENTITY_UNPROCESSING)

    resp = await Registry().binance.get_trades(symbol_, since_, to_)
    data = resp['data']
    if not len(data):
        return []

    # calculate trades stat of more assets
    group_data = group_list_dict(data, 'symbol')
    if type(group_data) == dict:
        result = {}
        for key, value in group_data.items():
            result[key] = calculate_trade_stat(value, side_)
        return result

    # calculate trades stat of one asset
    result = calculate_trade_stat(group_data, side_)
    return result


# get volume imbalance
async def binance_volume_imbalance(symbol_: str, since_: int, to_: int):
    if not validate_quote_base(symbol_):
        raise BinanceUnprocessableEntity(_BINANCE_ERR_MSG_ENTITY_UNPROCESSING)

    resp = await Registry().binance.get_trades(symbol_, since_, to_)
    data = resp['data']
    if not len(data):
        return []

    # calculate volume imbalance of more assets
    group_data = group_list_dict(resp['data'], 'symbol')
    if type(group_data) == dict:
        result = {}
        for key, value in group_data.items():
            result[key] = calculate_volume_imbalance(value)
        return result

    # calculate volume imbalance of one asset
    result = calculate_volume_imbalance(group_data)
    return result
