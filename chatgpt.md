GoTrade Functions Documentation

This document provides detailed information on the available functions in the **GoTrade** module, organized by the exchanges they belong to. Each exchange supports trading operations, including market orders, limit orders, time-weighted average price (TWAP) orders, and edge-based strategies.

---

## Import Statements

To use the GoTrade functionalities for specific exchanges, import them as follows:

```python
from GoTrade.exchanges import bybit 
from GoTrade.exchanges import okx 
OKX Functions
The okx module provides tools for trading on the OKX exchange. It supports market orders, limit orders, TWAP strategies, and edge-based strategies.

1. okx.login()
Description:
Logs into the OKX exchange account. Ensure credentials are properly configured in your environment or settings.

Usage:

python
Copy code
okx.login()
2. okx.market_order
Description:
Places a market order on OKX. A market order is executed immediately at the best available price.

Parameters:

symbol (str): Trading pair (e.g., "DOT-USDT-SWAP").
side (str): Order direction, either "buy" or "sell".
quantity (float): The amount to trade.
blocking (bool): Whether to block execution until the order is filled.
Usage:

python
Copy code
okx.market_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, blocking=True)
3. okx.limit_order
Description:
Places a limit order on OKX, which allows setting a specific price for execution.

Parameters:

symbol (str): Trading pair (e.g., "DOT-USDT-SWAP").
side (str): Order direction, either "buy" or "sell".
quantity (float): The amount to trade.
price (float): The price at which to execute the trade.
blocking (bool): Whether to block execution until the order is filled.
Usage:

python
Copy code
okx.limit_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, price=9.2, blocking=True)
4. okx.market_edge_order
Description:
Places a market order with a maximum time for order completion.

Parameters:

symbol (str): Trading pair (e.g., "DOT-USDT-SWAP").
side (str): Order direction, either "buy" or "sell".
quantity (float): The amount to trade.
max_timer (int): Maximum time in seconds to complete the order.
blocking (bool): Whether to block execution until the order is filled.
Usage:

python
Copy code
okx.market_edge_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, max_timer=30, blocking=True)
5. okx.twap_order
Description:
Places a TWAP order, which splits the total quantity into smaller parts to be executed over a specified duration.

Parameters:

symbol (str): Trading pair (e.g., "DOT-USDT-SWAP").
side (str): Order direction, either "buy" or "sell".
quantity (float): Total quantity to trade.
duration (int): Total time in seconds for the order.
interval (int): Time in seconds between each smaller order.
blocking (bool): Whether to block execution until the order is filled.
Usage:

python
Copy code
okx.twap_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, duration=60, interval=15, blocking=True)
6. okx.twap_edge_order
Description:
Places a TWAP order with an edge strategy, ensuring execution within a defined time window.

Parameters:

symbol (str): Trading pair (e.g., "DOT-USDT-SWAP").
side (str): Order direction, either "buy" or "sell".
quantity (float): Total quantity to trade.
duration (int): Total time in seconds for the order.
interval (int): Time in seconds between each smaller order.
blocking (bool): Whether to block execution until the order is filled.
Usage:

python
Copy code
okx.twap_edge_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, duration=120, interval=30, blocking=True)
Bybit Functions
The bybit module supports similar trading operations for the Bybit exchange. It includes functionality for perpetual, spot, and linear contracts.

1. bybit.login()
Description:
Logs into the Bybit exchange account. Ensure credentials are properly configured.

Usage:

python
Copy code
bybit.login()
2. bybit.market_order
Description:
Places a market order on Bybit.

Parameters:

symbol (str): Trading pair (e.g., "EOSUSDT").
side (str): Order direction, either "buy" or "sell".
quantity (float): The amount to trade.
blocking (bool): Whether to block execution until the order is filled.
instrument_type (str): Type of market ("LINEAR", "SPOT", etc.).
Usage:

python
Copy code
bybit.market_order(symbol="EOSUSDT", side="buy", quantity=10, blocking=True, instrument_type="LINEAR")
3. bybit.limit_order
Description:
Places a limit order on Bybit.

Parameters:

symbol (str): Trading pair (e.g., "DOTUSDT").
side (str): Order direction, either "buy" or "sell".
quantity (float): The amount to trade.
price (float): The price at which to execute the trade.
blocking (bool): Whether to block execution until the order is filled.
instrument_type (str): Type of market ("LINEAR", "SPOT", etc.).
Usage:

python
Copy code
bybit.limit_order(symbol="DOTUSDT", side="buy", quantity=1, price=9.2, blocking=True, instrument_type="LINEAR")
4. bybit.market_edge_order
Description:
Places a market order with a maximum time for order completion.

Parameters:

symbol (str): Trading pair (e.g., "ETHUSDT").
side (str): Order direction, either "buy" or "sell".
quantity (float): The amount to trade.
max_timer (int): Maximum time in seconds to complete the order.
blocking (bool): Whether to block execution until the order is filled.
instrument_type (str): Type of market ("LINEAR", "SPOT", etc.).
Usage:

python
Copy code
bybit.market_edge_order(symbol="ETHUSDT", side="buy", quantity=1, max_timer=30, blocking=True, instrument_type="SPOT")
5. bybit.twap_order
Description:
Places a TWAP order on Bybit.

Parameters:

symbol (str): Trading pair (e.g., "DOTUSDT").
side (str): Order direction, either "buy" or "sell".
quantity (float): Total quantity to trade.
duration (int): Total time in seconds for the order.
interval (int): Time in seconds between each smaller order.
blocking (bool): Whether to block execution until the order is filled.
instrument_type (str): Type of market ("LINEAR", "SPOT", etc.).
Usage:

python
Copy code
bybit.twap_order(symbol="DOTUSDT", side="buy", quantity=1, duration=60, interval=15, blocking=True, instrument_type="LINEAR")
6. bybit.twap_edge_order
Description:
Places a TWAP order with an edge strategy.

Parameters:

symbol (str): Trading pair (e.g., "BTCUSDT").
side (str): Order direction, either "buy" or "sell".
quantity