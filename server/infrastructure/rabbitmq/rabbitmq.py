import os
from aio_pika import connect_robust
from aio_pika.patterns import RPC
from aio_pika.exceptions import CONNECTION_EXCEPTIONS

_URI = os.environ.get("RABBITMQ_URI")
_NAME = os.environ.get("RABBITMQ_NAME")


async def get_rpc() -> RPC:
    try:
        connection = await connect_robust(_URI, client_properties={"connection_name": _NAME})
        channel = await connection.channel()
        rpc = await RPC.create(channel)
        return rpc

    except CONNECTION_EXCEPTIONS as e:
        raise e
