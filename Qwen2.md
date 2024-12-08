# GoTrade Module Documentation

Generated on: 12/7/2024, 8:33:56 PM

## message_structures.py

Certainly! Below is an example of how you can document your Python code in a format suitable for a module documentation, including necessary import statements based on the provided structure.

### Module Documentation for `gotrade.message_structures`

---

#### Module: gotrade.message_structures

This module defines various C-structure-like classes and unions using the ctypes library to represent different message structures used within the trading system. The primary purpose of these structures is to facilitate communication between different components of the system, ensuring that messages are correctly formatted according to specific algorithms.

##### Import Statements:

```python
from ctypes import Structure, Union, c_int, c_double, c_char
```

---

### Classes and Unions

#### `TwapParams`
A structure representing parameters for Time-Weighted Average Price (TWAP) algorithm.

**Fields:**
- **duration:** int - The duration of the TWAP algorithm in seconds.
- **interval:** int - The interval at which orders are placed during the TWAP session in milliseconds.

```python
class TwapParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("duration", c_int),
        ("interval", c_int)
    ]
```

---

#### `MarketEdgeParams`
A structure representing parameters for a Market Edge algorithm.

**Fields:**
- **max_timer:** int - The maximum time in seconds before the algorithm should be executed or considered invalid.

```python
class MarketEdgeParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("max_timer", c_int)
    ]
```

# Collection of all available functions in GoTrade

## Import statements
```
from GoTrade.exchanges import bybit 
from GoTrade.exchanges import okx 
```
## OKX Functions
```
okx.login()
okx.market_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, blocking=True)
okx.limit_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, price=9.2, blocking=True)
okx.market_edge_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, max_timer=30, blocking=True)
okx.twap_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, duration=60, interval=15, blocking=True)
okx.twap_edge_order(symbol="DOT-USDT-SWAP", side="buy", quantity=1, duration=120, interval=30, blocking=True)
```
## Bybit Functions
```
bybit.login()
bybit.market_order(symbol="EOSUSDT", side="buy", quantity=10, blocking=True, instrument_type="LINEAR")
bybit.limit_order(symbol="DOTUSDT", side="buy", quantity=1, price=9.2, blocking=True, instrument_type="LINEAR")
bybit.market_edge_order(symbol="ETHUSDT", side="buy", quantity=1, max_timer=30, blocking=True, instrument_type="SPOT")
bybit.twap_order(symbol="DOTUSDT", side="buy", quantity=1, duration=60, interval=15, blocking=True, instrument_type="LINEAR")
bybit.twap_edge_order(symbol="BTCUSDT", side="buy", quantity=1, duration=120, interval=30, blocking=True, instrument_type="SPOT")
```

---

#### `TPSLParams`
A structure representing parameters for Take Profit and Stop Loss (TP/SL) algorithm.

**Fields:**
- **tp_percentage:** double - The percentage of the current price at which to set a take profit order.
- **sl_percentage:** double - The percentage of the current price at which to set a stop loss order.

```python
class TPSLParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("tp_percentage", c_double),
        ("sl_percentage", c_double)
    ]
```

---

#### `PlaceParams`
A structure representing parameters for placing an order.

**Fields:**
- **type:** char[16] - The type of order to be placed.
- **instrument_type:** char[16] - The type of instrument being traded (e.g., "STOCK", "FUTURE").

```python
class PlaceParams(Structure):
    _pack_ = 1
    _fields_ = [
        ("type", c_char * 16),
        ("instrument_type", c_char * 16)
    ]
```

---

#### `AlgoParams`
A union representing different algorithm-specific parameters. Only one of the fields (`twap`, `market_edge`, `place`, or `tpsl`) will be valid at any given time.

**Fields:**
- **twap:** TwapParams
- **market_edge:** MarketEdgeParams
- **place:** PlaceParams
- **tpsl:** TPSLParams

```python
class AlgoParams(Union):
    _pack_ = 1
    _fields_ = [
        ("twap", TwapParams),
        ("market_edge", MarketEdgeParams),
        ("place", PlaceParams),
        ("tpsl", TPSLParams)
    ]
```

---

#### `SideOrPlaceID`
A union representing either a side of the order or an ID associated with placing orders.

**Fields:**
- **side:** char[8] - The trading side (e.g., "BUY", "SELL").
- **place_id:** int - An identifier for the placement of an order.

```python
class SideOrPlaceID(Union):
    _pack_ = 1
    _fields_ = [
        ("side", c_char * 8),
        ("place_id", c_int)
    ]
```

---

#### `GQMessage`
A structure representing a generic trading message used to communicate with the exchange.

**Fields:**
- **algorithm_type:** char[16] - The type of algorithm being executed.
- **exchange:** char[16] - The name of the exchange.
- **account:** char[32] - The account identifier.
- **symbol:** char[32] - The trading symbol (e.g., "AAPL", "BTCUSD").
- **side_or_place_id:** SideOrPlaceID
- **quantity:** double - The quantity of units to trade.
- **price:** double - The price at which the order is placed or executed.
- **credential_id:** char[40] - An identifier for authentication purposes.
- **params:** AlgoParams

```python
class GQMessage(Structure):
    _pack_ = 1
    _fields_ = [
        ("algorithm_type", c_char * 16),
        ("exchange", c_char * 16),
        ("account", c_char * 32),
        ("symbol", c_char * 32),
        ("side_or_place_id", SideOrPlaceID),
        ("quantity", c_double),
        ("price", c_double),
        ("credential_id", c_char * 40),
        ("params", AlgoParams)
    ]
```

---

This documentation provides a clear and concise description of each structure and union, along with their respective fields. It serves as an essential reference for developers working on the gotrade system to understand how these structures are used in message communication.

---

## oems_operations.py

### Part 1/4

Certainly! Below is the comprehensive documentation for your module `gotrade.oems_operations`, including import statements, function descriptions with parameter details, return types, and any other relevant information.

---

### Module Documentation: `gotrade.oems_operations`

#### Imports

```python
import ctypes
from datetime import datetime
import http.client
import json
import threading
from .message_structures import GQMessage
from typing import Optional, Union, Dict, Any
from http import HTTPStatus
from .request_types import LoginResponse, OrderResponse, LoginRequest, MarketOrderRequest, LimitOrderRequest, TWAPOrderRequest, MarketEdgeOrderRequest, TwapEdgeOrderRequest
```

#### Constants

```python
HOSTNAME = "localhost"
HANDSHAKE_TOKEN = "9f2b9e0cd9a1a2c95b4e0b123c7b8d6a"
```

#### Functions

##### `login_to_exchange`
Login to the trading exchange.

**Parameters:**
- **exchange_name (str):** The name of the exchange.
- **account_name (str):** The account name on the exchange.
- **key (str):** The API key for authentication.
- **secret (str):** The secret key for authentication.
- **passphrase (str, optional):** A passphrase if required by the exchange. Defaults to an empty string.
- **authenticate (bool, optional):** Whether to authenticate with a handshake or not. Defaults to `True`.

**Returns:**
- **LoginResponse:** An object containing success status, HTTP code, and message.

**Example Usage:**

```python
response = login_to_exchange(
    exchange_name="TestExchange",
    account_name="testuser123",
    key="your_api_key_here",
    secret="your_secret_key_here"
)
print(response.success)  # True or False based on success status.
```

---

##### `_send_order`
Send an order to the trading exchange.

**Parameters:**
- **msg (GQMessage):** A `GQMessage` object containing order details.

**Returns:**
- **OrderResponse:** An object with success status, HTTP code, and message.

**Example Usage:**

```python
order_response = _send_order(msg=your_gq_message_object)
print(order_response.message)  # Message indicating if the order was sent or failed.
```

---

##### `_send_order_nonblocking`
Send an order to the trading exchange non-blocking. This function is intended for asynchronous operations and ensures request completion without waiting.

**Parameters:**
- **msg (GQMessage):** A `GQMessage` object containing order details.

**Returns:**
- **OrderResponse:** An object with success status, HTTP code, and message.

**Example Usage:**

```python
def callback(order_response):
    print(f"Order sent {order_response.message}")

send_order_task = threading.Thread(target=_send_order_nonblocking, args=(your_gq_message_object,))
send_order_task.start()
```

---

### Notes:
1. **Error Handling**: Both `_send_order` and `_send_order_nonblocking` functions are designed with robust error handling to manage network errors or unexpected issues during order placement.
2. **Asynchronous Usage** : Use `_send_order_nonblocking` for scenarios where non-blocking operation is required, such as when multiple orders need to be placed simultaneously without waiting for each other's completion.

---

This documentation should provide a clear guide on how to use the functions in your `gotrade.oems_operations` module. If you have any additional functionality or custom exceptions that are part of this file, please let me know so I can incorporate them into the documentation!

### Part 2/4

Certainly! Below is a comprehensive documentation template for the `oems_operations` module, including necessary imports from other modules based on the provided code snippet. The documentation includes descriptions of each function and their parameters.

### Module Documentation

#### File Path:
- **gotrade/oems_operations**

#### Imports:
```python
from gotrade.oems.oems_request import MarketOrderRequest, LimitOrderRequest
from gotrade.oems.oems_message import GQMessage
from gotrade.oems.order_response import OrderResponse
from http.client import HTTPConnection
import datetime
```

### Function Documentation

#### `_send_order`
This function sends a market order to OEMS and returns an `OrderResponse` object. It is used internally by the `place_market_order` and `place_limit_order` functions.

##### Parameters:
- **msg (GQMessage)**: The GQMessage object containing order details.
  
##### Returns:
- An instance of `OrderResponse`, indicating whether the operation was successful, along with other metadata like status code and message.

#### `_send_order_nonblocking`
This function sends a market or limit order to OEMS in a non-blocking manner. It is used internally by the `place_market_order` and `place_limit_order` functions when the `blocking=False`.

##### Parameters:
- **msg (GQMessage)**: The GQMessage object containing order details.
  
##### Returns:
- A boolean value indicating whether the order was successfully submitted.

#### `place_market_order`
This function places a market order through OEMS. It returns an `OrderResponse` object based on the success of the operation.

##### Parameters:
- **exchange_name (str, optional)**: Name of the exchange where the order is to be placed.
- **account_name (str, optional)**: Name of the trading account used for placing orders.
- **symbol (str, optional)**: Trading symbol or asset type for which the order should be executed.
- **side (str, optional)**: Side of the trade ("buy" or "sell").
- **quantity (float, optional)**: Number of units to buy/sell.
- **blocking (bool, default=True)**: If True, waits for response; if False, sends asynchronously and returns immediately.
- **instrument_type (str, default="")**: Type of financial instrument.

##### Returns:
- An instance of `OrderResponse`, containing success status, status code, message, and optional response data.

#### `place_limit_order`
This function places a limit order through OEMS. It returns an `OrderResponse` object based on the success of the operation.

##### Parameters:
- **exchange_name (str, optional)**: Name of the exchange where the order is to be placed.
- **account_name (str, optional)**: Name of the trading account used for placing orders.
- **symbol (str, optional)**: Trading symbol or asset type for which the order should be executed.
- **side (str, optional)**: Side of the trade ("buy" or "sell").
- **quantity (float, optional)**: Number of units to buy/sell.
- **price (float, optional)**: Limit price at which the order will be executed.
- **blocking (bool, default=True)**: If True, waits for response; if False, sends asynchronously and returns immediately.
- **instrument_type (str, default="")**: Type of financial instrument.

##### Returns:
- An instance of `OrderResponse`, containing success status, status code, message, and optional response data.

### Part 3/4

Certainly! Below is an example of how you might document your `oems_operations` module, including necessary import statements from a hypothetical `submodules.txt` configuration. I'll assume the structure and dependencies are defined in `submodules.txt`. For simplicity, let's say the file specifies modules like `gotrade.oems.order`, `gotrade.utils.validation`, etc.

### Module Documentation for gotrade.oems_operations

```python
"""
Module: gotrade.oems_operations

This module provides functions to place different types of orders through OEMS (Order Execution Management System).

Submodule Imports:
    - from gotrade.oems import order as _order
    - from gotrade.utils import validation as _validation
    - from gotrade.models import GQMessage, TWAPOrderRequest, MarketEdgeOrderRequest, OrderResponse

Functions:
    - place_twap_order(exchange_name: str, account_name: str, symbol: str, side: str, quantity: float, duration: int, interval: int, blocking: bool, instrument_type: str) -> OrderResponse
        Place a TWAP (Time-Weighted Average Price) order through OEMS.
    
    - place_market_edge_order(exchange_name: str, account_name: str, symbol: str, side: str, quantity: float, max_timer: int, blocking: bool, instrument_type: str) -> OrderResponse
        Place a Market Edge order through OEMS.

Classes:
    - GQMessage
        Represents a generic message used in OEMS operations.
    
    - TWAPOrderRequest
        Request object for TWAP order placements.
    
    - MarketEdgeOrderRequest
        Request object for Market Edge order placements.
    
    - OrderResponse
        Response object indicating the result of an order submission.

Internal Functions:
    - _send_order(msg: GQMessage) -> OrderResponse
        Sends a blocking order request to OEMS and returns the response.
    
    - _send_order_nonblocking(msg: GQMessage) -> bool
        Sends a non-blocking order request to OEMS, returning True if successful, False otherwise.

"""

from gotrade.oems import order as _order
from gotrade.utils import validation as _validation
from gotrade.models import (
    GQMessage,
    TWAPOrderRequest,
    MarketEdgeOrderRequest,
    OrderResponse
)


def place_twap_order(exchange_name: str, account_name: str, symbol: str, side: str, quantity: float, duration: int, interval: int, blocking: bool = True, instrument_type: str = "") -> OrderResponse:
    """
    Place a TWAP (Time-Weighted Average Price) order through OEMS.

    Args:
        exchange_name (str): Name of the trading exchange.
        account_name (str): Account name for the operation.
        symbol (str): Symbol representing the asset to trade.
        side (str): Side of the order ("buy" or "sell").
        quantity (float): Quantity of assets to buy/sell.
        duration (int): Duration in minutes over which the TWAP should be executed.
        interval (int): Interval in seconds between execution steps.
        blocking (bool, optional): If True, blocks until the operation is complete. Defaults to True.
        instrument_type (str, optional): Type of instrument. Defaults to "".

    Returns:
        OrderResponse: Response indicating success/failure and details of order submission.
    
    Raises:
        ValueError: If request validation fails or an invalid exchange name is provided.
    """
    # Function implementation goes here

def place_market_edge_order(exchange_name: str, account_name: str, symbol: str, side: str, quantity: float, max_timer: int, blocking: bool = True, instrument_type: str = "") -> OrderResponse:
    """
    Place a Market Edge order through OEMS.

    Args:
        exchange_name (str): Name of the trading exchange.
        account_name (str): Account name for the operation.
        symbol (str): Symbol representing the asset to trade.
        side (str): Side of the order ("buy" or "sell").
        quantity (float): Quantity of assets to buy/sell.
        max_timer (int): Maximum time allowed for market edge calculation in seconds.
        blocking (bool, optional): If True, blocks until the operation is complete. Defaults to True.
        instrument_type (str, optional): Type of instrument. Defaults to "".

    Returns:
        OrderResponse: Response indicating success/failure and details of order submission.
    
    Raises:
        ValueError: If request validation fails or an invalid exchange name is provided.
    """
    # Function implementation goes here
```

This documentation provides a clear interface for users about the functions available, their parameters, return values, and possible exceptions. Make sure to fill in the function implementations as needed.

### Part 4/4

Certainly! Below is the documentation for your `gotrade.oems_operations` module, including detailed explanations of each function with their respective parameters.

### Module Documentation

#### Imports
```python
from gotrade.models.requests import TwapEdgeOrderRequest, GQMessage, OrderResponse
```

#### Functions

##### Function: place_twap_edge_order
Place a TWAP Edge order through OEMS.

**Parameters:**
- `exchange_name` (str): The name of the exchange. Default is None.
- `account_name` (str): The account name for placing orders. Default is None.
- `symbol` (str): The symbol of the asset being traded. Default is None.
- `side` (str): Indicates if the order should be a 'buy' or 'sell'. Default is None.
- `quantity` (int): The quantity of the asset to trade. Default is None.
- `duration` (float): Duration for TWAP execution, in seconds. Default is None.
- `interval` (float): Interval between executions during TWAP period, in seconds. Default is None.
- `blocking` (bool): Indicates whether the function should block until order confirmation is received or if it should return immediately after sending the order request. Default is True.
- `instrument_type` (str): Instrument type specific to certain exchanges like Bybit. Default is an empty string.

**Returns:**
- `OrderResponse`: A response object that contains success status, HTTP status code and message for any errors encountered during the process.

---

##### Function: _send_order
Sends a blocking order request through OEMS.

This function sends a GQMessage to place a trading order on an exchange. The function blocks until it receives confirmation of order execution or rejection.

**Parameters:**
- `msg` (GQMessage): A message object containing the details necessary for placing the order.

**Returns:**
- `OrderResponse`: An OrderResponse object that contains success status and message if there were any issues during the operation.

---

##### Function: _send_order_nonblocking
Sends a non-blocking order request through OEMS.

This function sends a GQMessage to place a trading order on an exchange. Unlike `_send_order`, this method does not block for confirmation of the order's status; it returns immediately after sending the message.

**Parameters:**
- `msg` (GQMessage): A message object containing the details necessary for placing the order.

**Returns:**
- `OrderResponse`: An OrderResponse object that contains success status and message if there were any issues during the operation.

---

### Example Usage

Below is an example of how to use the functions defined in this module:

```python
from gotrade.oems_operations import place_twap_edge_order, _send_order_nonblocking

# Place a blocking TWAP Edge order
response = place_twap_edge_order(
    exchange_name="bitmex",
    account_name="my_account",
    symbol="BTC/USD",
    side="buy",
    quantity=10,
    duration=3600,
    interval=30,
    instrument_type=""
)

print(response.success, response.status_code, response.message)

# Place a non-blocking TWAP Edge order
response_nonblocking = place_twap_edge_order(
    exchange_name="bitmex",
    account_name="my_account",
    symbol="BTC/USD",
    side="buy",
    quantity=10,
    duration=3600,
    interval=30,
    blocking=False,
    instrument_type=""
)

print(response_nonblocking.success, response_nonblocking.status_code, response_nonblocking.message)
```

---

This documentation covers the functions in your module and provides a clear understanding of their usage. Let me know if you need further assistance or additional details!

---

## request_types.py

### Part 1/3

Sure! Below is the detailed documentation for your `gotrade.request_types` module, including the necessary import statements and descriptions of each class with their methods.

### Module Documentation

#### Import Statements

```python
from typing import Optional, Dict, Any
```

---

### Class Documentation

#### `LoginResponse`
This class represents a response object after attempting to log in. It contains attributes indicating whether the login was successful and additional metadata like status code and message.

- **Attributes:**
  - `success (bool)`: A boolean value indicating if the login was successful.
  - `status_code (int)`: The HTTP status code of the request.
  - `message (str)`: An optional message describing the outcome of the login attempt.

---

#### `LoginRequest`
This class represents a login request to authenticate a user. It includes various fields necessary for authentication and an option to disable authentication if needed.

- **Attributes:**
  - `name (str)`: The name or identifier for the account.
  - `key (str)`: The API key associated with the account.
  - `secret (str)`: The secret required to authenticate the request.
  - `passphrase (str)`: An optional passphrase used alongside the API credentials.
  - `authenticate (bool, default=True)`: A flag indicating whether authentication should be performed.

- **Methods:**
  - `model_dump() -> Dict[str, Any]`: Returns a dictionary representation of the login request object suitable for serialization or logging.

---

#### `MarketOrderRequest`
This class represents a market order placed on an exchange. It includes basic information about the order and performs validation to ensure proper formatting and completeness.

- **Attributes:**
  - `exchange_name (str)`: The name of the exchange where the order is being placed.
  - `account_name (str)`: The name or identifier for the account placing the order.
  - `symbol (str)`: The trading pair symbol on which the market order will be executed.
  - `side (str)`: Indicates whether the trade is a 'BUY' or 'SELL'.
  - `quantity (float)`: The amount of currency to buy or sell.
  - `instrument_type (str, default="")`: An optional parameter used specifically for Bybit exchange.

- **Methods:**
  - `validate() -> tuple`: Validates the market order request. Returns a tuple where the first element indicates whether validation was successful, and the second provides an error message if there are issues.

---

#### `LimitOrderRequest`
This class represents a limit order placed on an exchange with specified price and quantity parameters. It performs similar validations to ensure proper formatting and completeness of the data provided.

- **Attributes:**
  - `exchange_name (str)`: The name of the exchange where the order is being placed.
  - `account_name (str)`: The name or identifier for the account placing the order.
  - `symbol (str)`: The trading pair symbol on which the limit order will be executed.
  - `side (str)`: Indicates whether the trade is a 'BUY' or 'SELL'.
  - `quantity (float)`: The amount of currency to buy or sell at the specified price.
  - `price (float)`: The price at which the order should be filled.
  - `instrument_type (str, default="")`: An optional parameter used specifically for Bybit exchange.

- **Methods:**
  - `validate() -> tuple`: Validates the limit order request. Returns a tuple where the first element indicates whether validation was successful, and the second provides an error message if there are issues.

---

### Example Usage

```python
# Creating a LoginRequest object
login_request = LoginRequest(name="user1", key="api_key", secret="secret_key")

# Serializing the login request to JSON format (example usage)
print(login_request.model_dump())

# Placing a market order on Bybit exchange
market_order = MarketOrderRequest(
    exchange_name="bybit",
    account_name="my_account",
    symbol="BTCUSD",
    side="BUY",
    quantity=0.1,
    instrument_type="linear"
)

is_valid, error_message = market_order.validate()
if is_valid:
    # Proceed with placing the order
else:
    print(f"Market Order Validation Error: {error_message}")

# Placing a limit order on Bybit exchange
limit_order = LimitOrderRequest(
    exchange_name="bybit",
    account_name="my_account",
    symbol="BTCUSD",
    side="BUY",
    quantity=0.1,
    price=25000.0,
    instrument_type="linear"
)

is_valid, error_message = limit_order.validate()
if is_valid:
    # Proceed with placing the order
else:
    print(f"Limit Order Validation Error: {error_message}")
```

This documentation should help in understanding and using these classes effectively within your codebase or project.

### Part 2/3

Certainly! Below is the documentation for the `gotrade.request_types` module, including import statements, class descriptions, and method details based on your provided code.

### Module Documentation

**Module**: `gotrade.request_types`

This module contains classes that define request types used by the GoTrade system to handle order requests across different exchanges. These include generic order requests and specific requests for Bybit exchange.

#### Imports
```python
from typing import Dict, Any, Optional, Tuple
```

### Classes

#### Class: `OrderResponse`
Represents a response object containing details of an order request status.

**Attributes**:
- `success (bool)`: Indicates if the operation was successful.
- `status_code (int)`: HTTP or system-specific code indicating success/error.
- `message (str)`: Descriptive message for the result.
- `response_data (Optional[Dict[str, Any]])`: Optional data associated with the response.

**Constructor**:
```python
OrderResponse(success: bool, status_code: int, message: str, response_data: Optional[Dict[str, Any]] = None)
```

#### Class: `TWAPOrderRequest`
Represents an order request for Time-Weighted Average Price (TWAP) trading strategy.

**Attributes**:
- `exchange_name (str)`: Name of the exchange.
- `account_name (str)`: Account name on the exchange.
- `symbol (str)`: Trading symbol.
- `side (str)`: 'BUY' or 'SELL'.
- `quantity (float)`: Quantity to trade.
- `duration (int)`: Duration in minutes for TWAP execution.
- `interval (int)`: Interval in seconds between trades.
- `instrument_type (Optional[str])`: Optional instrument type required for Bybit.

**Constructor**:
```python
TWAPOrderRequest(exchange_name: str, account_name: str, symbol: str, side: str, quantity: float, duration: int, interval: int, instrument_type: Optional[str] = "")
```

**Method**: `validate()`
Validates the order request parameters. Returns a tuple `(success: bool, message: str)` indicating validation success and any error messages.

```python
def validate(self) -> Tuple[bool, str]:
    pass
```

#### Class: `MarketEdgeOrderRequest`
Represents an order request for Market Edge trading strategy.

**Attributes**:
- `exchange_name (str)`: Name of the exchange.
- `account_name (str)`: Account name on the exchange.
- `symbol (str)`: Trading symbol.
- `side (str)`: 'BUY' or 'SELL'.
- `quantity (float)`: Quantity to trade.
- `max_timer (int)`: Maximum timer for edge trading execution.
- `instrument_type (Optional[str])`: Optional instrument type required for Bybit.

**Constructor**:
```python
MarketEdgeOrderRequest(exchange_name: str, account_name: str, symbol: str, side: str, quantity: float, max_timer: int, instrument_type: Optional[str] = "")
```

**Method**: `validate()`
Validates the order request parameters. Returns a tuple `(success: bool, message: str)` indicating validation success and any error messages.

```python
def validate(self) -> Tuple[bool, str]:
    pass
```

#### Class: `TwapEdgeOrderRequest`
Represents an order request for Time-Weighted Average Price Edge trading strategy (incomplete in the provided code).

**Attributes**:
- `exchange_name (str)`
- `account_name (str)`
- `symbol (str)`
- `side (str)`
- `quantity (float)`
- `max_timer (int)`
- `instrument_type (Optional[str])`

**Constructor**: (Incomplete)
```python
TwapEdgeOrderRequest(exchange_name: str, account_name: str, symbol: str, side: str, quantity: float, max_timer: int, instrument_type: Optional[str] = "")
```

**Method**: `validate()`
Validates the order request parameters. Returns a tuple `(success: bool, message: str)` indicating validation success and any error messages.

```python
def validate(self) -> Tuple[bool, str]:
    pass
```

### Example Usage

Below is an example of how to use these classes:

```python
from gotrade.request_types import TWAPOrderRequest, OrderResponse

# Create a TWAP order request
order_request = TWAPOrderRequest(
    exchange_name="bybit",
    account_name="alice",
    symbol="BTCUSD",
    side="BUY",
    quantity=1.0,
    duration=60,
    interval=5,
    instrument_type="futures"
)

# Validate the order request
is_valid, message = order_request.validate()
if is_valid:
    # Proceed with the operation and get a response
    order_response = OrderResponse(success=True, status_code=200, message="Order successful", response_data={"orderId": 12345})
else:
    print(message)  # Handle validation failure
```

This documentation covers all necessary aspects of the provided code. If you need further details or additional classes to be added, please let me know!

### Part 3/3

Sure! Below is an example of how you could document your code in Python's docstring format, including the required imports based on the provided information.

### Module Documentation

```python
"""
Module to handle request types used by Gotrade API.

This module contains classes and functions necessary for handling various trade requests.
"""

# Import statements
from gotrade.request_types import RequestType  # Assuming this is a base class or interface

```

### Class Documentation

```python
class TradeRequest:
    """
    Represents a trading request for the Gotrade API.

    Attributes:
        exchange_name (str): Name of the exchange in lowercase.
        account_name (str): Name of the account associated with the trade.
        symbol (str): Trading pair or market identifier.
        side (str): Direction of the trade, either 'BUY' or 'SELL'.
        quantity (float): Quantity of the asset to be traded.
        duration (int): Duration in seconds for which the order is valid.
        interval (int): Interval between execution attempts if not immediate.
        instrument_type (str, optional): Type of financial instrument. Required by Bybit only.

    Methods:
        validate: Validates all attributes and ensures they meet the necessary criteria.
    """

    def __init__(self,
                 exchange_name: str,
                 account_name: str,
                 symbol: str,
                 side: str,
                 quantity: float,
                 duration: int,
                 interval: int,
                 instrument_type: str = ""):
        """
        Initializes a new instance of the TradeRequest class.

        :param exchange_name (str): Name of the exchange in lowercase.
        :param account_name (str): Name of the trading account.
        :param symbol (str): Trading pair or market identifier.
        :param side (str): Direction of the trade. Valid values are 'BUY' and 'SELL'.
        :param quantity (float): Quantity to be traded, must be a positive number.
        :param duration (int): Duration in seconds for which the order is valid, must be a positive integer.
        :param interval (int): Interval between execution attempts if not immediate, must be a positive integer.
        :param instrument_type (str, optional): Type of financial instrument. Required by Bybit only.
        """
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.duration = duration
        self.interval = interval
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
        """
        Validates the attributes of the trade request.

        Checks for missing fields, correctness of data types and values.
        
        :return: A tuple containing a boolean indicating if validation succeeded or failed,
                 along with an error message (if any).
        """
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, self.quantity, self.duration, self.interval]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity, duration, interval"

        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"

        if not isinstance(self.duration, int) or self.duration <= 0:
            return False, "Duration must be a positive integer"

        if not isinstance(self.interval, int) or self.interval <= 0:
            return False, "Interval must be a positive integer"

        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"

        # Bybit-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"

        return True, ""
```

This documentation ensures that anyone reading it will have a clear understanding of what the `TradeRequest` class does, its attributes, and how to use its methods.

---

## exchanges\bybit.py

### Part 1/3

Certainly! Below is the documentation for the `gotrade.exchanges.bybit` module, which includes import statements based on your provided code snippet and detailed function descriptions.

### Module Documentation: gotrade.exchanges.bybit

#### Imports:
```python
from dotenv import load_dotenv  # For loading environment variables from a .env file
from ..oems_operations import (  # Importing functions for interacting with the exchange
    login_to_exchange, 
    place_market_order,
    place_limit_order,
    place_market_edge_order,
    place_twap_order,
    place_twap_edge_order
)
```

#### Functions:

##### `login(exchange_name=None, account_name=None, key=None, secret=None, passphrase="", authenticate=True) -> bool`
- **Description**: This function logs into the exchange using provided credentials or environment variables.
- **Parameters**:
  - `exchange_name`: Name of the exchange to log in (default: "bybit")
  - `account_name`: Account name associated with the API key
  - `key`: API key for authentication (optional, can be loaded from environment variable)
  - `secret`: Secret used for signing requests (optional, can be loaded from environment variable)
  - `passphrase`: Passphrase for additional security (default: "")
  - `authenticate`: Flag indicating whether to authenticate the login request (default: True)
- **Returns**: A boolean value indicating if the login was successful.
  
##### Example Usage:
```python
is_logged_in = login(authenticate=True)  # Use environment variables for credentials
```

---

##### `market_order(exchange_name=None, account_name=None, symbol=None, side=None, quantity=None, blocking=True, instrument_type=None) -> bool`
- **Description**: This function places a market order on the exchange.
- **Parameters**:
  - `exchange_name`: Name of the exchange (default: "bybit")
  - `account_name`: Account name associated with the API key
  - `symbol`: Trading symbol (e.g., "EOSUSDT")
  - `side`: Order side ("buy" or "sell")
  - `quantity`: Quantity of asset to buy/sell
  - `blocking`: Whether the order should block execution (default: True)
  - `instrument_type`: Type of instrument (e.g., "SPOT", "PERPETUAL", "LINEAR")
- **Returns**: A boolean value indicating if the market order was successfully placed.
  
##### Example Usage:
```python
order_result = market_order(symbol="EOSUSDT", side="buy", quantity=10, blocking=True)
```

---

##### `limit_order(exchange_name=None, account_name=None, symbol=None, side=None, quantity=None, price=None, blocking=True, instrument_type=None) -> bool`
- **Description**: This function places a limit order on the exchange.
- **Parameters**:
  - `exchange_name`: Name of the exchange (default: "bybit")
  - `account_name`: Account name associated with the API key
  - `symbol`: Trading symbol (e.g., "DOTUSDT")
  - `side`: Order side ("buy" or "sell")
  - `quantity`: Quantity of asset to buy/sell
  - `price`: Price at which to place the limit order
  - `blocking`: Whether the order should block execution (default: True)
  - `instrument_type`: Type of instrument (e.g., "SPOT", "PERPETUAL", "LINEAR")
- **Returns**: A boolean value indicating if the limit order was successfully placed.

##### Example Usage:
```python
order_result = limit_order(symbol="DOTUSDT", side="buy", quantity=10, price=20.50, blocking=True)
```

---

This documentation should provide a clear overview of how to use each function in your `gotrade.exchanges.bybit` module. If you have more functions or additional details that need to be included, let me know!

### Part 2/3

Certainly! Below is the detailed documentation for the `gotrade.exchanges.bybit` module, including the necessary import statements and function descriptions with their parameters.

### Module Documentation: gotrade.exchanges.bybit

#### Import Statements:
```python
from gotrade.exchanges.bybit import market_edge_order, twap_order, twap_edge_order
```

---

### Functions:

#### `market_edge_order`
Placed a market edge order on the Bybit exchange.

**Signature:**  
`def market_edge_order(exchange_name=None, account_name=None, symbol=None, side=None, quantity=None, max_timer=None, blocking=True, instrument_type=None) -> bool:`

**Parameters:**
- **exchange_name (str):** Name of the exchange where the order will be placed. Default value is 'bybit'.
- **account_name (str):** Account name to use for placing the order, fetched from environment variables.
- **symbol (str):** Trading symbol on which the order should be executed (e.g., "ETHUSDT").
- **side (str):** The side of the order: either 'buy' or 'sell'.
- **quantity (float):** The quantity of the asset to buy/sell.
- **max_timer (int, optional):** Maximum timer for the edge order. Default value is None.
- **blocking (bool):** Whether the function should block while waiting for the order execution response. Default value is True.
- **instrument_type (str, optional):** Type of instrument: "SPOT", "PERPETUAL", "LINEAR". Default value is None.

**Returns:**  
`bool:` Returns `True` if the order was successfully placed; otherwise returns `False`.

---

#### `twap_order`
Placed a TWAP (Time Weighted Average Price) order on the Bybit exchange.

**Signature:**  
`def twap_order(exchange_name=None, account_name=None, symbol=None, side=None, quantity=None, duration=None, interval=None, blocking=True, instrument_type=None) -> bool:`

**Parameters:**
- **exchange_name (str):** Name of the exchange where the order will be placed. Default value is 'bybit'.
- **account_name (str):** Account name to use for placing the order, fetched from environment variables.
- **symbol (str):** Trading symbol on which the order should be executed (e.g., "DOTUSDT").
- **side (str):** The side of the order: either 'buy' or 'sell'.
- **quantity (float):** Total quantity of the asset to buy/sell.
- **duration (int):** Duration of the TWAP order in seconds.
- **interval (int):** Interval between executions in seconds.
- **blocking (bool):** Whether the function should block while waiting for the order execution response. Default value is True.
- **instrument_type (str, optional):** Type of instrument: "SPOT", "PERPETUAL", "LINEAR". Default value is None.

**Returns:**  
`bool:` Returns `True` if the order was successfully placed; otherwise returns `False`.

---

#### `twap_edge_order`
Placed a TWAP edge order on the Bybit exchange.

**Signature:**  
`def twap_edge_order(exchange_name=None, account_name=None, symbol=None, side=None, quantity=None, duration=None, interval=None, blocking=True, instrument_type=None) -> bool:`

**Parameters:**
- **exchange_name (str):** Name of the exchange where the order will be placed. Default value is 'bybit'.
- **account_name (str):** Account name to use for placing the order, fetched from environment variables.
- **symbol (str):** Trading symbol on which the order should be executed (e.g., "BTCUSDT").
- **side (str):** The side of the order: either 'buy' or 'sell'.
- **quantity (float):** Total quantity of the asset to buy/sell.
- **duration (int):** Duration of the TWAP order in seconds.
- **interval (int):** Interval between executions in seconds.
- **blocking (bool):** Whether the function should block while waiting for the order execution response. Default value is True.
- **instrument_type (str, optional):** Type of instrument: "SPOT", "PERPETUAL", "LINEAR". Default value is None.

**Returns:**  
`bool:` Returns `True` if the order was successfully placed; otherwise returns `False`.

---

This documentation provides a clear and concise description of each function along with its parameters, which should be useful for other developers working on this code.

### Part 3/3

Sure, I can help you document your code properly. Let's start by creating an informative docstring at the beginning of your module and then adding appropriate documentation to each function.

Given your provided snippet is part of a larger context, let’s assume there are functions already defined that use this snippet as a part of their functionality. Here’s how we can document it:

### Module Documentation

First, you need to define an import statement at the top of your module file (assuming `submodules.txt` contains relevant sub-modules).

```python
"""
Module: gotrade.exchanges.bybit

This module provides functions for trading on Bybit exchange.

Submodule Imports:
    - gotrade.base.exceptions
    - gotrade.models.order

"""

from gotrade.base import exceptions  # Assuming this is in submodules.txt
from gotrade.models import order as go_order  # Assuming 'order' is mentioned in submodules.txt
```

### Function Documentation

Now, let's document the specific function containing your provided code snippet. Here’s an example of how you can write documentation for a function:

```python
def place_order(order_details):
    """
    Places an order on Bybit exchange.

    Parameters:
        order_details (go_order.OrderDetails): An instance of OrderDetails that contains all necessary details to place an order.

    Returns:
        bool: True if the order was successfully placed, False otherwise.
    
    Raises:
        exceptions.APIError: If there is an error with the API request or response.
        
    Example Usage:
        >>> result = place_order(go_order.OrderDetails(symbol="BTCUSD", side="Buy", size=10))
        >>> print(result)
        True
    """
    try:
        # Function logic here...
        
        # Assuming 'result' is an instance of some class that provides the message and success status.
        print(f"Message: {result.message}")

        return result.success

    except exceptions.APIError as e:
        raise e
```

### Explanation:

1. **Module Docstring**: It describes what the module does, lists necessary imports, and possibly includes any caveats or dependencies.

2. **Function Documentation**:
   - **Parameters Section**: Specifies all input parameters with their types and descriptions.
   - **Returns Section**: Describes the return value(s) of the function.
   - **Raises Section**: Indicates exceptions that can be raised from this function.
   - **Example Usage**: Shows how to use the function, including an example output.

Make sure to replace `place_order`, `order_details`, and other names with actual existing function and parameter names in your module if they differ. This documentation style should adhere closely to any existing coding standards or guidelines provided by your project.

---

## exchanges\okx.py

### Part 1/2

Certainly! Below is an example of how you can document the code in your `okx` module within the `gotrade.exchanges` package. I'll include descriptions and parameter details for each function, following a standard documentation format.

```markdown
# Module: gotrade.exchanges.okx

This module provides functions to interact with OKX exchange using various trading operations like logging in, placing different types of orders, etc.

## Imports

```python
from dotenv import load_dotenv
from ..oems_operations import (
    login_to_exchange,
    place_market_order,
    place_limit_order,
    place_market_edge_order,
    place_twap_order,
    place_twap_edge_order
)
```

## Functions

### `login() -> bool`
Logs into the OKX exchange.

#### Parameters:
- None (uses environment variables for credentials).

#### Returns:
- `bool`: True if login is successful, False otherwise.

#### Example Usage:
```python
success = login()
if success:
    print("Login was successful.")
else:
    print("Failed to log in.")
```

### `market_order(symbol=None, side=None, quantity=None, blocking=True) -> bool`
Places a market order on the OKX exchange.

#### Parameters:
- `symbol` (str): The trading pair symbol.
- `side` (str): "buy" or "sell".
- `quantity` (float): Quantity to buy or sell.
- `blocking` (bool, optional): Whether to block until the order is complete. Default is True.

#### Returns:
- `bool`: True if the market order was successfully placed, False otherwise.

#### Example Usage:
```python
success = market_order(symbol="DOT-USDT-SWAP", side="buy", quantity=10)
if success:
    print("Market order was successful.")
else:
    print("Failed to place market order.")
```

### `limit_order(symbol=None, side=None, quantity=None, price=None, blocking=True) -> bool`
Places a limit order on the OKX exchange.

#### Parameters:
- `symbol` (str): The trading pair symbol.
- `side` (str): "buy" or "sell".
- `quantity` (float): Quantity to buy or sell.
- `price` (float): The price at which the order should be placed.
- `blocking` (bool, optional): Whether to block until the order is complete. Default is True.

#### Returns:
- `bool`: True if the limit order was successfully placed, False otherwise.

#### Example Usage:
```python
success = limit_order(symbol="DOT-USDT-SWAP", side="buy", quantity=10, price=5)
if success:
    print("Limit order was successful.")
else:
    print("Failed to place limit order.")
```

### `market_edge_order(symbol=None, side=None, quantity=None, max_timer=None, blocking=True) -> bool`
Places a market edge order on the OKX exchange.

#### Parameters:
- `symbol` (str): The trading pair symbol.
- `side` (str): "buy" or "sell".
- `quantity` (float): Quantity to buy or sell.
- `max_timer` (int, optional): Maximum time to wait for the order to be filled in milliseconds. Default is 1000 ms.
- `blocking` (bool, optional): Whether to block until the order is complete. Default is True.

#### Returns:
- `bool`: True if the market edge order was successfully placed, False otherwise.

#### Example Usage:
```python
success = market_edge_order(symbol="DOT-USDT-SWAP", side="buy", quantity=10, max_timer=2000)
if success:
    print("Market edge order was successful.")
else:
    print("Failed to place market edge order.")
```

### `twap_order() -> bool`
Places a Time-Weighted Average Price (TWAP) order on the OKX exchange.

#### Parameters:
- None (parameters are specified within function).

#### Returns:
- `bool`: True if the TWAP order was successfully placed, False otherwise.

#### Example Usage:
```python
# Assuming parameters are provided within twap_order function implementation.
success = twap_order()
if success:
    print("TWAP order was successful.")
else:
    print("Failed to place TWAP order.")
```

### `twap_edge_order() -> bool`
Places a Time-Weighted Average Price Edge (TWAP) order on the OKX exchange.

#### Parameters:
- None (parameters are specified within function).

#### Returns:
- `bool`: True if the TWAP edge order was successfully placed, False otherwise.

#### Example Usage:
```python
# Assuming parameters are provided within twap_edge_order function implementation.
success = twap_edge_order()
if success:
    print("TWAP Edge order was successful.")
else:
    print("Failed to place TWAP Edge order.")
```

---

This documentation provides a clear and concise guide on how to use the various functions in your `okx` module. Ensure that you provide similar detailed descriptions for all the methods, including any additional parameters or specific notes for each function.
```

### Part 2/2

Certainly! Below is a sample documentation for the `gotrade.exchanges.okx` module, including import statements based on typical structure and function details you've provided:

### Module Documentation: `gotrade.exchanges.okx`

#### Overview:
This module contains functions to place Time-Weighted Average Price (TWAP) orders and TWAP edge orders on OKX exchange.

#### Import Statements:
```python
from gotrade import utils  # Assuming a generic utility module that might be used.
from gotrade.exceptions import APIError, AuthenticationError  # Example error handling imports
```

If `submodules.txt` specifies the structure of your project and dependencies, make sure to adjust these based on actual paths within the project.

#### Functions:

1. **twap_order()**
   Places a TWAP order on OKX exchange.
   
   - **Parameters:**
     - `symbol` (str): Trading symbol for which the order is placed.
     - `side` (str): 'buy' or 'sell'.
     - `quantity` (float, int): Quantity of base asset to trade.
     - `duration` (int): Total duration of the TWAP order in seconds.
     - `interval` (int): Interval between executions in seconds.
     - `blocking` (bool, optional): If set to True, function will block until the order is placed. Default is True.
     
   - **Returns:**
     - bool: Returns True if the order was successfully placed.

2. **twap_edge_order()**
   Places a TWAP edge order on OKX exchange.
   
   - **Parameters:**
     - `symbol` (str): Trading symbol for which the order is placed.
     - `side` (str): 'buy' or 'sell'.
     - `quantity` (float, int): Quantity of base asset to trade.
     - `duration` (int): Total duration of the TWAP edge order in seconds.
     - `interval` (int): Interval between executions in seconds.
     - `blocking` (bool, optional): If set to True, function will block until the order is placed. Default is True.
     
   - **Returns:**
     - bool: Returns True if the order was successfully placed.

#### Example Usage:
```python
# Import necessary functions from the module
from gotrade.exchanges.okx import twap_order

# Example of placing a TWAP order
success = twap_order(symbol='BTC-USDT', side='buy', quantity=1, duration=3600, interval=60)
print(f"TWAP Order Success: {success}")

# Importing the second function for example usage
from gotrade.exchanges.okx import twap_edge_order

# Example of placing a TWAP Edge order
success = twap_edge_order(symbol='BTC-USDT', side='buy', quantity=1, duration=3600, interval=60)
print(f"TWAP Edge Order Success: {success}")
```

#### Error Handling:
- The `APIError` and `AuthenticationError` exceptions should be caught to handle errors appropriately. These are assumed to come from a common error handling module (`gotrade.exceptions`) for consistency across the project.

Make sure to replace paths in import statements with actual ones if your `submodules.txt` specifies different paths or additional sub-modules that need importing.

---

