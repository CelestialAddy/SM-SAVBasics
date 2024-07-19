# PROJECT: SM-SAVBasics
# SPECIFY: Sign.py
# STARTED: 2024.July by CelestialAddy
# ===================================================================================================

# 0 / Start.
print("SAVBasics v1 Sign by CelestialAddy" + "\n" + "_" * 50 + "\n")

# 1 / Setup.
try:
    import os, sys, struct
    import Modules.KnownSignatures as KS
except:
    input("ERROR: Module import unsuccessful - Sign.py.\n")
    exit()

# 2 / Establish operational mode/directions.
Opts = {
    "UI" : bool(),
    "Path" : str(),
    "SigType" : str(),
    "BigEndian" : bool(),
    }
CLAs = sys.argv
try:
    Opts["UI"] = False
    Opts["Path"] = str(CLAs[1])
    try:
        SigsBytes = list(KS.KnownSignatures.keys())
        SigsNamed = list(KS.KnownSignatures.values())
        Opts["SigType"] = SigsBytes[SigsNamed.index(CLAs[2])]
    except:
        Opts["SigType"] = bytes(CLAs[2], "utf-8")
    Opts["BigEndian"] = bool(int(CLAs[3]))
    print("Proceeding in command-line mode.")
except:
    Opts["UI"] = True
    print("Proceeding in console-input mode.")
if Opts["UI"] == True:
    AnsValid = False
    while AnsValid != True:
        Ans = input("Enter input/output SAV file path (such as C:/Users/Me/Documents/...): ")
        if len(Ans) > 0:
            Opts["Path"] = Ans
            AnsValid = True
        else:
            print("ERROR: Unworkable answer.")
            AnsValid = False
    AnsValid = False
    while AnsValid != True:
        print("\nPossible signatures:")
        for Sig in KS.KnownSignatures:
            print("\t" + KS.KnownSignatures[Sig])
        print("You may use any of these by listed name or a custom (8 characters) signature.")
        Ans = input("Pick/type the signature to use for the SAV: ")
        if Ans in KS.KnownSignatures.values():
            SigsBytes = list(KS.KnownSignatures.keys())
            SigsNamed = list(KS.KnownSignatures.values())
            Opts["SigType"] = SigsBytes[SigsNamed.index(Ans)]
            AnsValid = True
        elif len(Ans) == 8:
            Opts["SigType"] = bytes(Ans, "utf-8")
            AnsValid = True
        else:
            print("ERROR: Unworkable answer.")
            AnsValid = False
    AnsValid = False
    while AnsValid != True:
        Ans = input("Use big endian (yes/no = 1/0, definitely 0 for PC saves): ")
        if Ans == "0":
            Opts["BigEndian"] = False
            AnsValid = True
        elif Ans == "1":
            Opts["BigEndian"] = True
            AnsValid = True
        else:
            print("ERROR: Unworkable answer.")
            AnsValid = False

# 3 / Execute operations.
try: # 3.1 / Input.
    Stage1 = open(Opts["Path"], "rb")
    Stage2 = Stage1.read()
    Stage1.close()
except:
    input("ERROR: On input.")
    exit()
try: # 3.2 / Signing.
    FStr = "8s4784b"
    End = ["<", ">"][int(bool(Opts["BigEndian"]))]
    FStr = End + FStr
    Stage3 = struct.unpack(FStr, Stage2)
    Stage3 = list(Stage3)
    Stage3[0] = Opts["SigType"]
    Stage4 = struct.pack(FStr, *Stage3)
except:
    input("ERROR: On sign.")
    exit()
try: # 3.3 / Output.
    Stage5 = open(Opts["Path"], "wb")
    Stage5.write(Stage4)
    Stage5.close()
except:
    input("ERROR: On output.")
    exit()

# 4 / End.
print("Action completed successfully.")
if Opts["UI"] == True:
    input("\n")

# ===================================================================================================
# NOTHING: Beyond this point.
