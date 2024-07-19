# PROJECT: SM-SAVBasics
# SPECIFY: Modules/BytesToIntList.py
# STARTED: 2024.July by CelestialAddy
# ===================================================================================================

def BTIL(BytesObj):
    '''Returns every object in BytesObj as an integer, in a list, or None if invalid.'''
    try:
        IntList = []
        for Value in bytes(BytesObj):
            IntList.append(Value)
        return IntList
    except:
        return None
    pass
#

# ===================================================================================================
# NOTHING: Beyond this point.
