from usecase import SymbolUsecase, TradeUsecase
from usecase.exception import EntityAlreadyExistException, EntityNotFound
from router.util.response import rpc_response, STATUS_ERR_EXIST, STATUS_ERR_NOTFOUND, STATUS_MODIFIED


class RPCRouter:
    def __init__(self, symbol_usecase_: SymbolUsecase, trade_usecase_: TradeUsecase):
        self.symbol_usecase = symbol_usecase_
        self.trade_usecase = trade_usecase_

    # router for subscribe symbol
    async def symbol_subscribe(self, symbol: str):
        try:
            await self.symbol_usecase.save(symbol)
            return rpc_response(STATUS_MODIFIED)
        except EntityAlreadyExistException as e:
            return rpc_response(STATUS_ERR_EXIST, msg=e.__str__())

    # router for unsubscribe symbol
    async def symbol_unsubscribe(self, symbol: str):
        try:
            await self.symbol_usecase.delete(symbol)
            return rpc_response(STATUS_MODIFIED)
        except EntityNotFound as e:
            return rpc_response(STATUS_ERR_NOTFOUND, msg=e.__str__())

    # router for get subscribed symbols
    async def get_symbols(self):
        result = self.symbol_usecase.all()
        return rpc_response(data=result)

    # router for get raw trades symbol
    async def get_raw_trades(self, symbol: str, since: int, to: int):
        result = await self.trade_usecase.all(symbol, since, to)
        return rpc_response(data=result)
