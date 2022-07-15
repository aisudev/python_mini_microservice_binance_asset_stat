import asyncio
from datetime import datetime, timedelta

from usecase import SymbolUsecase, TradeUsecase
from util.log import log_info


async def data_manager(symbol_usecase: SymbolUsecase, trade_usecase: TradeUsecase):

    # current symbols size
    symbols_size = symbol_usecase.size()
    log_info("Data Manager start...")

    while True:
        # filter trade orders which less than 5min out.
        bound_timestamp = int((datetime.now() - timedelta(minutes=5)).timestamp() * 1000)
        await trade_usecase.filterout_least_timestamp(bound_timestamp)

        # filter trade orders that related to symbols in.
        if symbols_size != symbol_usecase.size():
            symbols_size = symbol_usecase.size()
            symbols = symbol_usecase.all()
            await trade_usecase.filterin_symbols(symbols)

        await asyncio.sleep(1)
