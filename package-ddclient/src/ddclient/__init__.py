__version__ = "0.8.3"
# 0.7.0
# Support allow bit feature for setting datagram

# 0.8.0
# 1. Support data object id field for data gram payload
# 2. Support 'IsNoneVolatile' and 'IsRetain' columns for new DD

# 0.8.1
# Support uint64_t type in ddclient (for code generation to work).
# Disabled the warning for "IsNoneVolatile" and "IsRetain" when the value is empty.
# Updated the Supported Template version to 0.30.

# 0.8.2
# Send E_DATA_OBJECT_ID in payload as two uint32 data

# 0.8.3
# skip time stamp compare when compare payload
