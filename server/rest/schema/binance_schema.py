from pydantic import BaseModel


class SymbolRequestBody(BaseModel):
    symbol: str
