import os
import sys
from dotenv import load_dotenv

# Add parent directory to the sys.path to allow import of modules from parent directory
sys.path.append("..")

# Import necessary functions from the parent module (oems_operations)
from ..oems_operations import (
    login_to_exchange, 
    place_market_order, 
    place_limit_order, 
    place_market_edge_order, 
    place_twap_order, 
    place_twap_edge_order
)

# Load environment variables from .env file
load_dotenv()

# Function to login to the exchange
def login() -> bool:
    # Attempt to log in using provided credentials from environment variables
    result = login_to_exchange(
        exchange_name='okx',
        account_name=os.getenv('OKX_ACCOUNT'),  # Fetch the account name from the environment variables
        key=os.getenv('OKX_API_KEY'),  # Fetch the API key
        secret=os.getenv('OKX_SECRET'),  # Fetch the secret key
        passphrase=os.getenv('OKX_PASSPHRASE'),  # Fetch the passphrase
        authenticate=True  # Set to True to perform authentication
    )
    
    # Print the result of the login attempt
    print("=== Login Response ===")
    print(f"Status Code: {result.status_code}")  # Display the HTTP status code of the response
    print(f"Message: {result.message}")  # Display the message from the response
    
    # Return True if the login is successful (status code is 0 and message is 'OK')
    return result.message == "OK" and result.status_code == 0

# Function to place a market order
def market_order(symbol=None, side=None, quantity=None, blocking=True) -> bool:
    # Call the function to place a market order on OKX
    result = place_market_order(
        exchange_name='okx',
        account_name=os.getenv('OKX_ACCOUNT'),
        symbol=symbol,  # The trading pair symbol (e.g., "DOT-USDT-SWAP")
        side=side,  # Side of the order: "buy" or "sell"
        quantity=quantity,  # Quantity to buy or sell
        blocking=blocking  # Whether to block until the order is complete
    )
    
    # Print the result of the market order attempt
    print("=== Market Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")
    
    # Return True if the order was successfully placed
    return result.success

# Function to place a limit order
def limit_order(symbol=None, side=None, quantity=None, price=None, blocking=True) -> bool:
    # Call the function to place a limit order on OKX
    result = place_limit_order(
        exchange_name='okx',
        account_name=os.getenv('OKX_ACCOUNT'),
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,  # The price at which the order should be placed
        blocking=blocking
    )
    
    # Print the result of the limit order attempt
    print("=== Limit Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")
    
    # Return True if the order was successfully placed
    return result.success

# Function to place a market edge order
def market_edge_order(symbol=None, side=None, quantity=None, max_timer=None, blocking=True) -> bool:
    # Call the function to place a market edge order on OKX
    result = place_market_edge_order(
        exchange_name='okx',
        account_name=os.getenv('OKX_ACCOUNT'),
        symbol=symbol,
        side=side,
        quantity=quantity,
        max_timer=max_timer,  # Maximum time to wait for the order to be filled
        blocking=blocking
    )

    # Print the result of the market edge order attempt
    print("=== Market Edge Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")

    # Return True if the order was successfully placed
    return result.success

# Function to place a TWAP (Time-Weighted Average Price) order
def twap_order(symbol=None, side=None, quantity=None, duration=None, interval=None, blocking=True) -> bool:
    # Call the function to place a TWAP order on OKX
    result = place_twap_order(
        exchange_name='okx',
        account_name=os.getenv('OKX_ACCOUNT'),
        symbol=symbol,
        side=side,
        quantity=quantity,
        duration=duration,  # Total duration of the TWAP order in seconds
        interval=interval,  # Interval between executions in seconds
        blocking=blocking
    )

    # Print the result of the TWAP order attempt
    print("=== TWAP Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")

    # Return True if the order was successfully placed
    return result.success

# Function to place a TWAP edge order
def twap_edge_order(symbol=None, side=None, quantity=None, duration=None, interval=None, blocking=True) -> bool:
    # Call the function to place a TWAP edge order on OKX
    result = place_twap_edge_order(
        exchange_name='okx',
        account_name=os.getenv('OKX_ACCOUNT'),
        symbol=symbol,
        side=side,
        quantity=quantity,
        duration=duration,  # Total duration of the TWAP edge order in seconds
        interval=interval,  # Interval between executions in seconds
        blocking=blocking
    )

    # Print the result of the TWAP edge order attempt
    print("=== TWAP Edge Order Response ===")
    print(f"Status Code: {result.status_code}")
    print(f"Message: {result.message}")

    # Return True if the order was successfully placed
    return result.success

