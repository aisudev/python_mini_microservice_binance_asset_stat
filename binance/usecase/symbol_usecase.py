from model import SymbolModel
from .exception.exception import EntityAlreadyExistException, EntityNotFound

_ERR_MSG_SYMBOL_ALREADY_EXIST = "can not create, symbol already exist"
_ERR_MSG_SYMBOL_NOTFOUND = "symbol does not exist"


class SymbolUsecase:
    def __init__(self):
        from repository import SymbolRepository
        self.__repo = SymbolRepository()

    def all(self) -> list[str]:
        data = [item.symbol for item in self.__repo.all()]
        return data

    # add new symbol
    async def save(self, symbol_: str):
        if self.__repo.isin(symbol_):
            raise EntityAlreadyExistException(_ERR_MSG_SYMBOL_ALREADY_EXIST)

        name = symbol_.replace("/", "")
        key = name.lower()
        symbol_model = SymbolModel(
            symbol=symbol_,
            name=name,
            key=key
        )

        await self.__repo.save(symbol_model)

    # remove symbol from data
    async def delete(self, symbol_):
        if not self.__repo.isin(symbol_):
            raise EntityNotFound(_ERR_MSG_SYMBOL_NOTFOUND)

        data = self.__repo.all()
        deleted_data = list(filter(lambda item: item != symbol_, data))
        self.__repo.overwrite(deleted_data)

    # get size of data
    def size(self):
        return self.__repo.size()

    # convert name to symbol
    async def name_to_symbol(self, name_: str) -> str:
        data = self.__repo.all()
        for item in data:
            if item.name == name_:
                return item.symbol

        return ""

    # convert to parameter
    async def to_params(self, types_: list[str]) -> list:
        data = self.__repo.all()
        params = []
        keys = [item.key for item in data]

        for t in types_:
            for k in keys:
                params.append(f"{k}@{t}")
        return params




