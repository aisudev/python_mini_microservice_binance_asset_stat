from dataclasses import dataclass


@dataclass
class SymbolModel:
    symbol: str
    name: str
    key: str

    def __eq__(self, other) -> bool:
        return self.symbol == other
