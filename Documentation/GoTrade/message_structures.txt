import ctypes

# Define the algorithm-specific parameter structures
class TwapParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("duration", ctypes.c_int),
        ("interval", ctypes.c_int),
    ]

class MarketEdgeParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("max_timer",  ctypes.c_int),
    ]

class TPSLParams(ctypes.Structure):
    _pack = 1
    _fields_ = [
        ("tp_percentage", ctypes.c_double),
        ("sl_percentage", ctypes.c_double)
    ]

class PlaceParams(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("type", ctypes.c_char * 16),
        ("instrument_type", ctypes.c_char * 16),
    ]

class AlgoParams(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ("twap", TwapParams),
        ("market_edge", MarketEdgeParams),
        ("place", PlaceParams),
        ("tpsl", TPSLParams)
    ]

class SideOrPlaceID(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ("side", ctypes.c_char * 8),
        ("place_id", ctypes.c_int)
    ]

class GQMessage(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("algorithm_type", ctypes.c_char * 16),
        ("exchange", ctypes.c_char * 16),
        ("account", ctypes.c_char * 32),
        ("symbol", ctypes.c_char * 32),
        ("side_or_place_id", SideOrPlaceID),
        ("quantity", ctypes.c_double),
        ("price", ctypes.c_double),
        ("credential_id", ctypes.c_char * 40),
        ("params", AlgoParams),
    ]
