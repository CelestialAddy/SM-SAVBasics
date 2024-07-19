# PROJECT: SM-SAVBasics
# SPECIFY: Modules/JSONImport.py
# STARTED: 2024.July by CelestialAddy
# ===================================================================================================

def JSON_Import(JSONString):
    '''Returns dictionary representation of save data if valid, None otherwise.'''
    try:
        try:
            import json
            import Modules.IntListToBytes as Hack
        except:
            input("ERROR: Module import unsuccessful - JSONImport.py.")
            exit()
        JSONString = str(JSONString)
        SDD = json.loads(JSONString)
        # On export to JSON, bytes objects (for struct strings) become integer lists.
        # This needs to be reversed here...
        IntList = SDD["General"]["Signature"]
        SDD["General"]["Signature"] = Hack.ILTB(IntList)
        Iterate = ["01", "02", "03", "04", "05", "06", "07", "08"]
        for Slot in Iterate:
            IntList = SDD["Slot" + Slot]["Miscellaneous"]["UnknownString01"]
            SDD["Slot" + Slot]["Miscellaneous"]["UnknownString01"] = Hack.ILTB(IntList)
            IntList = SDD["Slot" + Slot]["Miscellaneous"]["UnknownString02"]
            SDD["Slot" + Slot]["Miscellaneous"]["UnknownString02"] = Hack.ILTB(IntList)
        #
        return SDD
    except:
        return None
    pass
#

# ===================================================================================================
# NOTHING: Beyond this point.
