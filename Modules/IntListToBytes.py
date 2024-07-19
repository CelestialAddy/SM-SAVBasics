# PROJECT: SM-SAVBasics
# SPECIFY: Modules/IntListToBytes.py
# STARTED: 2024.July by CelestialAddy
# ===================================================================================================

def ILTB(IntList):
    '''Returns a bytes object containing every integer value from a list, or None if invalid.'''
    try:
        IntList = list(IntList)
        Bytes = bytearray()
        for Value in IntList:
            Bytes.append(Value)
        return bytes(Bytes)
    except:
        return None
    pass
#

# ===================================================================================================
# NOTHING: Beyond this point.
