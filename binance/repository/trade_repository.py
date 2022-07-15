from model import Singleton, TradeModel


class TradeRepository(metaclass=Singleton):
    def __init__(self):
        self.__data: list[TradeModel] = []

    # add trade order info
    async def save(self, trade_model_: TradeModel):
        self.__data.append(trade_model_)
        self.__data = sorted(self.__data, key=lambda item: item.traded_at, reverse=True)

    # return all data
    def all(self) -> list[TradeModel]:
        return self.__data

    # overwrite data
    def overwrite(self, data_: list[TradeModel]):
        self.__data = data_

    # get size of data
    def size(self) -> int:
        return len(self.__data)





