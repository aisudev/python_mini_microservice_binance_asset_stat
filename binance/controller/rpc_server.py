import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import RPC
from aio_pika.exceptions import CONNECTION_EXCEPTIONS
import os

from router import RPCRouter
from util.log import log_info, log_error

_URI = os.environ.get("RABBITMQ_URI")
_NAME = os.environ.get("RABBITMQ_NAME")


async def rpc_consumer(rpc_router: RPCRouter) -> None:
    try:
        # connection & create RPC pattern
        connection = await connect_robust(_URI, client_properties={"connection_name": _NAME})
        channel = await connection.channel()
        rpc = await RPC.create(channel)

        # Register queues for process function of symbol.
        await rpc.register("symbol.subscribe", rpc_router.symbol_subscribe, auto_delete=True)
        await rpc.register("symbol.unsubscribe", rpc_router.symbol_unsubscribe, auto_delete=True)
        await rpc.register("symbol.all", rpc_router.get_symbols, auto_delete=True)

        # Register queues for process function of trade.
        await rpc.register("trade.raw_trades", rpc_router.get_raw_trades, auto_delete=True)

        # other
        log_info("RPC start...")
        try:
            await asyncio.Future()
        finally:
            await connection.close()
            log_info("RPC closed...")

    except CONNECTION_EXCEPTIONS as e:
        log_error(e.__str__())
        raise e
