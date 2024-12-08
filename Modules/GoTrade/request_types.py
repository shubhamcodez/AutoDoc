from typing import Optional, Dict, Any
        
class LoginResponse:
    def __init__(
        self,
        success: bool,
        status_code: int,
        message: str
    ):
        self.success = success
        self.status_code = status_code
        self.message = message

class LoginRequest:
    def __init__(self, 
                 name: str,
                 key: str, 
                 secret: str, 
                 passphrase: str,
                 authenticate: bool = True):
        self.name = name
        self.key = key
        self.secret = secret
        self.passphrase = passphrase
        self.authenticate = authenticate
    
    def model_dump(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "key": self.key,
            "secret": self.secret,
            "passphrase": self.passphrase,
            "authenticate": self.authenticate
        }

class MarketOrderRequest:
    def __init__(self,
                 exchange_name: str,
                 account_name: str,
                 symbol: str,
                 side: str,
                 quantity: float,
                 instrument_type: str = ""):
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.instrument_type = instrument_type

    def validate(self) -> tuple:  # Python 3.6 compatible tuple return
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, self.quantity]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity"
        
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"
        
        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"
            
        # Bybit-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"
            
        return True, ""

class LimitOrderRequest:
    def __init__(self,
                 exchange_name: str,
                 account_name: str,
                 symbol: str,
                 side: str,
                 quantity: float,
                 price: float,
                 instrument_type: str = ""):
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.price = price
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, self.quantity, self.price]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity, price"
        
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"
            
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            return False, "Price must be a positive number"
        
        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"
            
        # Bybit-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"
            
        return True, ""

class OrderResponse:
    def __init__(
        self,
        success: bool,
        status_code: int,
        message: str,
        response_data: Optional[Dict[str, Any]] = None
    ):
        self.success = success
        self.status_code = status_code
        self.message = message
        self.response_data = response_data

class TWAPOrderRequest:
    def __init__(self,
                 exchange_name: str,
                 account_name: str,
                 symbol: str,
                 side: str,
                 quantity: float,
                 duration: int,
                 interval: int,
                 instrument_type: str = ""):
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.duration = duration
        self.interval = interval
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
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


class MarketEdgeOrderRequest:
    def __init__(self,
                 exchange_name: str,
                 account_name: str,
                 symbol: str,
                 side: str,
                 quantity: float,
                 max_timer: int,
                 instrument_type: str = ""):
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.max_timer = max_timer
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
        if not all([self.exchange_name, self.account_name, self.symbol, self.side, self.quantity, self.max_timer]):
            return False, "Missing required fields: exchange_name, account_name, symbol, side, quantity, max_timer"

        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False, "Quantity must be a positive number"

        if not isinstance(self.max_timer, int) or self.max_timer <= 0:
            return False, "Max timer must be a positive integer"

        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be 'BUY' or 'SELL'"

        # Bybit-specific validation
        if self.exchange_name == "bybit" and not self.instrument_type:
            return False, "instrument_type is required for Bybit"
        elif self.exchange_name != "bybit" and self.instrument_type:
            return False, f"instrument_type is not supported for {self.exchange_name}"

        return True, ""
class TwapEdgeOrderRequest:
    def __init__(self,
                 exchange_name: str,
                 account_name: str,
                 symbol: str,
                 side: str,
                 quantity: float,
                 duration: int,
                 interval: int,
                 instrument_type: str = ""):
        self.exchange_name = exchange_name.lower()
        self.account_name = account_name
        self.symbol = symbol
        self.side = side.upper()
        self.quantity = quantity
        self.duration = duration
        self.interval = interval
        self.instrument_type = instrument_type

    def validate(self) -> tuple:
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
