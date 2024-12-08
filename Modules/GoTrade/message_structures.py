import ctypes

# Time-Weighted Average Price (TWAP) algorithm parameters
# This structure defines the configuration for TWAP order execution
class TwapParams(ctypes.Structure):
    _pack_ = 1  # Ensures tight memory packing with no padding between fields
    _fields_ = [
        ("duration", ctypes.c_int),   # Total duration for the TWAP execution in seconds
        ("interval", ctypes.c_int),   # Time interval between each partial order in seconds
    ]

# Market Edge algorithm parameters
# Contains settings for the market edge trading strategy
class MarketEdgeParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("max_timer", ctypes.c_int),  # Maximum time limit for the market edge algorithm in seconds
    ]

# Take Profit/Stop Loss parameters
# Defines the percentage levels for automatic profit taking and loss prevention
class TPSLParams(ctypes.Structure):
    _pack = 1
    _fields_ = [
        ("tp_percentage", ctypes.c_double),  # Take profit trigger percentage
        ("sl_percentage", ctypes.c_double)   # Stop loss trigger percentage
    ]

# Place order parameters
# Contains basic order placement configurations
class PlaceParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("type", ctypes.c_char * 16),          # Order type (e.g., "LIMIT", "MARKET")
        ("instrument_type", ctypes.c_char * 16) # Type of instrument being traded
    ]

# Union of all algorithm-specific parameters
# This allows flexible parameter storage based on the algorithm type being used
class AlgoParams(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ("twap", TwapParams),           # TWAP algorithm parameters
        ("market_edge", MarketEdgeParams), # Market Edge algorithm parameters
        ("place", PlaceParams),         # Basic order placement parameters
        ("tpsl", TPSLParams)            # Take Profit/Stop Loss parameters
    ]

# Union for handling either order side or place ID
# This allows the same field to be used for new orders (side) or order modifications (place_id)
class SideOrPlaceID(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ("side", ctypes.c_char * 8),    # Order side ("BUY" or "SELL")
        ("place_id", ctypes.c_int)      # Unique identifier for an existing order
    ]

# Main message structure for the Global Queue (GQ) system
# This structure contains all necessary information for processing a trading request
class GQMessage(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("algorithm_type", ctypes.c_char * 16),  # Type of algorithm to be used (e.g., "TWAP", "MARKET_EDGE")
        ("exchange", ctypes.c_char * 16),        # Target exchange for the order
        ("account", ctypes.c_char * 32),         # Trading account identifier
        ("symbol", ctypes.c_char * 32),          # Trading symbol/instrument
        ("side_or_place_id", SideOrPlaceID),     # Either order side or place ID for modifications
        ("quantity", ctypes.c_double),           # Order quantity
        ("price", ctypes.c_double),              # Order price
        ("credential_id", ctypes.c_char * 40),   # Authentication credential identifier
        ("params", AlgoParams),                  # Algorithm-specific parameters
    ]

# Usage Notes:
# 1. All structures use _pack_ = 1 to ensure consistent memory layout across different platforms
# 2. Character arrays are fixed-size to maintain stable memory structure
# 3. The AlgoParams union allows different algorithm parameters to share the same memory space
# 4. The SideOrPlaceID union enables dual functionality for new orders and modifications
# 5. All numeric fields use explicit ctypes to ensure consistent data types across systems