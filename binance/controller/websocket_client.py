import asyncio
import os
import websockets
import json

from usecase import SymbolUsecase, TradeUsecase
from util.log import log_info, log_error

_URL: str = os.environ.get("BINANCE_WEBSOCKET_URL")


# websocket client for connect to binance websocket
async def websocket_client(symbol_usecase: SymbolUsecase, trade_usecase: TradeUsecase):
    log_info("Websocket Client connected to Binance...")
    async with websockets.connect(_URL) as websocket:
        try:
            symbol_size = symbol_usecase.size()
            subscribed_symbol = await send_subscribe(websocket, symbol_usecase)

            while True:
                # receive and save trade info
                raw = await websocket.recv()
                data = response_converter(raw)
                if "E" in data.keys():
                    await trade_usecase.save(symbol_usecase, data)

                # check condition for sub & unsub
                if symbol_usecase.size() > symbol_size:
                    symbol_size = symbol_usecase.size()
                    subscribed_symbol = await send_subscribe(websocket, symbol_usecase)
                elif 0 < symbol_usecase.size() < symbol_size:
                    symbol_size = symbol_usecase.size()
                    subscribed_symbol = await send_unsubscribe(websocket, symbol_usecase, subscribed_symbol)
                elif symbol_usecase.size() == 0:
                    await send_unsubscribe(websocket, symbol_usecase, subscribed_symbol)
                    while True:
                        log_info("subscription is empty, waiting for subscribe any symbols")
                        if symbol_usecase.size() > 0:
                            symbol_size = 1
                            subscribed_symbol = await send_subscribe(websocket, symbol_usecase)
                            break
                        await asyncio.sleep(1)

        except websockets.ConnectionClosed as e:
            log_error(e.__str__())
        finally:
            log_info("Websocket Client closed...")
            await websocket.close()


# send message to binance websocket for subscribe
async def send_subscribe(websocket, symbol_usecase: SymbolUsecase) -> list:
    params = await symbol_usecase.to_params(["trade"])
    log_info(f"subscription => {params}")

    # create message
    msg = {
        "method": "SUBSCRIBE",
        "params": params,
        "id": 1
    }
    msg = str(msg).replace("'", '"')
    await websocket.send(msg)
    return params


# send message to binance websocket for unsubscribe
async def send_unsubscribe(websocket, symbol_usecase: SymbolUsecase, subscribed_symbol: list) -> list:
    params = await symbol_usecase.to_params(["trade"])
    unscribed_params = list(filter(lambda item: item not in params, subscribed_symbol))

    msg = {
        "method": "UNSUBSCRIBE",
        "params": unscribed_params,
        "id": 312
    }
    msg = str(msg).replace("'", '"')
    await websocket.send(msg)
    return params


# convert response data to dict
def response_converter(raw) -> dict:
    decode = json.loads(raw)
    data = dict(decode)
    return data
