from abc import abstractmethod


class BinancePort:
    @abstractmethod
    async def subscribe(self, symbol_: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def unsubscribe(self, symbol_: str) -> dict:
        raise NotImplementedError
    
    @abstractmethod
    async def get_symbols(self) -> list:
        raise NotImplementedError

    @abstractmethod
    async def get_trades(self, symbol_: str, since_: int, to_: int) -> dict:
        raise NotImplementedError
