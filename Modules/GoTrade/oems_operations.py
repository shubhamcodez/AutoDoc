import ctypes
from datetime import datetime
import http.client
import json
import threading
from .message_structures import GQMessage
from typing import Optional, Union, Dict, Any
from http import HTTPStatus
from .request_types import LoginResponse, OrderResponse, LoginRequest, MarketOrderRequest, LimitOrderRequest, TWAPOrderRequest, MarketEdgeOrderRequest, TwapEdgeOrderRequest

HOSTNAME = "localhost"
HANDSHAKE_TOKEN = "9f2b9e0cd9a1a2c95b4e0b123c7b8d6a"

def login_to_exchange(exchange_name=None, account_name=None, key=None, 
                     secret=None, passphrase="", authenticate=True) -> LoginResponse:
    # Validate required inputs
    if not all([exchange_name, account_name, key, secret]):
        return LoginResponse(
            success=False,
            status_code=400,
            message="Missing required fields: exchange_name, account_name, api_key, and secret_key are required"
        )
    
    # Create proper request object
    request = LoginRequest(
        name=account_name,
        key=key,
        secret=secret,
        passphrase=passphrase,
        authenticate=authenticate
    )
    
    try:
        conn = http.client.HTTPConnection(HOSTNAME, 9998, timeout=10)
        headers = {
            "Content-Type": "application/json",
            "Handshake-Token": HANDSHAKE_TOKEN
        }
        
        conn.request("POST", f"/{exchange_name.lower()}/login", 
                    body=json.dumps(request.model_dump()),
                    headers=headers)
        response = conn.getresponse()
        response_data = json.loads(response.read())
        
        # Handle response based on response field
        return LoginResponse(
            success=response_data["response"] == "SUCCESS",
            status_code=response_data.get("status_code", 0),
            message=response_data.get("message", "Unknown response")
        )
            
    except ConnectionRefusedError:
        return LoginResponse(
            success=False,
            status_code=503,
            message="Could not connect to server - connection refused"
        )
    except http.client.HTTPException as e:
        return LoginResponse(
            success=False,
            status_code=500,
            message=f"HTTP error occurred: {str(e)}"
        )
    except Exception as e:
        return LoginResponse(
            success=False,
            status_code=500,
            message=f"An error occurred: {str(e)}"
        )
    finally:
        conn.close()

def _send_order(msg: GQMessage) -> OrderResponse:
    """Send order to exchange
    
    Args:
        msg: GQMessage structure containing order details
        
    Returns:
        OrderResponse with success status, HTTP code and message
    """
    conn = http.client.HTTPConnection(HOSTNAME, 9998)
    headers = {
        "Content-Type": "application/octet-stream",
        "Handshake-Token": HANDSHAKE_TOKEN
    }
    
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        conn.request("POST", "/place", body=bytes(msg), headers=headers)
        response = conn.getresponse()
        
        # Just read the raw response, don't try to parse it
        response_data = response.read()
        
        return OrderResponse(
            success=response.status in (200, 201),
            status_code=response.status,
            message=f"[{current_time}] Order {'sent' if response.status in (200, 201) else 'failed'}",
            response_data=None  # We don't parse the binary response
        )
    except Exception as e:
        return OrderResponse(
            success=False,
            status_code=500,
            message=f"[{datetime.now()}] Error: {str(e)}"
        )
    finally:
        conn.close()

def _send_order_nonblocking(msg: GQMessage) -> OrderResponse:
    """Non-blocking order placement that ensures request completion"""
    conn = http.client.HTTPConnection(HOSTNAME, 9998)
    headers = {
        "Content-Type": "application/octet-stream",
        "Handshake-Token": HANDSHAKE_TOKEN
    }
    
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        conn.request("POST", "/place", body=bytes(msg), headers=headers)
        
        # Get response but don't wait for body
        response = conn.getresponse()
        response.read()  # Read but ignore response body
        
        return OrderResponse(
            success=True,
            status_code=202,
            message=f"[{current_time}] Order submitted asynchronously",
            response_data=None
        )
    except Exception as e:
        return OrderResponse(
            success=False,
            status_code=500,
            message=f"[{datetime.now()}] Error: {str(e)}"
        )
    finally:
        conn.close()

def place_market_order(exchange_name=None, account_name=None, symbol=None, 
                      side=None, quantity=None, blocking=True,
                      instrument_type="") -> OrderResponse:
    """Place a market order through OEMS"""
    
    # Create and validate request
    request = MarketOrderRequest(
        exchange_name=exchange_name,
        account_name=account_name,
        symbol=symbol,
        side=side,
        quantity=quantity,
        instrument_type=instrument_type
    )
    
    # Validate request
    is_valid, error_msg = request.validate()
    if not is_valid:
        return OrderResponse(
            success=False,
            status_code=400,
            message=error_msg
        )

    # Create GQMessage
    msg = GQMessage()
    msg.algorithm_type = b"PLACE"
    msg.exchange = request.exchange_name.upper().encode()
    msg.account = request.account_name.encode()
    msg.symbol = request.symbol.encode()
    msg.side_or_place_id.side = request.side.encode()
    msg.quantity = request.quantity
    msg.price = 0.0
    msg.credential_id = b""
    msg.params.place.type = b"market"
    msg.params.place.instrument_type = request.instrument_type.encode() if request.exchange_name == "bybit" else b""
    
    # Send order
    if blocking:
        return _send_order(msg)
    else:
        if _send_order_nonblocking(msg):
            return OrderResponse(
                success=True,
                status_code=202,
                message="Order submitted asynchronously",
                response_data=None
            )
        else:
            return OrderResponse(
                success=False,
                status_code=500,
                message="Failed to submit nonblocking order",
                response_data=None
            )

def place_limit_order(exchange_name=None, account_name=None, symbol=None, 
                     side=None, quantity=None, price=None, blocking=True,
                     instrument_type="") -> OrderResponse:
    """Place a limit order through OEMS"""
    
    # Create and validate request
    request = LimitOrderRequest(
        exchange_name=exchange_name,
        account_name=account_name,
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        instrument_type=instrument_type
    )
    
    # Validate request
    is_valid, error_msg = request.validate()
    if not is_valid:
        return OrderResponse(
            success=False,
            status_code=400,
            message=error_msg
        )

    # Create GQMessage
    msg = GQMessage()
    msg.algorithm_type = b"PLACE"
    msg.exchange = request.exchange_name.upper().encode()
    msg.account = request.account_name.encode()
    msg.symbol = request.symbol.encode()
    msg.side_or_place_id.side = request.side.encode()
    msg.quantity = request.quantity
    msg.price = request.price
    msg.credential_id = b""
    msg.params.place.type = b"limit"
    msg.params.place.instrument_type = request.instrument_type.encode() if request.exchange_name == "bybit" else b""
    
    # Send order
    if blocking:
        return _send_order(msg)
    else:
        if _send_order_nonblocking(msg):
            return OrderResponse(
                success=True,
                status_code=202,
                message="Order submitted asynchronously",
                response_data=None
            )
        else:
            return OrderResponse(
                success=False,
                status_code=500,
                message="Failed to submit nonblocking order",
                response_data=None
            )

# Place TWAP Order
def place_twap_order(exchange_name=None, account_name=None, symbol=None,
                     side=None, quantity=None, duration=None, interval=None,
                     blocking=True, instrument_type="") -> OrderResponse:
    """
    Place a TWAP order through OEMS.
    """
    # Create and validate request
    request = TWAPOrderRequest(
        exchange_name=exchange_name,
        account_name=account_name,
        symbol=symbol,
        side=side,
        quantity=quantity,
        duration=duration,
        interval=interval,
        instrument_type=instrument_type
    )

    is_valid, error_msg = request.validate()
    if not is_valid:
        return OrderResponse(
            success=False,
            status_code=400,
            message=error_msg
        )

    # Create the TWAP-specific GQMessage
    msg = GQMessage()
    msg.algorithm_type = b"TWAP"
    msg.exchange = request.exchange_name.upper().encode()
    msg.account = request.account_name.encode()
    msg.symbol = request.symbol.encode()
    msg.side_or_place_id.side = request.side.encode()
    msg.quantity = request.quantity
    msg.price = 0.0  # TWAP orders typically don't specify a fixed price
    msg.credential_id = b""

    # Fill TWAP-specific parameters
    msg.params.twap.duration = request.duration
    msg.params.twap.interval = request.interval
    msg.params.place.instrument_type = request.instrument_type.encode() if request.exchange_name == "bybit" else b""

    # Send the order (blocking or non-blocking)
    if blocking:
        return _send_order(msg)
    else:
        return _send_order_nonblocking(msg)


def place_market_edge_order(exchange_name=None, account_name=None, symbol=None,
                            side=None, quantity=None, max_timer=None,
                            blocking=True, instrument_type="") -> OrderResponse:
    """
    Place a Market Edge order through OEMS.
    """
    # Create and validate request
    request = MarketEdgeOrderRequest(
        exchange_name=exchange_name,
        account_name=account_name,
        symbol=symbol,
        side=side,
        quantity=quantity,
        max_timer=max_timer,
        instrument_type=instrument_type
    )

    is_valid, error_msg = request.validate()
    if not is_valid:
        return OrderResponse(
            success=False,
            status_code=400,
            message=error_msg
        )

    # Create the Market Edge-specific GQMessage
    msg = GQMessage()
    msg.algorithm_type = b"MARKET_EDGE"
    msg.exchange = request.exchange_name.upper().encode()
    msg.account = request.account_name.encode()
    msg.symbol = request.symbol.encode()
    msg.side_or_place_id.side = request.side.encode()
    msg.quantity = request.quantity
    msg.price = 0.0  # Market Edge orders typically don't specify a fixed price
    msg.credential_id = b""

    # Fill Market Edge-specific parameters
    msg.params.market_edge.max_timer = request.max_timer
    msg.params.place.instrument_type = request.instrument_type.encode() if request.exchange_name == "bybit" else b""

    # Send the order (blocking or non-blocking)
    if blocking:
        return _send_order(msg)
    else:
        return _send_order_nonblocking(msg)


def place_twap_edge_order(exchange_name=None, account_name=None, symbol=None,
                          side=None, quantity=None, duration=None, interval=None,
                          blocking=True, instrument_type="") -> OrderResponse:
    """
    Place a TWAP Edge order through OEMS.
    """
    # Create and validate request
    request = TwapEdgeOrderRequest(
        exchange_name=exchange_name,
        account_name=account_name,
        symbol=symbol,
        side=side,
        quantity=quantity,
        duration=duration,
        interval=interval,
        instrument_type=instrument_type
    )

    is_valid, error_msg = request.validate()
    if not is_valid:
        return OrderResponse(
            success=False,
            status_code=400,
            message=error_msg
        )

    # Create the TWAP Edge-specific GQMessage
    msg = GQMessage()
    msg.algorithm_type = b"TWAP_EDGE"
    msg.exchange = request.exchange_name.upper().encode()
    msg.account = request.account_name.encode()
    msg.symbol = request.symbol.encode()
    msg.side_or_place_id.side = request.side.encode()
    msg.quantity = request.quantity
    msg.price = 0.0  # TWAP Edge orders typically don't specify a fixed price
    msg.credential_id = b""

    # Fill TWAP Edge-specific parameters
    msg.params.twap.duration = request.duration
    msg.params.twap.interval = request.interval
    msg.params.place.instrument_type = request.instrument_type.encode() if request.exchange_name == "bybit" else b""

    # Send the order (blocking or non-blocking)
    if blocking:
        return _send_order(msg)
    else:
        return _send_order_nonblocking(msg)

# Modify Order

# Cancel Order

# Logout
