# PROJECT: SM-SAVBasics
# SPECIFY: Modules/ListToString.py
# STARTED: 2024.July by CelestialAddy
# ===================================================================================================

def List_To_String(List, SepChar):
    '''Returns a string of all items in List combined sequentially, separated by SepChar. Or None.'''
    try:
        String = ""
        Index = -1
        for Item in List:
            Index = Index + 1
            String = String + str(Item)
            if Index != len(List) - 1:
                String = String + str(SepChar)
                pass
            continue
        return String
    except:
        return None
    pass
#

# ===================================================================================================
# NOTHING: Beyond this point.
