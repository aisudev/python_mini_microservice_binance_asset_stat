from model import Singleton, SymbolModel

_INITIAL_SYMBOLS = [SymbolModel("BTC/USDT", "BTCUSDT", "btcusdt"), SymbolModel("ETH/USDT", "ETHUSDT", "ethusdt")]


class SymbolRepository(metaclass=Singleton):
    def __init__(self):
        self.__data: list[SymbolModel] = _INITIAL_SYMBOLS

    # add symbol
    async def save(self, symbol_model_: SymbolModel):
        self.__data.append(symbol_model_)

    # get size of data
    def size(self) -> int:
        return len(self.__data)

    # get all data
    def all(self) -> list[SymbolModel]:
        return self.__data

    # is in list?
    def isin(self, symbol_: str) -> bool:
        return 0 < len([item for item in self.__data if item == symbol_])

    # overwrite into data
    def overwrite(self, data_: list[SymbolModel]):
        self.__data = data_




