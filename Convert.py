# PROJECT: SM-SAVBasics
# SPECIFY: Convert.py
# STARTED: 2024.July by CelestialAddy
# ===================================================================================================

# 0 / Start.
print("SAVBasics v1 Convert by CelesialAddy" + "\n" + "_" * 50 + "\n")

# 1 / Setup.
try:
    import sys, struct, json
    import Modules.SAVImport as SAVImport
    import Modules.SAVExport as SAVExport
    import Modules.JSONImport as JSONImport
    import Modules.JSONExport as JSONExport
    import Modules.StatusUpdate as SU
except:
    input("ERROR: Module import unsuccessful - Convert.py.\n")
    exit()

# 2 / Establish operational mode/directions.
OpModes = [
    "PC_SAV_TO_JSON",
    "JSON_TO_PC_SAV",
    ]
Opts = {
    "UI" : bool(),
    "Conversion" : str(),
    "InputPath" : str(),
    "OutputPath" : str(),
    "BigEndian" : bool(),
    }
CLAs = sys.argv
try:
    Opts["UI"] = False
    Opts["Conversion"] = str(OpModes[OpModes.index(CLAs[1])])
    Opts["InputPath"] = str(CLAs[2])
    Opts["OutputPath"] = str(CLAs[3])
    Opts["BigEndian"] = bool(int(CLAs[4]))
    print("Proceeding in command-line mode.")
except:
    Opts["UI"] = True
    print("Proceeding in console-input mode.")
if Opts["UI"] == True:
    AnsValid = False
    while AnsValid != True:
        Ans = input("Pick your action by number.\n\n\t1 : PC SAV to JSON\n\t2 : JSON TO PC SAV\n\n")
        if Ans == "1":
            Opts["Conversion"] = "PC_SAV_TO_JSON"
            AnsValid = True
        elif Ans == "2":
            Opts["Conversion"] = "JSON_TO_PC_SAV"
            AnsValid = True
        else:
            print("ERROR: Unworkable answer.")
            AnsValid = False
    AnsValid = False
    while AnsValid != True:
        Ans = input("Enter input file path (such as C:/Users/Me/Documents/...): ")
        if len(Ans) > 0:
            Opts["InputPath"] = Ans
            AnsValid = True
        else:
            print("ERROR: Unworkable answer.")
            AnsValid = False
    AnsValid = False
    while AnsValid != True:
        Ans = input("Enter output file path (such as C:/Users/Me/Documents/...): ")
        if len(Ans) > 0:
            Opts["OutputPath"] = Ans
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
    if Opts["Conversion"] == "PC_SAV_TO_JSON":
        Stage1 = open(Opts["InputPath"], "rb")
        Stage2 = Stage1.read()
        Stage1.close()
    elif Opts["Conversion"] == "JSON_TO_PC_SAV":
        Stage1 = open(Opts["InputPath"], "r")
        Stage2 = Stage1.read()
        Stage1.close()
    else:
        SU.Signal("ERROR: Bad input conversion action.", Opts["UI"])
        exit()
except:
    SU.Signal("ERROR: On input.", Opts["UI"])
    exit()
try: # 3.2 / Conversion.
    if Opts["Conversion"] == "PC_SAV_TO_JSON":
        Stage3 = SAVImport.SAV_Import(Stage2, Opts["BigEndian"])
        Stage4 = JSONExport.JSON_Export(Stage3)
        if Stage4 == None:
            Except()
    elif Opts["Conversion"] == "JSON_TO_PC_SAV":
        Stage3 = JSONImport.JSON_Import(Stage2)
        Stage4 = SAVExport.SAV_Export(Stage3, Opts["BigEndian"])
        if Stage4 == None:
            Except()
    else:
        SU.Signal("ERROR: Bad conversion conversion action.", Opts["UI"])
        exit()
except:
    SU.Signal("ERROR: On inter-format conversion.", Opts["UI"])
    exit()
try: # 3.3 / Output.
    if Opts["Conversion"] == "PC_SAV_TO_JSON":
        Stage5 = open(Opts["OutputPath"], "w")
        Stage5.write(Stage4)
        Stage5.close()
    elif Opts["Conversion"] == "JSON_TO_PC_SAV":
        Stage5 = open(Opts["OutputPath"], "wb")
        Stage5.write(Stage4)
        Stage5.close()
    else:
        SU.Signal("ERROR: Bad output conversion action.", Opts["UI"])
        exit()
except:
    SU.Signal("ERROR: On output.", Opts["UI"])
    exit()

# 4 / End.
print("Action completed successfully.")
if Opts["UI"] == True:
    input("\n")

# ===================================================================================================
# NOTHING: Beyond this point.
