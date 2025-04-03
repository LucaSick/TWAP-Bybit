"""
Abstract base class representing the interface for interacting with a trading exchange.
"""
class ExchangeInterface:
    """
    Fetches market data for the given symbol (e.g., current bid/ask prices).
    Args -> symbol (str): The trading pair symbol (e.g., 'BTC/USDT').
    Returns -> dict: A dictionary containing relevant symbol data (e.g., bid/ask prices).
    """
    def get_symbol_data(symbol):
        pass

    """
    Places an order on the exchange.
    Args ->
        symbol (str): The trading symbol.
        side (sideType): Whether to buy ('bid') or sell ('ask').
        size (float): The quantity of the asset to trade.
        price (float): The price at which to place the order.
    Returns ->
        dict: A dictionary representing the response from the exchange.
    """
    def make_order(symbol, side, size, price):
        pass