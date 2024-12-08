import sys
# Adding the parent directory to sys.path to import modules from there
sys.path.append("..")
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
# Import functions from oems_operations module for interacting with exchange
from ..oems_operations import (
    login_to_exchange, place_market_order, place_limit_order, 
    place_market_edge_order, place_twap_order, place_twap_edge_order
)

# Login function to authenticate with the exchange
def login(exchange_name=None, account_name=None, key=None, 
         secret=None, passphrase="", authenticate=True) -> bool:
    # Attempt to login using credentials from environment variables
    result = login_to_exchange(
        exchange_name="bybit",  # Exchange name
        account_name=os.getenv('BYBIT_ACCOUNT'),  # Fetch account name from environment variables
        key=os.getenv('BYBIT_API_KEY'),  # Fetch API key from environment variables
        secret=os.getenv('BYBIT_SECRET'),  # Fetch API secret from environment variables
        passphrase=os.getenv('BYBIT_PASSPHRASE'),  # Fetch passphrase from environment variables
        authenticate=True  # Flag to authenticate the login request
    )
    
    # Print the login response for debugging purposes
    print("=== Login Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")
    
    # Return True if the login was successful, else return False
    return result.message == "OK" and result.status_code == 0

# Function to place a market order on the exchange
def market_order(exchange_name=None, account_name=None, symbol=None, 
                side=None, quantity=None, blocking=True,
                instrument_type=None) -> bool:
    # Call place_market_order function to execute a market order
    result = place_market_order(
        exchange_name='bybit',  # Specify exchange name
        account_name=os.getenv('BYBIT_ACCOUNT'),  # Fetch account name from environment variables
        symbol=symbol,  # The trading symbol (e.g., "EOSUSDT")
        side=side,  # The side of the order: "buy" or "sell"
        quantity=quantity,  # The quantity of the asset to buy/sell
        blocking=blocking,  # Whether the order should block the execution
        instrument_type=instrument_type  # Type of instrument: "SPOT", "PERPETUAL", "LINEAR", etc.
    )
    
    # Print the response from the order placement attempt for debugging purposes
    print("=== Market Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")
    
    # Return True if the order was successfully placed, else return False
    return result.success

# Function to place a limit order on the exchange
def limit_order(exchange_name=None, account_name=None, symbol=None, 
               side=None, quantity=None, price=None, blocking=True,
               instrument_type=None) -> bool:
    # Call place_limit_order function to execute a limit order
    result = place_limit_order(
        exchange_name='bybit',  # Specify exchange name
        account_name=os.getenv('BYBIT_ACCOUNT'),  # Fetch account name from environment variables
        symbol=symbol,  # The trading symbol (e.g., "DOTUSDT")
        side=side,  # The side of the order: "buy" or "sell"
        quantity=quantity,  # The quantity of the asset to buy/sell
        price=price,  # The price at which to place the limit order
        blocking=blocking,  # Whether the order should block the execution
        instrument_type=instrument_type  # Type of instrument: "SPOT", "PERPETUAL", "LINEAR", etc.
    )
    
    # Print the response from the order placement attempt for debugging purposes
    print("=== Limit Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")
    
    # Return True if the order was successfully placed, else return False
    return result.success

# Function to place a market edge order on the exchange
def market_edge_order(exchange_name=None, account_name=None, symbol=None,
                      side=None, quantity=None, max_timer=None, blocking=True,
                      instrument_type=None) -> bool:
    # Call place_market_edge_order function to execute a market edge order
    result = place_market_edge_order(
        exchange_name='bybit',  # Specify exchange name
        account_name=os.getenv('BYBIT_ACCOUNT'),  # Fetch account name from environment variables
        symbol=symbol,  # The trading symbol (e.g., "ETHUSDT")
        side=side,  # The side of the order: "buy" or "sell"
        quantity=quantity,  # The quantity of the asset to buy/sell
        max_timer=max_timer,  # Maximum timer for the edge order
        blocking=blocking,  # Whether the order should block the execution
        instrument_type=instrument_type  # Type of instrument: "SPOT", "PERPETUAL", "LINEAR", etc.
    )

    # Print the response from the order placement attempt for debugging purposes
    print("=== Market Edge Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")

    # Return True if the order was successfully placed, else return False
    return result.success

# Function to place a TWAP (Time Weighted Average Price) order on the exchange
def twap_order(exchange_name=None, account_name=None, symbol=None,
               side=None, quantity=None, duration=None, interval=None, blocking=True,
               instrument_type=None) -> bool:
    # Call place_twap_order function to execute a TWAP order
    result = place_twap_order(
        exchange_name='bybit',  # Specify exchange name
        account_name=os.getenv('BYBIT_ACCOUNT'),  # Fetch account name from environment variables
        symbol=symbol,  # The trading symbol (e.g., "DOTUSDT")
        side=side,  # The side of the order: "buy" or "sell"
        quantity=quantity,  # The total quantity of the asset to buy/sell
        duration=duration,  # Duration of the TWAP order (in seconds)
        interval=interval,  # Interval between executions (in seconds)
        blocking=blocking,  # Whether the order should block the execution
        instrument_type=instrument_type  # Type of instrument: "SPOT", "PERPETUAL", "LINEAR", etc.
    )

    # Print the response from the order placement attempt for debugging purposes
    print("=== TWAP Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")

    # Return True if the order was successfully placed, else return False
    return result.success

# Function to place a TWAP edge order on the exchange
def twap_edge_order(exchange_name=None, account_name=None, symbol=None,
                    side=None, quantity=None, duration=None, interval=None, blocking=True,
                    instrument_type=None) -> bool:
    # Call place_twap_edge_order function to execute a TWAP edge order
    result = place_twap_edge_order(
        exchange_name='bybit',  # Specify exchange name
        account_name=os.getenv('BYBIT_ACCOUNT'),  # Fetch account name from environment variables
        symbol=symbol,  # The trading symbol (e.g., "BTCUSDT")
        side=side,  # The side of the order: "buy" or "sell"
        quantity=quantity,  # The total quantity of the asset to buy/sell
        duration=duration,  # Duration of the TWAP order (in seconds)
        interval=interval,  # Interval between executions (in seconds)
        blocking=blocking,  # Whether the order should block the execution
        instrument_type=instrument_type  # Type of instrument: "SPOT", "PERPETUAL", "LINEAR", etc.
    )

    # Print the response from the order placement attempt for debugging purposes
    print("=== TWAP Edge Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")

    # Return True if the order was successfully placed, else return False
    return result.success
