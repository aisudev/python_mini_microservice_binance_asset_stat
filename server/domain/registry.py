from domain.model.singleton import Singleton


class Registry(metaclass=Singleton):
    def __init__(self):
        from domain.port.binance_port import BinancePort
        self.binance: BinancePort | None = None
