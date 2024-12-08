from typing import Optional, Dict, Any

# Response class for login operations
class LoginResponse:
    def __init__(
        self,
        success: bool,        # Indicates if the login attempt was successful
        status_code: int,     # HTTP status code or custom status code
        message: str          # Descriptive message about the login result
    ):
        self.success = success
        self.status_code = status_code
        self.message = message

# Request class for login operations
class LoginRequest:
    def __init__(self, 
                 name: str,           # Account/user identifier
                 key: str,            # API key for authentication
                 secret: str,         # API secret for authentication
                 passphrase: str,     # Additional security passphrase
                 authenticate: bool = True):  # Flag to control authentication process
        self.name = name
        self.key = key
        self.secret = secret
        self.passphrase = passphrase
        self.authenticate = authenticate
    
    def model_dump(self) -> Dict[str, Any]:
        """
        Converts the request object to a dictionary format
        Returns: Dictionary containing all request parameters
        """
        return {
            "name": self.name,
            "key": self.key,
            "secret": self.secret,
            "passphrase": self.passphrase,
            "authenticate": self.authenticate
        }

# Request class for market orders (immediate execution at market price)
class MarketOrderRequest:
    def __init__(self,
                 exchange_name: str,      # Name of the target exchange (e.g., "binance", "bybit")
                 account_name: str,       # Trading account identifier
                 symbol: str,             # Trading pair symbol (e.g., "BTCUSDT")
                 side: str,               # Order side ("BUY" or "SELL")
                 quantity: float,         # Order quantity
                 instrument_type: str = ""):  # Instrument type (required for Bybit)
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
        """
        Validates the market order request parameters
        Returns: Tuple of (success: bool, error_message: str)
        """
        # Check for required fields
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, self.quantity]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity"
        
        # Validate quantity
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"
        
        # Validate order side
        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"
            
        # Exchange-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"
            
        return True, ""

# Request class for Take Profit/Stop Loss orders
class TPSLOrderRequest:
    def __init__(self,
                 exchange_name: str,        # Name of the target exchange
                 account_name: str,         # Trading account identifier
                 symbol: str,               # Trading pair symbol
                 side: str,                 # Order side ("BUY" or "SELL")
                 quantity: float,           # Order quantity
                 tp_percentage: float,      # Take profit trigger percentage
                 sl_percentage: float,      # Stop loss trigger percentage
                 instrument_type: str = ""): # Instrument type (required for Bybit)
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.tp_percentage = tp_percentage
        self.sl_percentage = sl_percentage
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
        """
        Validates Take Profit/Stop Loss order parameters
        Returns: Tuple of (success: bool, error_message: str)
        """
        # Check for required fields
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, 
                   self.quantity, self.tp_percentage, self.sl_percentage]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity, tp_percentage, sl_percentage"

        # Validate numeric parameters
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"

        if not isinstance(self.tp_percentage, (int, float)):
            return False, "Take profit percentage must be a number"

        if not isinstance(self.sl_percentage, (int, float)):
            return False, "Stop loss percentage must be a number"

        if self.tp_percentage <= 0:
            return False, "Take profit percentage must be positive"

        if self.sl_percentage <= 0:
            return False, "Stop loss percentage must be positive"

        # Validate order side
        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"

        # Exchange-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"

        return True, ""

# Generic Cancel Order Request
class CancelOrderRequest:
    def __init__(self,
                 exchange_name: str,      # Name of the target exchange
                 account_name: str,       # Trading account identifier
                 symbol: str,             # Trading pair symbol
                 order_id: str,           # Unique order identifier to cancel
                 instrument_type: str = ""): # Instrument type (required for Bybit)
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.order_id = order_id
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
        """
        Validates cancel order request parameters
        Returns: Tuple of (success: bool, error_message: str)
        """
        if not all([self.exchange_name, self.account_name, self.symbol, self.order_id]):
            return False, "Missing required fields: exchange_name, account_name, symbol, order_id"

        # Exchange-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"

        return True, ""

# Modify Order Request
class ModifyOrderRequest:
    def __init__(self,
                 exchange_name: str,      # Name of the target exchange
                 account_name: str,       # Trading account identifier
                 symbol: str,             # Trading pair symbol
                 order_id: str,           # Order ID to modify
                 new_price: float,        # New price for the order
                 new_quantity: float,     # New quantity for the order
                 instrument_type: str = ""): # Instrument type (required for Bybit)
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.order_id = order_id
        self.new_price = new_price
        self.new_quantity = new_quantity
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
        """
        Validates modify order request parameters
        Returns: Tuple of (success: bool, error_message: str)
        """
        if not all([self.exchange_name, self.account_name, self.symbol, self.order_id]):
            return False, "Missing required fields: exchange_name, account_name, symbol, order_id"

        # Validate numeric parameters
        if self.new_price is not None:
            if not isinstance(self.new_price, (int, float)) or self.new_price <= 0:
                return False, "New price must be a positive number"

        if self.new_quantity is not None:
            if not isinstance(self.new_quantity, (int, float)) or self.new_quantity <= 0:
                return False, "New quantity must be a positive number"

        # Exchange-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"

        return True, ""

# Request class for limit orders (orders with specific price)
class LimitOrderRequest:
    def __init__(self,
                 exchange_name: str,      # Name of the target exchange
                 account_name: str,       # Trading account identifier
                 symbol: str,             # Trading pair symbol
                 side: str,               # Order side ("BUY" or "SELL")
                 quantity: float,         # Order quantity
                 price: float,            # Limit price for the order
                 instrument_type: str = ""):  # Instrument type (required for Bybit)
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.price = price
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
        """
        Validates the limit order request parameters
        Returns: Tuple of (success: bool, error_message: str)
        """
        # Check for required fields
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, self.quantity, self.price]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity, price"
        
        # Validate quantity and price
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"
            
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            return False, "Price must be a positive number"
        
        # Validate order side
        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"
            
        # Exchange-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"
            
        return True, ""

# Generic response class for order operations
class OrderResponse:
    def __init__(
        self,
        success: bool,         # Indicates if the order operation was successful
        status_code: int,      # Status code of the operation
        message: str,          # Descriptive message about the result
        response_data: Optional[Dict[str, Any]] = None  # Additional response data
    ):
        self.success = success
        self.status_code = status_code
        self.message = message
        self.response_data = response_data

# Request class for Time-Weighted Average Price (TWAP) orders
class TWAPOrderRequest:
    def __init__(self,
                 exchange_name: str,      # Name of the target exchange
                 account_name: str,       # Trading account identifier
                 symbol: str,             # Trading pair symbol
                 side: str,               # Order side ("BUY" or "SELL")
                 quantity: float,         # Total order quantity
                 duration: int,           # Total duration for execution (seconds)
                 interval: int,           # Time between each partial order (seconds)
                 instrument_type: str = ""):  # Instrument type (required for Bybit)
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
        Validates TWAP order parameters
        Returns: Tuple of (success: bool, error_message: str)
        """
        # Check for required fields
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, 
                   self.quantity, self.duration, self.interval]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity, duration, interval"
        
        # Validate numeric parameters
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"
        
        if not isinstance(self.duration, int) or self.duration <= 0:
            return False, "Duration must be a positive integer"
        
        if not isinstance(self.interval, int) or self.interval <= 0:
            return False, "Interval must be a positive integer"
        
        # Validate order side
        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"
        
        # Exchange-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"
        
        return True, ""

# Request class for Market Edge algorithm orders
class MarketEdgeOrderRequest:
    def __init__(self,
                 exchange_name: str,      # Name of the target exchange
                 account_name: str,       # Trading account identifier
                 symbol: str,             # Trading pair symbol
                 side: str,               # Order side ("BUY" or "SELL")
                 quantity: float,         # Order quantity
                 max_timer: int,          # Maximum time for order execution (seconds)
                 instrument_type: str = ""):  # Instrument type (required for Bybit)
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.max_timer = max_timer
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
        """
        Validates Market Edge order parameters
        Returns: Tuple of (success: bool, error_message: str)
        """
        # Check for required fields
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, 
                   self.quantity, self.max_timer]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity, max_timer"

        # Validate numeric parameters
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"

        if not isinstance(self.max_timer, int) or self.max_timer <= 0:
            return False, "Max timer must be a positive integer"

        # Validate order side
        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"

        # Exchange-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"

        return True, ""

# Request class for TWAP Edge algorithm orders (combines TWAP and Edge strategies)
class TwapEdgeOrderRequest:
    def __init__(self,
                 exchange_name: str,      # Name of the target exchange
                 account_name: str,       # Trading account identifier
                 symbol: str,             # Trading pair symbol
                 side: str,               # Order side ("BUY" or "SELL")
                 quantity: float,         # Total order quantity
                 duration: int,           # Total duration for execution (seconds)
                 interval: int,           # Time between each partial order (seconds)
                 instrument_type: str = ""):  # Instrument type (required for Bybit)
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
        Validates TWAP Edge order parameters
        Returns: Tuple of (success: bool, error_message: str)
        """
        # Check for required fields
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, 
                   self.quantity, self.duration, self.interval]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity, duration, interval"

        # Validate numeric parameters
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"

        if not isinstance(self.duration, int) or self.duration <= 0:
            return False, "Duration must be a positive integer"

        if not isinstance(self.interval, int) or self.interval <= 0:
            return False, "Interval must be a positive integer"

        # Validate order side
        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"

        # Exchange-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"

        return True, ""