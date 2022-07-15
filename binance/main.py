import os
import sys
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import asyncio
import uvloop
from concurrent import futures
from dotenv import load_dotenv
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), ".env")))


from usecase import SymbolUsecase, TradeUsecase
from controller import rpc_consumer, websocket_client, data_manager
from router import RPCRouter


# main function.
def main():
    # declare usecase
    symbol_usecase = SymbolUsecase()
    trade_usecase = TradeUsecase()

    # declare rpc router
    rpc_router = RPCRouter(symbol_usecase, trade_usecase)

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(asyncio.run, rpc_consumer(rpc_router))
        executor.submit(asyncio.run, websocket_client(symbol_usecase, trade_usecase))
        executor.submit(asyncio.run, data_manager(symbol_usecase, trade_usecase))


if __name__ == "__main__":
    uvloop.install()
    main()


