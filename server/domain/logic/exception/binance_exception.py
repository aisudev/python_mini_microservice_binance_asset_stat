class BinanceSymbolNotFound(Exception):
    pass


class BinanceSymbolAlreadyExist(Exception):
    pass


class BinanceTradeNotRelatedToSymbol(Exception):
    pass


class BinanceUnprocessableEntity(Exception):
    pass
