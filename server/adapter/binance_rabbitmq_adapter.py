from domain.port.binance_port import BinancePort
from aio_pika.exceptions import MessageProcessError


class BinanceRabbitMQAdapter(BinancePort):
    def __init__(self, rpc):
        self.rpc = rpc

    async def subscribe(self, symbol_: str) -> dict:
        try:
            return await self.rpc.call("symbol.subscribe", kwargs=dict(symbol=symbol_))
        except MessageProcessError as e:
            raise e

    async def unsubscribe(self, symbol_: str) -> dict:
        try:
            return await self.rpc.call("symbol.unsubscribe", kwargs=dict(symbol=symbol_))
        except MessageProcessError as e:
            raise e

    async def get_symbols(self) -> list:
        try:
            return await self.rpc.call("symbol.all")
        except MessageProcessError as e:
            raise e

    async def get_trades(self, symbol_: str, since_: int, to_: int) -> dict:
        try:
            return await self.rpc.call("trade.raw_trades", kwargs=dict(symbol=symbol_, since=since_, to=to_))
        except MessageProcessError as e:
            raise e
