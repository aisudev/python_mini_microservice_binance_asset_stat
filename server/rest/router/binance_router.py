from fastapi import APIRouter, HTTPException, status
from rest.schema.binance_schema import SymbolRequestBody
from domain.logic.binance_logic import \
    binance_subscribe, \
    binance_unsubscribe, \
    binance_raw_trades, \
    binance_trades_stat, \
    binance_volume_imbalance, \
    binance_symbols
from domain.logic.exception.binance_exception import \
    BinanceSymbolNotFound, \
    BinanceSymbolAlreadyExist,\
    BinanceUnprocessableEntity
from aio_pika.exceptions import MessageProcessError

binance_router = APIRouter()


@binance_router.post("/subscribe_trade_symbol", status_code=status.HTTP_201_CREATED)
async def subscribe_trade_symbol(body: SymbolRequestBody):
    try:
        await binance_subscribe(body.symbol)

    except BinanceSymbolAlreadyExist as e:
        raise HTTPException(status.HTTP_409_CONFLICT, e.__str__())
    except MessageProcessError as e: 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e.__str__())


@binance_router.post("/unsubscribe_trade_symbol", status_code=status.HTTP_200_OK)
async def unsubscribe_trade_symbol(body: SymbolRequestBody):
    try:
        await binance_unsubscribe(body.symbol)

    except BinanceSymbolNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, e.__str__())
    except MessageProcessError as e: 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e.__str__())


@binance_router.get("/symbols", status_code=status.HTTP_200_OK)
async def get_symbols():
    try:
        data = await binance_symbols()
        return dict(data=data)

    except MessageProcessError as e: 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e.__str__())


@binance_router.get("/get_raw_trades", status_code=status.HTTP_200_OK)
async def get_raw_trades(symbol: str = None, since: int = None, to: int = None):
    try:
        data = await binance_raw_trades(symbol_=symbol, since_=since, to_=to)
        return dict(data=data)

    except BinanceUnprocessableEntity as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.__str__())
    except MessageProcessError as e: 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e.__str__())


@binance_router.get("/get_trades_stat", status_code=status.HTTP_200_OK)
async def get_trades_stat(symbol: str = None, since: int = None, to: int = None, side: str = "buy"):
    if side != "buy" and side != "sell":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "side should be buy or sell")

    try:
        data = await binance_trades_stat(symbol, since, to, side)
        return data

    except BinanceUnprocessableEntity as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.__str__())
    except MessageProcessError as e: 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e.__str__())


@binance_router.get("/get_volume_imbalance", status_code=status.HTTP_200_OK)
async def get_volume_imbalance(symbol: str = None, since: int = None, to: int = None):
    try:
        data = await binance_volume_imbalance(symbol, since, to)
        return data

    except BinanceUnprocessableEntity as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.__str__())
    except MessageProcessError as e: 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, e.__str__())
