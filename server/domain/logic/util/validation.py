import re


def validate_quote_base(symbol_: str):
    if not symbol_:
        return True

    pattern = re.compile("([A-Z]+)(/)([A-Z]+)")
    return bool(pattern.match(symbol_))
