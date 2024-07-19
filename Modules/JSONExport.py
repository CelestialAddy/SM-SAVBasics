# PROJECT: SM-SAVBasics
# SPECIFY: Modules/JSONExport.py
# STARTED: 2024.July by CelestialAddy
# ===================================================================================================

def JSON_Export(SaveDataDictionary):
    '''Returns JSON string representation of save data if valid, None otherwise.'''
    try:
        try:
            import json
            import Modules.BytesToIntList as Hack
            import Modules.KnownSignatures as KS
        except:
            input("ERROR: Module import unsuccessful - JSONExport.py.")
            exit()
        SaveDataDictionary = dict(SaveDataDictionary)
        # Add this I guess.
        BSig = SaveDataDictionary["General"]["Signature"]
        if BSig in KS.KnownSignatures.keys():
            SaveDataDictionary["Meta"]["SignatureMatch"] = KS.KnownSignatures[BSig]
        else:
            SaveDataDictionary["Meta"]["SignatureMatch"] = "N/A",
        # JSON doesn't support bytes objects, so...
        Bytes = SaveDataDictionary["General"]["Signature"]
        SaveDataDictionary["General"]["Signature"] = Hack.BTIL(Bytes)
        Iterate = ["01", "02", "03", "04", "05", "06", "07", "08"]
        for Slot in Iterate:
            Bytes = SaveDataDictionary["Slot" + Slot]["Miscellaneous"]["UnknownString01"]
            SaveDataDictionary["Slot" + Slot]["Miscellaneous"]["UnknownString01"] = Hack.BTIL(Bytes)
            Bytes = SaveDataDictionary["Slot" + Slot]["Miscellaneous"]["UnknownString02"]
            SaveDataDictionary["Slot" + Slot]["Miscellaneous"]["UnknownString02"] = Hack.BTIL(Bytes)
        #
        JSONString = json.dumps(SaveDataDictionary, indent="\t")
        return JSONString + "\n"
    except:
        return None
    pass
#

# ===================================================================================================
# NOTHING: Beyond this point.
