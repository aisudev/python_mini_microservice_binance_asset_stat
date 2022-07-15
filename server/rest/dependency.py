from infrastructure.rabbitmq import get_rpc
from adapter.binance_rabbitmq_adapter import BinanceRabbitMQAdapter
from domain.registry import Registry


# injection
async def inject():
    rpc = await get_rpc()
    Registry().binance = BinanceRabbitMQAdapter(rpc)

