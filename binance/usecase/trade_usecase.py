from model import TradeModel
from usecase import SymbolUsecase

import dataclasses
from datetime import timedelta, datetime


class TradeUsecase:
    def __init__(self):
        from repository import TradeRepository
        self.__repo = TradeRepository()

    async def all(self, symbol: str = "", since: int = 0, to: int = 0):
        # return all data
        data = self.__repo.all()
        if not symbol and not since and not to:
            result = [dataclasses.asdict(item) for item in data]
            return result

        # return data where traded_at between since and to
        since = since if since else int((datetime.now() - timedelta(minutes=5)).timestamp() * 1000)
        to = to if to else int(datetime.now().timestamp() * 1000)
        if not symbol:
            tmp = filter(lambda item: since <= item.traded_at <= to, data)
            result = [dataclasses.asdict(item) for item in tmp]
            return result

        # return data where equal to symbol and traded_at between since and to
        tmp = filter(lambda item: item.symbol == symbol and since <= item.traded_at <= to, data)
        result = [dataclasses.asdict(item) for item in tmp]
        return result

    # save preprocess trade data and save into repository
    async def save(self, symbol_usecase: SymbolUsecase, data_: dict):
        symbol = await symbol_usecase.name_to_symbol(data_["s"])
        if not symbol:
            return

        side = "sell" if data_["m"] else "buy"
        trade_model = TradeModel(
            symbol=symbol,
            price=data_["p"],
            volume=data_["q"],
            traded_at=data_["T"],
            side=side
        )
        await self.__repo.save(trade_model)

    # filter trades where symbol whick not in symbols list out.
    async def filterin_symbols(self, symbols: list[str]):
        data = self.__repo.all()
        new_data: list[TradeModel] = list(filter(lambda item: item.symbol in symbols, data))
        self.__repo.overwrite(new_data)

    # filter trades where traded_at least than bound out.
    async def filterout_least_timestamp(self, bound: int):
        data = self.__repo.all()
        new_data: list[TradeModel] = list(filter(lambda item: item.traded_at >= bound, data))
        self.__repo.overwrite(new_data)
