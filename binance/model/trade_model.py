from dataclasses import dataclass


@dataclass
class TradeModel:
    symbol: str
    price: float
    volume: int
    traded_at: int
    side: str
