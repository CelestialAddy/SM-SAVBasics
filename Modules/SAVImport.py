# PROJECT: SM-SAVBasics
# SPECIFY: Modules/SAVImport.py
# STARTED: 2024.July by CelestialAddy
# ===================================================================================================

# If more data from the save game is discovered to be useful later...
# ... then these things all need to be changed:
#      * The FStr compositions will need to be updated.
#      * The SDB# chunk/value-encompass offsets will need to be updated.
#      * The SDB#-dictionary value maps will need to be updated.
#      * The first of those is pre-allowed through splitting and notation.
#      * The last of those can be copy-pasted a lot.
#      * There's that at least. Otherwise this is probably clunky, though.

def SAV_Import(SAV, IsBigEndian):
    '''Returns the save data as a dictionary if data is valid.\nReturns None otherwise.'''
    try:
        # STEP 0: Get ready.
        try:
            import struct
            import Modules.ListToString as ListToString
        except:
            input("ERROR: Module import unsuccessful - SAVImport.py.")
            exit()
        SAV = bytearray(SAV)
        IsBigEndian = int(bool(IsBigEndian))
        # STEP 1: Generate format/struct string for SAV.
        FStr_EndianA = ["<", ">"][IsBigEndian]
        FStr_HeaderC = [
            "8s", # Signature.
            "8x", # Padding.
            ]
        FStr_HeaderA = ListToString.List_To_String(FStr_HeaderC, "")
        FStr_Slot0XC = [
            "16x", # Padding.
            "1i", # Continue Level.
            "1i", # Menu Lock.
            "1i", # Unlock Level A.
            "1i", # Unlock Level B.
            "1i", # Unlock Level C.
            "1i", # Unlock Level D.
            "1i", # Unlock Level E.
            "40x", # Padding.
            "1i", # Unknown Volume.
            "1i", # Music Volume.
            "1i", # SFX Volume.
            "1i", # Voice Volume.
            "1i", # Movie Volume.
            "10x", # Padding.
            "1h", # Secret Store Toggles.
            "25x", # Padding.
            "1?", # CC FieldGoal PPK.
            "1?", # CC GravitySlam PPJ.
            "1?", # CC WebHit PPW.
            "1?", # CC BackflipKick PKK.
            "1?", # CC Sting PKP.
            "1?", # CC Palm PKJ.
            "1?", # CC HighWebHit PKW.
            "1?", # CC DiveBomb PJJ.
            "1?", # CC HeadHammer PJP.
            "1?", # CC DiveKick PJK.
            "2x", # Padding.
            "1?", # CC Uppercut KKP.
            "1?", # CC FlipMule KKJ.
            "1?", # CC LowWebHit KKW.
            "1x", # Padding.
            "1?", # CC ScissorKick KPK.
            "1?", # CC HighStomp KPJ.
            "1x", # Padding.
            "1?", # CC Tackle KJJ.
            "1?", # CC Handspring KJK.
            "1?", # CC Haymaker KJP.
            "3x", # Padding.
            "1?", # CC AdvWebDome WCKK.
            "1x", # Padding.
            "1?", # CC AdvWebGloves WCPP.
            "1x", # Padding.
            "1?", # CC AdvImpactWeb WCW.
            "13x", # Padding.
            "3I", # TRAIN BasicAimCombat 1/2/3.
            "3I", # TRAIN BasicSwingTraining 1/2/3.
            "3I", # TRAIN AdvancedSwingTraining 1/2/3.
            "3I", # TRAIN ExpertSwingTraining 1/2/3.
            "3I", # TRAIN BasicZipTraining 1/2/3.
            "3I", # TRAIN AdvancedZipTraining 1/2/3.
            "3I", # TRAIN ExpertZipTraining 1/2/3.
            "3I", # TRAIN SwingRings 1/2/3.
            "3I", # TRAIN SwingPlatforms 1/2/3.
            "3I", # TRAIN ObstacleCourse 1/2/3.
            "2x", # Padding.
            "5h", # PTS SFJ Completion,Perfect,Combat,Secret,Style.
            "4h", # PTS WH Completion,Stealth,Secret,Style.
            "4h", # PTS BOAH Completion,Time,Secret,Style.
            "4h", # PTS OG Completion,Perfect,DefeatedHKs,Style.
            "4h", # PTS TSS Completion,Time,Perfect,Style.
            "5h", # PTS CTTS Completion,Time,Secret,Combat,Style.
            "5h", # PTS SWS Completion,Time,Perfect,Secret,Style.
            "3h", # PTS VL Completion,Time,Perfect.
            "1h", # PTS Unknown01.
            "4h", # PTS VE Completion,Time,Perfect,VultureProximity.
            "1h", # PTS Unknown02.
            "4h", # PTS ADWV Completion,Time,Perfect,Style.
            "1h", # PTS C Completion.
            "1h", # PTS SR Completion.
            "4h", # PTS CDE Completion,Time,Perfect,Style.
            "4h", # PTS TO Completion,Time,Perfect,Style.
            "3h", # PTS RAT Completion,Time,Perfect.
            "8h", # PTS Unknown03-10.
            "5h", # PTS TRE Completion,Bats,Health,Pickups,Style.
            "5h", # PTS BAE Completion,Time,Perfect,Secret,Stealth.
            "1h", # PTS Unknown11.
            "3h", # PTS CC Completion,Time,Perfect.
            "1h", # PTS Unknown12.
            "4h", # PTS OUW Completion,Time,Perfect,Style.
            "4h", # PTS EFO Completion,Perfect,SupersoldiersKilled,Style.
            "2h", # PTS MJK Completion,Perfect.
            "5h", # PTS Unknown 13-17.
            "1h", # PTS SR Style.
            "3h", # PTS C Secret,ProtectedScorpion,Style.
            "1h", # PTS Unknown18.
            "1h", # PTS SR NoPickupsUsed.
            "2h", # PTS Unknown19-20.
            "1h", # PTS TO RideGoblin.
            "6x", # Padding.
            "1i", # Difficulty.
            "1i", # Movement Flags.
            "1?", # Tank Controls.
            "11x", # Padding.
            "1h", # Camera Mode.
            "1h", # Show Style Points.
            "2x", # Padding.
            "2s", # HC/CH.
            "6x", # Padding.
            "1?", # Invert Jump/Web Inputs.
            "1x", # Padding.
            "1?", # Invert Zip/Swing Inputs.
            "1x", # Padding.
            "1?", # Controller Stick/D-PAD Switch.
            "1x", # Padding.
            "1i", # Invert Camera Look.
            "1i", # Controller Vibration.
            "8x", # Padding.
            "8s", # fakehero.
            "8x", # Padding.
            ]
        FStr_Slot0XA = ListToString.List_To_String(FStr_Slot0XC, "")
        FStr_FooterC = [
            "16x", # Padding.
            "1h", # Last Slot.
            "2x", # Padding.
            "1h", # Year.
            "1h", # Month.
            "1h", # Weekday.
            "1h", # Day.
            "1h", # Hour.
            "1h", # Minute.
            "1h", # Second.
            "6x", # Padding.
            ]
        FStr_FooterA = ListToString.List_To_String(FStr_FooterC, "")
        FStr = str(FStr_EndianA + FStr_HeaderA + FStr_Slot0XA * 8 + FStr_FooterA)
        del FStr_HeaderC, FStr_Slot0XC, FStr_FooterC
        # STEP 2: Unpack SAV via struct and FStr.
        # Split into 0-9 chunks (header-slot#-footer) so that dict mapping is easier/changeable.
        SDB = struct.unpack(FStr, SAV)
        # For debugging/updating the SBD offsets right below.
        #Index = 0
        #for Entry in SDB:
        #    if Entry == b'fakehero':
        #        print(Index, "!")
        #    Index = Index + 1
        #/\
        SDB0 = []
        for I in range(0, 1):
            SDB0.append(SDB[I])
        SDB1 = []
        for I in range(1, 181):
            SDB1.append(SDB[I])
        SDB2 = []
        for I in range(181, 361):
            SDB2.append(SDB[I])
        SDB3 = []
        for I in range(361, 541):
            SDB3.append(SDB[I])
        SDB4 = []
        for I in range(541, 721):
            SDB4.append(SDB[I])
        SDB5 = []
        for I in range(721, 901):
            SDB5.append(SDB[I])
        SDB6 = []
        for I in range(901, 1081):
            SDB6.append(SDB[I])
        SDB7 = []
        for I in range(1081, 1261):
            SDB7.append(SDB[I])
        SDB8 = []
        for I in range(1261, 1441):
            SDB8.append(SDB[I])
        SDB9 = []
        for I in range(1441, 1449):
            SDB9.append(SDB[I])
        del SDB
        # STEP 3: Create a dictionary to better represent the save data, and populate it via binary.
        SaveDataBetter = {
            "Meta" : { # Only used in dictionary/JSON outputs to give context.
                "DataType" : "Spider-Man (2002/Windows) save data as handled by SM-SAVBasics",
                "DataForm" : "1",
                },
            "General" : { # Header/footer data.
                "Signature" : SDB0[0],
                "LastSaveSlot" : SDB9[0],
                "LastSaveYear" : SDB9[1],
                "LastSaveMonth" : SDB9[2],
                "LastSaveWeekday" : SDB9[3],
                "LastSaveDay" : SDB9[4],
                "LastSaveHour" : SDB9[5],
                "LastSaveMinute" : SDB9[6],
                "LastSaveSecond" : SDB9[7],
                },
            "Slot01" : { # Slot-tailored data.
                "Baseline" : {
                    "Difficulty" : SDB1[168],
                    "ContinueLevel" : SDB1[0],
                    "UnlocksLevelUNKNOWN" : SDB1[2],
                    "UnlocksLevelEASY" : SDB1[3],
                    "UnlocksLevelNORMAL" : SDB1[4],
                    "UnlocksLevelHERO" : SDB1[5],
                    "UnlocksLevelSUPERHERO" : SDB1[6],
                    "SecretStoreToggles" : SDB1[12],
                    },
                "CombatControls" : {
                    "FieldGoal_PPK" : SDB1[13],
                    "GravitySlam_PPJ" : SDB1[14],
                    "WebHit_PPW" : SDB1[15],
                    "BackflipKick_PKK" : SDB1[16],
                    "Sting_PKP" : SDB1[17],
                    "Palm_PKJ" : SDB1[18],
                    "HighWebHit_PKW" : SDB1[19],
                    "DiveBomb_PJJ" : SDB1[20],
                    "HeadHammer_PJP" : SDB1[21],
                    "DiveKick_PJK" : SDB1[22],
                    "Uppercut_KKP" : SDB1[23],
                    "FlipMule_KKJ" : SDB1[24],
                    "LowWebHit_KKW" : SDB1[25],
                    "ScissorKick_KPK" : SDB1[26],
                    "HighStomp_KPJ" : SDB1[27],
                    "Tackle_KJJ" : SDB1[28],
                    "Handspring_KJK" : SDB1[29],
                    "Haymaker_KJP" : SDB1[30],
                    "AdvWebDome_WCKK" : SDB1[31],
                    "AdvWebGloves_WCPP" : SDB1[32],
                    "AdvImpactWeb_WCW" : SDB1[33],
                    },
                "TrainingBestTimes" : {
                    "BasicAirCombat" : [SDB1[34], SDB1[35], SDB1[36]],
                    "BasicSwingTraining" : [SDB1[37], SDB1[38], SDB1[39]],
                    "AdvancedSwingTraining" : [SDB1[40], SDB1[41], SDB1[42]],
                    "ExpertSwingTraining" : [SDB1[43], SDB1[44], SDB1[45]],
                    "BasicZipTraining" : [SDB1[46], SDB1[47], SDB1[48]],
                    "AdvancedZipTraining" : [SDB1[49], SDB1[50], SDB1[51]],
                    "ExpertZipTraining" : [SDB1[52], SDB1[53], SDB1[54]],
                    "SwingRings" : [SDB1[55], SDB1[56], SDB1[57]],
                    "SwingPlatforms" : [SDB1[58], SDB1[59], SDB1[60]],
                    "ObstacleCourse" : [SDB1[61], SDB1[62], SDB2[63]],
                    },
                "LevelBonusPoints" : {
                    "SearchForJustice" : {
                        "LevelCompletion" : SDB1[64],
                        "Perfect" : SDB1[65],
                        "Combat" : SDB1[66],
                        "SecretsFound" : SDB1[67],
                        "Style" : SDB1[68],
                        },
                    "WarehouseHunt" : {
                        "LevelCompletion" : SDB1[69],
                        "StealthBonus" : SDB1[70],
                        "SecretsFound" : SDB1[71],
                        "Style" : SDB1[72],
                        },
                    "BirthOfAHero" : {
                        "LevelCompletion" : SDB1[73],
                        "Time" : SDB1[74],
                        "SecretsFound" : SDB1[75],
                        "Style" : SDB1[76],
                        },
                    "OscorpsGambit" : {
                        "LevelCompletion" : SDB1[77],
                        "Perfect" : SDB1[78],
                        "DefeatedHKs" : SDB1[79],
                        "Style" : SDB1[80],
                        },
                    "TheSubwayStation" : {
                        "LevelCompletion" : SDB1[81],
                        "Time" : SDB1[82],
                        "Perfect" : SDB1[83],
                        "Style" : SDB1[84],
                        },
                    "ChaseThroughTheSewer" : {
                        "LevelCompletion" : SDB1[85],
                        "Time" : SDB1[86],
                        "SecretsFound" : SDB1[87],
                        "Combat" : SDB1[88],
                        "Style" : SDB1[89],
                        },
                    "ShowdownWithShocker" : {
                        "LevelCompletion" : SDB1[90],
                        "Time" : SDB1[91],
                        "Perfect" : SDB1[92],
                        "SecretsFound" : SDB1[93],
                        "Style" : SDB1[94],
                        },
                    "VulturesLair" : {
                        "LevelCompletion" : SDB1[95],
                        "Time" : SDB1[96],
                        "Perfect" : SDB1[97],
                        },
                    "VultureEscapes" : {
                        "LevelCompletion" : SDB1[99],
                        "Time" : SDB1[100],
                        "Perfect" : SDB1[101],
                        "VultureProximity" : SDB1[102],
                        },
                    "AirDuelWithVulture" : {
                        "LevelCompletion" : SDB1[104],
                        "Time" : SDB1[105],
                        "Perfect" : SDB1[106],
                        "Style" : SDB1[107],
                        },
                    "Corralled" : {
                        "LevelCompletion" : SDB1[108],
                        "SecretsFound" : SDB1[160],
                        "ProtectedScorpion" : SDB1[161],
                        "Style" : SDB1[162],
                        },
                    "ScorpionsRampage" : {
                        "LevelCompletion" : SDB1[109],
                        "Style" : SDB1[159],
                        "NoPickupsUsed" : SDB1[164],
                        },
                    "CoupDEtat" : {
                        "LevelCompletion" : SDB1[110],
                        "Time" : SDB1[111],
                        "Perfect" : SDB1[112],
                        "Style" : SDB1[113],
                        },
                    "TheOffer" : {
                        "LevelCompletion" : SDB1[114],
                        "Time" : SDB1[115],
                        "Perfect" : SDB1[116],
                        "Style" : SDB1[117],
                        "RideGoblin" : SDB1[167],
                        },
                    "RaceAgainstTime" : {
                        "LevelCompletion" : SDB1[118],
                        "Time" : SDB1[119],
                        "Perfect" : SDB1[120],
                        },
                    "TheRazorsEdge" : {
                        "LevelCompletion" : SDB1[129],
                        "RBatsDestroyed" : SDB1[130],
                        "RemainingHealth" : SDB1[131],
                        "PickupsUsed" : SDB1[132],
                        "Style" : SDB1[133],
                        },
                    "BreakingAndEntering" : {
                        "LevelCompletion" : SDB1[134],
                        "Time" : SDB1[135],
                        "Perfect" : SDB1[136],
                        "SecretsFound" : SDB1[137],
                        "StealthBonus" : SDB1[138],
                        },
                    "ChemicalChaos" : {
                        "LevelCompletion" : SDB1[140],
                        "Time" : SDB1[141],
                        "Perfect" : SDB1[142],
                        },
                    "OscorpsUltimateWeapon" : {
                        "LevelCompletion" : SDB1[144],
                        "Time" : SDB1[145],
                        "Perfect" : SDB1[146],
                        "Style" : SDB1[147],
                        },
                    "EscapeFromOscorp" : {
                        "LevelCompletion" : SDB1[148],
                        "Perfect" : SDB1[149],
                        "SupersoldiersKilled" : SDB1[150],
                        "Style" : SDB1[151],
                        },
                    "MaryJaneKidnapped" : {
                        "LevelCompletion" : SDB1[152],
                        "Perfect" : SDB1[153],
                        },
                    "Other" : {
                        "UnknownBonus01" : SDB1[98],
                        "UnknownBonus02" : SDB1[103],
                        "UnknownBonus03" : SDB1[121],
                        "UnknownBonus04" : SDB1[122],
                        "UnknownBonus05" : SDB1[123],
                        "UnknownBonus06" : SDB1[124],
                        "UnknownBonus07" : SDB1[125],
                        "UnknownBonus08" : SDB1[126],
                        "UnknownBonus09" : SDB1[127],
                        "UnknownBonus10" : SDB1[128],
                        "UnknownBonus11" : SDB1[139],
                        "UnknownBonus12" : SDB1[143],
                        "UnknownBonus13" : SDB1[154],
                        "UnknownBonus14" : SDB1[155],
                        "UnknownBonus15" : SDB1[156],
                        "UnknownBonus16" : SDB1[157],
                        "UnknownBonus17" : SDB1[158],
                        "UnknownBonus18" : SDB1[163],
                        "UnknownBonus19" : SDB1[165],
                        "UnknownBonus20" : SDB1[166],
                        },
                    },
                "Options" : {
                    "UnknownVolume" : SDB1[7],
                    "MusicVolume" : SDB1[8],
                    "SFXVolume" : SDB1[9],
                    "VoiceVolume" : SDB1[10],
                    "MovieVolume" : SDB1[11],
                    "CameraMode" : SDB1[171],
                    "InvertCameraLook" : SDB1[177],
                    "ControllerVibration" : SDB1[178],
                    "SwapJumpAndWebInputs" : SDB1[174],
                    "SwapZipAndSwingInputs" : SDB1[175],
                    "ControllerMovementTweak" : SDB1[176],
                    "MovementToggles" : SDB1[169],
                    "TankControls" : SDB1[170],
                    "ShowStylePoints" : SDB1[172],
                    },
                "Miscellaneous" : {
                    "MainMenuState" : SDB1[1],
                    "UnknownString01" : SDB1[173],
                    "UnknownString02" : SDB1[179],
                    },
                },
            "Slot02" : { # Slot-tailored data.
                "Baseline" : {
                    "Difficulty" : SDB2[168],
                    "ContinueLevel" : SDB2[0],
                    "UnlocksLevelUNKNOWN" : SDB2[2],
                    "UnlocksLevelEASY" : SDB2[3],
                    "UnlocksLevelNORMAL" : SDB2[4],
                    "UnlocksLevelHERO" : SDB2[5],
                    "UnlocksLevelSUPERHERO" : SDB2[6],
                    "SecretStoreToggles" : SDB2[12],
                    },
                "CombatControls" : {
                    "FieldGoal_PPK" : SDB2[13],
                    "GravitySlam_PPJ" : SDB2[14],
                    "WebHit_PPW" : SDB2[15],
                    "BackflipKick_PKK" : SDB2[16],
                    "Sting_PKP" : SDB2[17],
                    "Palm_PKJ" : SDB2[18],
                    "HighWebHit_PKW" : SDB2[19],
                    "DiveBomb_PJJ" : SDB2[20],
                    "HeadHammer_PJP" : SDB2[21],
                    "DiveKick_PJK" : SDB2[22],
                    "Uppercut_KKP" : SDB2[23],
                    "FlipMule_KKJ" : SDB2[24],
                    "LowWebHit_KKW" : SDB2[25],
                    "ScissorKick_KPK" : SDB2[26],
                    "HighStomp_KPJ" : SDB2[27],
                    "Tackle_KJJ" : SDB2[28],
                    "Handspring_KJK" : SDB2[29],
                    "Haymaker_KJP" : SDB2[30],
                    "AdvWebDome_WCKK" : SDB2[31],
                    "AdvWebGloves_WCPP" : SDB2[32],
                    "AdvImpactWeb_WCW" : SDB2[33],
                    },
                "TrainingBestTimes" : {
                    "BasicAirCombat" : [SDB2[34], SDB2[35], SDB2[36]],
                    "BasicSwingTraining" : [SDB2[37], SDB2[38], SDB2[39]],
                    "AdvancedSwingTraining" : [SDB2[40], SDB2[41], SDB2[42]],
                    "ExpertSwingTraining" : [SDB2[43], SDB2[44], SDB2[45]],
                    "BasicZipTraining" : [SDB2[46], SDB2[47], SDB2[48]],
                    "AdvancedZipTraining" : [SDB2[49], SDB2[50], SDB2[51]],
                    "ExpertZipTraining" : [SDB2[52], SDB2[53], SDB2[54]],
                    "SwingRings" : [SDB2[55], SDB2[56], SDB2[57]],
                    "SwingPlatforms" : [SDB2[58], SDB2[59], SDB2[60]],
                    "ObstacleCourse" : [SDB2[61], SDB2[62], SDB2[63]],
                    },
                "LevelBonusPoints" : {
                    "SearchForJustice" : {
                        "LevelCompletion" : SDB2[64],
                        "Perfect" : SDB2[65],
                        "Combat" : SDB2[66],
                        "SecretsFound" : SDB2[67],
                        "Style" : SDB2[68],
                        },
                    "WarehouseHunt" : {
                        "LevelCompletion" : SDB2[69],
                        "StealthBonus" : SDB2[70],
                        "SecretsFound" : SDB2[71],
                        "Style" : SDB2[72],
                        },
                    "BirthOfAHero" : {
                        "LevelCompletion" : SDB2[73],
                        "Time" : SDB2[74],
                        "SecretsFound" : SDB2[75],
                        "Style" : SDB2[76],
                        },
                    "OscorpsGambit" : {
                        "LevelCompletion" : SDB2[77],
                        "Perfect" : SDB2[78],
                        "DefeatedHKs" : SDB2[79],
                        "Style" : SDB2[80],
                        },
                    "TheSubwayStation" : {
                        "LevelCompletion" : SDB2[81],
                        "Time" : SDB2[82],
                        "Perfect" : SDB2[83],
                        "Style" : SDB2[84],
                        },
                    "ChaseThroughTheSewer" : {
                        "LevelCompletion" : SDB2[85],
                        "Time" : SDB2[86],
                        "SecretsFound" : SDB2[87],
                        "Combat" : SDB2[88],
                        "Style" : SDB2[89],
                        },
                    "ShowdownWithShocker" : {
                        "LevelCompletion" : SDB2[90],
                        "Time" : SDB2[91],
                        "Perfect" : SDB2[92],
                        "SecretsFound" : SDB2[93],
                        "Style" : SDB2[94],
                        },
                    "VulturesLair" : {
                        "LevelCompletion" : SDB2[95],
                        "Time" : SDB2[96],
                        "Perfect" : SDB2[97],
                        },
                    "VultureEscapes" : {
                        "LevelCompletion" : SDB2[99],
                        "Time" : SDB2[100],
                        "Perfect" : SDB2[101],
                        "VultureProximity" : SDB2[102],
                        },
                    "AirDuelWithVulture" : {
                        "LevelCompletion" : SDB2[104],
                        "Time" : SDB2[105],
                        "Perfect" : SDB2[106],
                        "Style" : SDB2[107],
                        },
                    "Corralled" : {
                        "LevelCompletion" : SDB2[108],
                        "SecretsFound" : SDB2[160],
                        "ProtectedScorpion" : SDB2[161],
                        "Style" : SDB2[162],
                        },
                    "ScorpionsRampage" : {
                        "LevelCompletion" : SDB2[109],
                        "Style" : SDB2[159],
                        "NoPickupsUsed" : SDB2[164],
                        },
                    "CoupDEtat" : {
                        "LevelCompletion" : SDB2[110],
                        "Time" : SDB2[111],
                        "Perfect" : SDB2[112],
                        "Style" : SDB2[113],
                        },
                    "TheOffer" : {
                        "LevelCompletion" : SDB2[114],
                        "Time" : SDB2[115],
                        "Perfect" : SDB2[116],
                        "Style" : SDB2[117],
                        "RideGoblin" : SDB2[167],
                        },
                    "RaceAgainstTime" : {
                        "LevelCompletion" : SDB2[118],
                        "Time" : SDB2[119],
                        "Perfect" : SDB2[120],
                        },
                    "TheRazorsEdge" : {
                        "LevelCompletion" : SDB2[129],
                        "RBatsDestroyed" : SDB2[130],
                        "RemainingHealth" : SDB2[131],
                        "PickupsUsed" : SDB2[132],
                        "Style" : SDB2[133],
                        },
                    "BreakingAndEntering" : {
                        "LevelCompletion" : SDB2[134],
                        "Time" : SDB2[135],
                        "Perfect" : SDB2[136],
                        "SecretsFound" : SDB2[137],
                        "StealthBonus" : SDB2[138],
                        },
                    "ChemicalChaos" : {
                        "LevelCompletion" : SDB2[140],
                        "Time" : SDB2[141],
                        "Perfect" : SDB2[142],
                        },
                    "OscorpsUltimateWeapon" : {
                        "LevelCompletion" : SDB2[144],
                        "Time" : SDB2[145],
                        "Perfect" : SDB2[146],
                        "Style" : SDB2[147],
                        },
                    "EscapeFromOscorp" : {
                        "LevelCompletion" : SDB2[148],
                        "Perfect" : SDB2[149],
                        "SupersoldiersKilled" : SDB2[150],
                        "Style" : SDB2[151],
                        },
                    "MaryJaneKidnapped" : {
                        "LevelCompletion" : SDB2[152],
                        "Perfect" : SDB2[153],
                        },
                    "Other" : {
                        "UnknownBonus01" : SDB2[98],
                        "UnknownBonus02" : SDB2[103],
                        "UnknownBonus03" : SDB2[121],
                        "UnknownBonus04" : SDB2[122],
                        "UnknownBonus05" : SDB2[123],
                        "UnknownBonus06" : SDB2[124],
                        "UnknownBonus07" : SDB2[125],
                        "UnknownBonus08" : SDB2[126],
                        "UnknownBonus09" : SDB2[127],
                        "UnknownBonus10" : SDB2[128],
                        "UnknownBonus11" : SDB2[139],
                        "UnknownBonus12" : SDB2[143],
                        "UnknownBonus13" : SDB2[154],
                        "UnknownBonus14" : SDB2[155],
                        "UnknownBonus15" : SDB2[156],
                        "UnknownBonus16" : SDB2[157],
                        "UnknownBonus17" : SDB2[158],
                        "UnknownBonus18" : SDB2[163],
                        "UnknownBonus19" : SDB2[165],
                        "UnknownBonus20" : SDB2[166],
                        },
                    },
                "Options" : {
                    "UnknownVolume" : SDB2[7],
                    "MusicVolume" : SDB2[8],
                    "SFXVolume" : SDB2[9],
                    "VoiceVolume" : SDB2[10],
                    "MovieVolume" : SDB2[11],
                    "CameraMode" : SDB2[171],
                    "InvertCameraLook" : SDB2[177],
                    "ControllerVibration" : SDB2[178],
                    "SwapJumpAndWebInputs" : SDB2[174],
                    "SwapZipAndSwingInputs" : SDB2[175],
                    "ControllerMovementTweak" : SDB2[176],
                    "MovementToggles" : SDB2[169],
                    "TankControls" : SDB2[170],
                    "ShowStylePoints" : SDB2[172],
                    },
                "Miscellaneous" : {
                    "MainMenuState" : SDB2[1],
                    "UnknownString01" : SDB2[173],
                    "UnknownString02" : SDB2[179],
                    },
                },
            "Slot03" : { # Slot-tailored data.
                "Baseline" : {
                    "Difficulty" : SDB3[168],
                    "ContinueLevel" : SDB3[0],
                    "UnlocksLevelUNKNOWN" : SDB3[2],
                    "UnlocksLevelEASY" : SDB3[3],
                    "UnlocksLevelNORMAL" : SDB3[4],
                    "UnlocksLevelHERO" : SDB3[5],
                    "UnlocksLevelSUPERHERO" : SDB3[6],
                    "SecretStoreToggles" : SDB3[12],
                    },
                "CombatControls" : {
                    "FieldGoal_PPK" : SDB3[13],
                    "GravitySlam_PPJ" : SDB3[14],
                    "WebHit_PPW" : SDB3[15],
                    "BackflipKick_PKK" : SDB3[16],
                    "Sting_PKP" : SDB3[17],
                    "Palm_PKJ" : SDB3[18],
                    "HighWebHit_PKW" : SDB3[19],
                    "DiveBomb_PJJ" : SDB3[20],
                    "HeadHammer_PJP" : SDB3[21],
                    "DiveKick_PJK" : SDB3[22],
                    "Uppercut_KKP" : SDB3[23],
                    "FlipMule_KKJ" : SDB3[24],
                    "LowWebHit_KKW" : SDB3[25],
                    "ScissorKick_KPK" : SDB3[26],
                    "HighStomp_KPJ" : SDB3[27],
                    "Tackle_KJJ" : SDB3[28],
                    "Handspring_KJK" : SDB3[29],
                    "Haymaker_KJP" : SDB3[30],
                    "AdvWebDome_WCKK" : SDB3[31],
                    "AdvWebGloves_WCPP" : SDB3[32],
                    "AdvImpactWeb_WCW" : SDB3[33],
                    },
                "TrainingBestTimes" : {
                    "BasicAirCombat" : [SDB3[34], SDB3[35], SDB3[36]],
                    "BasicSwingTraining" : [SDB3[37], SDB3[38], SDB3[39]],
                    "AdvancedSwingTraining" : [SDB3[40], SDB3[41], SDB3[42]],
                    "ExpertSwingTraining" : [SDB3[43], SDB3[44], SDB3[45]],
                    "BasicZipTraining" : [SDB3[46], SDB3[47], SDB3[48]],
                    "AdvancedZipTraining" : [SDB3[49], SDB3[50], SDB3[51]],
                    "ExpertZipTraining" : [SDB3[52], SDB3[53], SDB3[54]],
                    "SwingRings" : [SDB3[55], SDB3[56], SDB3[57]],
                    "SwingPlatforms" : [SDB3[58], SDB3[59], SDB3[60]],
                    "ObstacleCourse" : [SDB3[61], SDB3[62], SDB3[63]],
                    },
                "LevelBonusPoints" : {
                    "SearchForJustice" : {
                        "LevelCompletion" : SDB3[64],
                        "Perfect" : SDB3[65],
                        "Combat" : SDB3[66],
                        "SecretsFound" : SDB3[67],
                        "Style" : SDB3[68],
                        },
                    "WarehouseHunt" : {
                        "LevelCompletion" : SDB3[69],
                        "StealthBonus" : SDB3[70],
                        "SecretsFound" : SDB3[71],
                        "Style" : SDB3[72],
                        },
                    "BirthOfAHero" : {
                        "LevelCompletion" : SDB3[73],
                        "Time" : SDB3[74],
                        "SecretsFound" : SDB3[75],
                        "Style" : SDB3[76],
                        },
                    "OscorpsGambit" : {
                        "LevelCompletion" : SDB3[77],
                        "Perfect" : SDB3[78],
                        "DefeatedHKs" : SDB3[79],
                        "Style" : SDB3[80],
                        },
                    "TheSubwayStation" : {
                        "LevelCompletion" : SDB3[81],
                        "Time" : SDB3[82],
                        "Perfect" : SDB3[83],
                        "Style" : SDB3[84],
                        },
                    "ChaseThroughTheSewer" : {
                        "LevelCompletion" : SDB3[85],
                        "Time" : SDB3[86],
                        "SecretsFound" : SDB3[87],
                        "Combat" : SDB3[88],
                        "Style" : SDB3[89],
                        },
                    "ShowdownWithShocker" : {
                        "LevelCompletion" : SDB3[90],
                        "Time" : SDB3[91],
                        "Perfect" : SDB3[92],
                        "SecretsFound" : SDB3[93],
                        "Style" : SDB3[94],
                        },
                    "VulturesLair" : {
                        "LevelCompletion" : SDB3[95],
                        "Time" : SDB3[96],
                        "Perfect" : SDB3[97],
                        },
                    "VultureEscapes" : {
                        "LevelCompletion" : SDB3[99],
                        "Time" : SDB3[100],
                        "Perfect" : SDB3[101],
                        "VultureProximity" : SDB3[102],
                        },
                    "AirDuelWithVulture" : {
                        "LevelCompletion" : SDB3[104],
                        "Time" : SDB3[105],
                        "Perfect" : SDB3[106],
                        "Style" : SDB3[107],
                        },
                    "Corralled" : {
                        "LevelCompletion" : SDB3[108],
                        "SecretsFound" : SDB3[160],
                        "ProtectedScorpion" : SDB3[161],
                        "Style" : SDB3[162],
                        },
                    "ScorpionsRampage" : {
                        "LevelCompletion" : SDB3[109],
                        "Style" : SDB3[159],
                        "NoPickupsUsed" : SDB3[164],
                        },
                    "CoupDEtat" : {
                        "LevelCompletion" : SDB3[110],
                        "Time" : SDB3[111],
                        "Perfect" : SDB3[112],
                        "Style" : SDB3[113],
                        },
                    "TheOffer" : {
                        "LevelCompletion" : SDB3[114],
                        "Time" : SDB3[115],
                        "Perfect" : SDB3[116],
                        "Style" : SDB3[117],
                        "RideGoblin" : SDB3[167],
                        },
                    "RaceAgainstTime" : {
                        "LevelCompletion" : SDB3[118],
                        "Time" : SDB3[119],
                        "Perfect" : SDB3[120],
                        },
                    "TheRazorsEdge" : {
                        "LevelCompletion" : SDB3[129],
                        "RBatsDestroyed" : SDB3[130],
                        "RemainingHealth" : SDB3[131],
                        "PickupsUsed" : SDB3[132],
                        "Style" : SDB3[133],
                        },
                    "BreakingAndEntering" : {
                        "LevelCompletion" : SDB3[134],
                        "Time" : SDB3[135],
                        "Perfect" : SDB3[136],
                        "SecretsFound" : SDB3[137],
                        "StealthBonus" : SDB3[138],
                        },
                    "ChemicalChaos" : {
                        "LevelCompletion" : SDB3[140],
                        "Time" : SDB3[141],
                        "Perfect" : SDB3[142],
                        },
                    "OscorpsUltimateWeapon" : {
                        "LevelCompletion" : SDB3[144],
                        "Time" : SDB3[145],
                        "Perfect" : SDB3[146],
                        "Style" : SDB3[147],
                        },
                    "EscapeFromOscorp" : {
                        "LevelCompletion" : SDB3[148],
                        "Perfect" : SDB3[149],
                        "SupersoldiersKilled" : SDB3[150],
                        "Style" : SDB3[151],
                        },
                    "MaryJaneKidnapped" : {
                        "LevelCompletion" : SDB3[152],
                        "Perfect" : SDB3[153],
                        },
                    "Other" : {
                        "UnknownBonus01" : SDB3[98],
                        "UnknownBonus02" : SDB3[103],
                        "UnknownBonus03" : SDB3[121],
                        "UnknownBonus04" : SDB3[122],
                        "UnknownBonus05" : SDB3[123],
                        "UnknownBonus06" : SDB3[124],
                        "UnknownBonus07" : SDB3[125],
                        "UnknownBonus08" : SDB3[126],
                        "UnknownBonus09" : SDB3[127],
                        "UnknownBonus10" : SDB3[128],
                        "UnknownBonus11" : SDB3[139],
                        "UnknownBonus12" : SDB3[143],
                        "UnknownBonus13" : SDB3[154],
                        "UnknownBonus14" : SDB3[155],
                        "UnknownBonus15" : SDB3[156],
                        "UnknownBonus16" : SDB3[157],
                        "UnknownBonus17" : SDB3[158],
                        "UnknownBonus18" : SDB3[163],
                        "UnknownBonus19" : SDB3[165],
                        "UnknownBonus20" : SDB3[166],
                        },
                    },
                "Options" : {
                    "UnknownVolume" : SDB3[7],
                    "MusicVolume" : SDB3[8],
                    "SFXVolume" : SDB3[9],
                    "VoiceVolume" : SDB3[10],
                    "MovieVolume" : SDB3[11],
                    "CameraMode" : SDB3[171],
                    "InvertCameraLook" : SDB3[177],
                    "ControllerVibration" : SDB3[178],
                    "SwapJumpAndWebInputs" : SDB3[174],
                    "SwapZipAndSwingInputs" : SDB3[175],
                    "ControllerMovementTweak" : SDB3[176],
                    "MovementToggles" : SDB3[169],
                    "TankControls" : SDB3[170],
                    "ShowStylePoints" : SDB3[172],
                    },
                "Miscellaneous" : {
                    "MainMenuState" : SDB3[1],
                    "UnknownString01" : SDB3[173],
                    "UnknownString02" : SDB3[179],
                    },
                },
            "Slot04" : { # Slot-tailored data.
                "Baseline" : {
                    "Difficulty" : SDB4[168],
                    "ContinueLevel" : SDB4[0],
                    "UnlocksLevelUNKNOWN" : SDB4[2],
                    "UnlocksLevelEASY" : SDB4[3],
                    "UnlocksLevelNORMAL" : SDB4[4],
                    "UnlocksLevelHERO" : SDB4[5],
                    "UnlocksLevelSUPERHERO" : SDB4[6],
                    "SecretStoreToggles" : SDB4[12],
                    },
                "CombatControls" : {
                    "FieldGoal_PPK" : SDB4[13],
                    "GravitySlam_PPJ" : SDB4[14],
                    "WebHit_PPW" : SDB4[15],
                    "BackflipKick_PKK" : SDB4[16],
                    "Sting_PKP" : SDB4[17],
                    "Palm_PKJ" : SDB4[18],
                    "HighWebHit_PKW" : SDB4[19],
                    "DiveBomb_PJJ" : SDB4[20],
                    "HeadHammer_PJP" : SDB4[21],
                    "DiveKick_PJK" : SDB4[22],
                    "Uppercut_KKP" : SDB4[23],
                    "FlipMule_KKJ" : SDB4[24],
                    "LowWebHit_KKW" : SDB4[25],
                    "ScissorKick_KPK" : SDB4[26],
                    "HighStomp_KPJ" : SDB4[27],
                    "Tackle_KJJ" : SDB4[28],
                    "Handspring_KJK" : SDB4[29],
                    "Haymaker_KJP" : SDB4[30],
                    "AdvWebDome_WCKK" : SDB4[31],
                    "AdvWebGloves_WCPP" : SDB4[32],
                    "AdvImpactWeb_WCW" : SDB4[33],
                    },
                "TrainingBestTimes" : {
                    "BasicAirCombat" : [SDB4[34], SDB4[35], SDB4[36]],
                    "BasicSwingTraining" : [SDB4[37], SDB4[38], SDB4[39]],
                    "AdvancedSwingTraining" : [SDB4[40], SDB4[41], SDB4[42]],
                    "ExpertSwingTraining" : [SDB4[43], SDB4[44], SDB4[45]],
                    "BasicZipTraining" : [SDB4[46], SDB4[47], SDB4[48]],
                    "AdvancedZipTraining" : [SDB4[49], SDB4[50], SDB4[51]],
                    "ExpertZipTraining" : [SDB4[52], SDB4[53], SDB4[54]],
                    "SwingRings" : [SDB4[55], SDB4[56], SDB4[57]],
                    "SwingPlatforms" : [SDB4[58], SDB4[59], SDB4[60]],
                    "ObstacleCourse" : [SDB4[61], SDB4[62], SDB4[63]],
                    },
                "LevelBonusPoints" : {
                    "SearchForJustice" : {
                        "LevelCompletion" : SDB4[64],
                        "Perfect" : SDB4[65],
                        "Combat" : SDB4[66],
                        "SecretsFound" : SDB4[67],
                        "Style" : SDB4[68],
                        },
                    "WarehouseHunt" : {
                        "LevelCompletion" : SDB4[69],
                        "StealthBonus" : SDB4[70],
                        "SecretsFound" : SDB4[71],
                        "Style" : SDB4[72],
                        },
                    "BirthOfAHero" : {
                        "LevelCompletion" : SDB4[73],
                        "Time" : SDB4[74],
                        "SecretsFound" : SDB4[75],
                        "Style" : SDB4[76],
                        },
                    "OscorpsGambit" : {
                        "LevelCompletion" : SDB4[77],
                        "Perfect" : SDB4[78],
                        "DefeatedHKs" : SDB4[79],
                        "Style" : SDB4[80],
                        },
                    "TheSubwayStation" : {
                        "LevelCompletion" : SDB4[81],
                        "Time" : SDB4[82],
                        "Perfect" : SDB4[83],
                        "Style" : SDB4[84],
                        },
                    "ChaseThroughTheSewer" : {
                        "LevelCompletion" : SDB4[85],
                        "Time" : SDB4[86],
                        "SecretsFound" : SDB4[87],
                        "Combat" : SDB4[88],
                        "Style" : SDB4[89],
                        },
                    "ShowdownWithShocker" : {
                        "LevelCompletion" : SDB4[90],
                        "Time" : SDB4[91],
                        "Perfect" : SDB4[92],
                        "SecretsFound" : SDB4[93],
                        "Style" : SDB4[94],
                        },
                    "VulturesLair" : {
                        "LevelCompletion" : SDB4[95],
                        "Time" : SDB4[96],
                        "Perfect" : SDB4[97],
                        },
                    "VultureEscapes" : {
                        "LevelCompletion" : SDB4[99],
                        "Time" : SDB4[100],
                        "Perfect" : SDB4[101],
                        "VultureProximity" : SDB4[102],
                        },
                    "AirDuelWithVulture" : {
                        "LevelCompletion" : SDB4[104],
                        "Time" : SDB4[105],
                        "Perfect" : SDB4[106],
                        "Style" : SDB4[107],
                        },
                    "Corralled" : {
                        "LevelCompletion" : SDB4[108],
                        "SecretsFound" : SDB4[160],
                        "ProtectedScorpion" : SDB4[161],
                        "Style" : SDB4[162],
                        },
                    "ScorpionsRampage" : {
                        "LevelCompletion" : SDB4[109],
                        "Style" : SDB4[159],
                        "NoPickupsUsed" : SDB4[164],
                        },
                    "CoupDEtat" : {
                        "LevelCompletion" : SDB4[110],
                        "Time" : SDB4[111],
                        "Perfect" : SDB4[112],
                        "Style" : SDB4[113],
                        },
                    "TheOffer" : {
                        "LevelCompletion" : SDB4[114],
                        "Time" : SDB4[115],
                        "Perfect" : SDB4[116],
                        "Style" : SDB4[117],
                        "RideGoblin" : SDB4[167],
                        },
                    "RaceAgainstTime" : {
                        "LevelCompletion" : SDB4[118],
                        "Time" : SDB4[119],
                        "Perfect" : SDB4[120],
                        },
                    "TheRazorsEdge" : {
                        "LevelCompletion" : SDB4[129],
                        "RBatsDestroyed" : SDB4[130],
                        "RemainingHealth" : SDB4[131],
                        "PickupsUsed" : SDB4[132],
                        "Style" : SDB4[133],
                        },
                    "BreakingAndEntering" : {
                        "LevelCompletion" : SDB4[134],
                        "Time" : SDB4[135],
                        "Perfect" : SDB4[136],
                        "SecretsFound" : SDB4[137],
                        "StealthBonus" : SDB4[138],
                        },
                    "ChemicalChaos" : {
                        "LevelCompletion" : SDB4[140],
                        "Time" : SDB4[141],
                        "Perfect" : SDB4[142],
                        },
                    "OscorpsUltimateWeapon" : {
                        "LevelCompletion" : SDB4[144],
                        "Time" : SDB4[145],
                        "Perfect" : SDB4[146],
                        "Style" : SDB4[147],
                        },
                    "EscapeFromOscorp" : {
                        "LevelCompletion" : SDB4[148],
                        "Perfect" : SDB4[149],
                        "SupersoldiersKilled" : SDB4[150],
                        "Style" : SDB4[151],
                        },
                    "MaryJaneKidnapped" : {
                        "LevelCompletion" : SDB4[152],
                        "Perfect" : SDB4[153],
                        },
                    "Other" : {
                        "UnknownBonus01" : SDB4[98],
                        "UnknownBonus02" : SDB4[103],
                        "UnknownBonus03" : SDB4[121],
                        "UnknownBonus04" : SDB4[122],
                        "UnknownBonus05" : SDB4[123],
                        "UnknownBonus06" : SDB4[124],
                        "UnknownBonus07" : SDB4[125],
                        "UnknownBonus08" : SDB4[126],
                        "UnknownBonus09" : SDB4[127],
                        "UnknownBonus10" : SDB4[128],
                        "UnknownBonus11" : SDB4[139],
                        "UnknownBonus12" : SDB4[143],
                        "UnknownBonus13" : SDB4[154],
                        "UnknownBonus14" : SDB4[155],
                        "UnknownBonus15" : SDB4[156],
                        "UnknownBonus16" : SDB4[157],
                        "UnknownBonus17" : SDB4[158],
                        "UnknownBonus18" : SDB4[163],
                        "UnknownBonus19" : SDB4[165],
                        "UnknownBonus20" : SDB4[166],
                        },
                    },
                "Options" : {
                    "UnknownVolume" : SDB4[7],
                    "MusicVolume" : SDB4[8],
                    "SFXVolume" : SDB4[9],
                    "VoiceVolume" : SDB4[10],
                    "MovieVolume" : SDB4[11],
                    "CameraMode" : SDB4[171],
                    "InvertCameraLook" : SDB4[177],
                    "ControllerVibration" : SDB4[178],
                    "SwapJumpAndWebInputs" : SDB4[174],
                    "SwapZipAndSwingInputs" : SDB4[175],
                    "ControllerMovementTweak" : SDB4[176],
                    "MovementToggles" : SDB4[169],
                    "TankControls" : SDB4[170],
                    "ShowStylePoints" : SDB4[172],
                    },
                "Miscellaneous" : {
                    "MainMenuState" : SDB4[1],
                    "UnknownString01" : SDB4[173],
                    "UnknownString02" : SDB4[179],
                    },
                },
            "Slot05" : { # Slot-tailored data.
                "Baseline" : {
                    "Difficulty" : SDB5[168],
                    "ContinueLevel" : SDB5[0],
                    "UnlocksLevelUNKNOWN" : SDB5[2],
                    "UnlocksLevelEASY" : SDB5[3],
                    "UnlocksLevelNORMAL" : SDB5[4],
                    "UnlocksLevelHERO" : SDB5[5],
                    "UnlocksLevelSUPERHERO" : SDB5[6],
                    "SecretStoreToggles" : SDB5[12],
                    },
                "CombatControls" : {
                    "FieldGoal_PPK" : SDB5[13],
                    "GravitySlam_PPJ" : SDB5[14],
                    "WebHit_PPW" : SDB5[15],
                    "BackflipKick_PKK" : SDB5[16],
                    "Sting_PKP" : SDB5[17],
                    "Palm_PKJ" : SDB5[18],
                    "HighWebHit_PKW" : SDB5[19],
                    "DiveBomb_PJJ" : SDB5[20],
                    "HeadHammer_PJP" : SDB5[21],
                    "DiveKick_PJK" : SDB5[22],
                    "Uppercut_KKP" : SDB5[23],
                    "FlipMule_KKJ" : SDB5[24],
                    "LowWebHit_KKW" : SDB5[25],
                    "ScissorKick_KPK" : SDB5[26],
                    "HighStomp_KPJ" : SDB5[27],
                    "Tackle_KJJ" : SDB5[28],
                    "Handspring_KJK" : SDB5[29],
                    "Haymaker_KJP" : SDB5[30],
                    "AdvWebDome_WCKK" : SDB5[31],
                    "AdvWebGloves_WCPP" : SDB5[32],
                    "AdvImpactWeb_WCW" : SDB5[33],
                    },
                "TrainingBestTimes" : {
                    "BasicAirCombat" : [SDB5[34], SDB5[35], SDB5[36]],
                    "BasicSwingTraining" : [SDB5[37], SDB5[38], SDB5[39]],
                    "AdvancedSwingTraining" : [SDB5[40], SDB5[41], SDB5[42]],
                    "ExpertSwingTraining" : [SDB5[43], SDB5[44], SDB5[45]],
                    "BasicZipTraining" : [SDB5[46], SDB5[47], SDB5[48]],
                    "AdvancedZipTraining" : [SDB5[49], SDB5[50], SDB5[51]],
                    "ExpertZipTraining" : [SDB5[52], SDB5[53], SDB5[54]],
                    "SwingRings" : [SDB5[55], SDB5[56], SDB5[57]],
                    "SwingPlatforms" : [SDB5[58], SDB5[59], SDB5[60]],
                    "ObstacleCourse" : [SDB5[61], SDB5[62], SDB5[63]],
                    },
                "LevelBonusPoints" : {
                    "SearchForJustice" : {
                        "LevelCompletion" : SDB5[64],
                        "Perfect" : SDB5[65],
                        "Combat" : SDB5[66],
                        "SecretsFound" : SDB5[67],
                        "Style" : SDB5[68],
                        },
                    "WarehouseHunt" : {
                        "LevelCompletion" : SDB5[69],
                        "StealthBonus" : SDB5[70],
                        "SecretsFound" : SDB5[71],
                        "Style" : SDB5[72],
                        },
                    "BirthOfAHero" : {
                        "LevelCompletion" : SDB5[73],
                        "Time" : SDB5[74],
                        "SecretsFound" : SDB5[75],
                        "Style" : SDB5[76],
                        },
                    "OscorpsGambit" : {
                        "LevelCompletion" : SDB5[77],
                        "Perfect" : SDB5[78],
                        "DefeatedHKs" : SDB5[79],
                        "Style" : SDB5[80],
                        },
                    "TheSubwayStation" : {
                        "LevelCompletion" : SDB5[81],
                        "Time" : SDB5[82],
                        "Perfect" : SDB5[83],
                        "Style" : SDB5[84],
                        },
                    "ChaseThroughTheSewer" : {
                        "LevelCompletion" : SDB5[85],
                        "Time" : SDB5[86],
                        "SecretsFound" : SDB5[87],
                        "Combat" : SDB5[88],
                        "Style" : SDB5[89],
                        },
                    "ShowdownWithShocker" : {
                        "LevelCompletion" : SDB5[90],
                        "Time" : SDB5[91],
                        "Perfect" : SDB5[92],
                        "SecretsFound" : SDB5[93],
                        "Style" : SDB5[94],
                        },
                    "VulturesLair" : {
                        "LevelCompletion" : SDB5[95],
                        "Time" : SDB5[96],
                        "Perfect" : SDB5[97],
                        },
                    "VultureEscapes" : {
                        "LevelCompletion" : SDB5[99],
                        "Time" : SDB5[100],
                        "Perfect" : SDB5[101],
                        "VultureProximity" : SDB5[102],
                        },
                    "AirDuelWithVulture" : {
                        "LevelCompletion" : SDB5[104],
                        "Time" : SDB5[105],
                        "Perfect" : SDB5[106],
                        "Style" : SDB5[107],
                        },
                    "Corralled" : {
                        "LevelCompletion" : SDB5[108],
                        "SecretsFound" : SDB5[160],
                        "ProtectedScorpion" : SDB5[161],
                        "Style" : SDB5[162],
                        },
                    "ScorpionsRampage" : {
                        "LevelCompletion" : SDB5[109],
                        "Style" : SDB5[159],
                        "NoPickupsUsed" : SDB5[164],
                        },
                    "CoupDEtat" : {
                        "LevelCompletion" : SDB5[110],
                        "Time" : SDB5[111],
                        "Perfect" : SDB5[112],
                        "Style" : SDB5[113],
                        },
                    "TheOffer" : {
                        "LevelCompletion" : SDB5[114],
                        "Time" : SDB5[115],
                        "Perfect" : SDB5[116],
                        "Style" : SDB5[117],
                        "RideGoblin" : SDB5[167],
                        },
                    "RaceAgainstTime" : {
                        "LevelCompletion" : SDB5[118],
                        "Time" : SDB5[119],
                        "Perfect" : SDB5[120],
                        },
                    "TheRazorsEdge" : {
                        "LevelCompletion" : SDB5[129],
                        "RBatsDestroyed" : SDB5[130],
                        "RemainingHealth" : SDB5[131],
                        "PickupsUsed" : SDB5[132],
                        "Style" : SDB5[133],
                        },
                    "BreakingAndEntering" : {
                        "LevelCompletion" : SDB5[134],
                        "Time" : SDB5[135],
                        "Perfect" : SDB5[136],
                        "SecretsFound" : SDB5[137],
                        "StealthBonus" : SDB5[138],
                        },
                    "ChemicalChaos" : {
                        "LevelCompletion" : SDB5[140],
                        "Time" : SDB5[141],
                        "Perfect" : SDB5[142],
                        },
                    "OscorpsUltimateWeapon" : {
                        "LevelCompletion" : SDB5[144],
                        "Time" : SDB5[145],
                        "Perfect" : SDB5[146],
                        "Style" : SDB5[147],
                        },
                    "EscapeFromOscorp" : {
                        "LevelCompletion" : SDB5[148],
                        "Perfect" : SDB5[149],
                        "SupersoldiersKilled" : SDB5[150],
                        "Style" : SDB5[151],
                        },
                    "MaryJaneKidnapped" : {
                        "LevelCompletion" : SDB5[152],
                        "Perfect" : SDB5[153],
                        },
                    "Other" : {
                        "UnknownBonus01" : SDB5[98],
                        "UnknownBonus02" : SDB5[103],
                        "UnknownBonus03" : SDB5[121],
                        "UnknownBonus04" : SDB5[122],
                        "UnknownBonus05" : SDB5[123],
                        "UnknownBonus06" : SDB5[124],
                        "UnknownBonus07" : SDB5[125],
                        "UnknownBonus08" : SDB5[126],
                        "UnknownBonus09" : SDB5[127],
                        "UnknownBonus10" : SDB5[128],
                        "UnknownBonus11" : SDB5[139],
                        "UnknownBonus12" : SDB5[143],
                        "UnknownBonus13" : SDB5[154],
                        "UnknownBonus14" : SDB5[155],
                        "UnknownBonus15" : SDB5[156],
                        "UnknownBonus16" : SDB5[157],
                        "UnknownBonus17" : SDB5[158],
                        "UnknownBonus18" : SDB5[163],
                        "UnknownBonus19" : SDB5[165],
                        "UnknownBonus20" : SDB5[166],
                        },
                    },
                "Options" : {
                    "UnknownVolume" : SDB5[7],
                    "MusicVolume" : SDB5[8],
                    "SFXVolume" : SDB5[9],
                    "VoiceVolume" : SDB5[10],
                    "MovieVolume" : SDB5[11],
                    "CameraMode" : SDB5[171],
                    "InvertCameraLook" : SDB5[177],
                    "ControllerVibration" : SDB5[178],
                    "SwapJumpAndWebInputs" : SDB5[174],
                    "SwapZipAndSwingInputs" : SDB5[175],
                    "ControllerMovementTweak" : SDB5[176],
                    "MovementToggles" : SDB5[169],
                    "TankControls" : SDB5[170],
                    "ShowStylePoints" : SDB5[172],
                    },
                "Miscellaneous" : {
                    "MainMenuState" : SDB5[1],
                    "UnknownString01" : SDB5[173],
                    "UnknownString02" : SDB5[179],
                    },
                },
            "Slot06" : { # Slot-tailored data.
                "Baseline" : {
                    "Difficulty" : SDB6[168],
                    "ContinueLevel" : SDB6[0],
                    "UnlocksLevelUNKNOWN" : SDB6[2],
                    "UnlocksLevelEASY" : SDB6[3],
                    "UnlocksLevelNORMAL" : SDB6[4],
                    "UnlocksLevelHERO" : SDB6[5],
                    "UnlocksLevelSUPERHERO" : SDB6[6],
                    "SecretStoreToggles" : SDB6[12],
                    },
                "CombatControls" : {
                    "FieldGoal_PPK" : SDB6[13],
                    "GravitySlam_PPJ" : SDB6[14],
                    "WebHit_PPW" : SDB6[15],
                    "BackflipKick_PKK" : SDB6[16],
                    "Sting_PKP" : SDB6[17],
                    "Palm_PKJ" : SDB6[18],
                    "HighWebHit_PKW" : SDB6[19],
                    "DiveBomb_PJJ" : SDB6[20],
                    "HeadHammer_PJP" : SDB6[21],
                    "DiveKick_PJK" : SDB6[22],
                    "Uppercut_KKP" : SDB6[23],
                    "FlipMule_KKJ" : SDB6[24],
                    "LowWebHit_KKW" : SDB6[25],
                    "ScissorKick_KPK" : SDB6[26],
                    "HighStomp_KPJ" : SDB6[27],
                    "Tackle_KJJ" : SDB6[28],
                    "Handspring_KJK" : SDB6[29],
                    "Haymaker_KJP" : SDB6[30],
                    "AdvWebDome_WCKK" : SDB6[31],
                    "AdvWebGloves_WCPP" : SDB6[32],
                    "AdvImpactWeb_WCW" : SDB6[33],
                    },
                "TrainingBestTimes" : {
                    "BasicAirCombat" : [SDB6[34], SDB6[35], SDB6[36]],
                    "BasicSwingTraining" : [SDB6[37], SDB6[38], SDB6[39]],
                    "AdvancedSwingTraining" : [SDB6[40], SDB6[41], SDB6[42]],
                    "ExpertSwingTraining" : [SDB6[43], SDB6[44], SDB6[45]],
                    "BasicZipTraining" : [SDB6[46], SDB6[47], SDB6[48]],
                    "AdvancedZipTraining" : [SDB6[49], SDB6[50], SDB6[51]],
                    "ExpertZipTraining" : [SDB6[52], SDB6[53], SDB6[54]],
                    "SwingRings" : [SDB6[55], SDB6[56], SDB6[57]],
                    "SwingPlatforms" : [SDB6[58], SDB6[59], SDB6[60]],
                    "ObstacleCourse" : [SDB6[61], SDB6[62], SDB6[63]],
                    },
                "LevelBonusPoints" : {
                    "SearchForJustice" : {
                        "LevelCompletion" : SDB6[64],
                        "Perfect" : SDB6[65],
                        "Combat" : SDB6[66],
                        "SecretsFound" : SDB6[67],
                        "Style" : SDB6[68],
                        },
                    "WarehouseHunt" : {
                        "LevelCompletion" : SDB6[69],
                        "StealthBonus" : SDB6[70],
                        "SecretsFound" : SDB6[71],
                        "Style" : SDB6[72],
                        },
                    "BirthOfAHero" : {
                        "LevelCompletion" : SDB6[73],
                        "Time" : SDB6[74],
                        "SecretsFound" : SDB6[75],
                        "Style" : SDB6[76],
                        },
                    "OscorpsGambit" : {
                        "LevelCompletion" : SDB6[77],
                        "Perfect" : SDB6[78],
                        "DefeatedHKs" : SDB6[79],
                        "Style" : SDB6[80],
                        },
                    "TheSubwayStation" : {
                        "LevelCompletion" : SDB6[81],
                        "Time" : SDB6[82],
                        "Perfect" : SDB6[83],
                        "Style" : SDB6[84],
                        },
                    "ChaseThroughTheSewer" : {
                        "LevelCompletion" : SDB6[85],
                        "Time" : SDB6[86],
                        "SecretsFound" : SDB6[87],
                        "Combat" : SDB6[88],
                        "Style" : SDB6[89],
                        },
                    "ShowdownWithShocker" : {
                        "LevelCompletion" : SDB6[90],
                        "Time" : SDB6[91],
                        "Perfect" : SDB6[92],
                        "SecretsFound" : SDB6[93],
                        "Style" : SDB6[94],
                        },
                    "VulturesLair" : {
                        "LevelCompletion" : SDB6[95],
                        "Time" : SDB6[96],
                        "Perfect" : SDB6[97],
                        },
                    "VultureEscapes" : {
                        "LevelCompletion" : SDB6[99],
                        "Time" : SDB6[100],
                        "Perfect" : SDB6[101],
                        "VultureProximity" : SDB6[102],
                        },
                    "AirDuelWithVulture" : {
                        "LevelCompletion" : SDB6[104],
                        "Time" : SDB6[105],
                        "Perfect" : SDB6[106],
                        "Style" : SDB6[107],
                        },
                    "Corralled" : {
                        "LevelCompletion" : SDB6[108],
                        "SecretsFound" : SDB6[160],
                        "ProtectedScorpion" : SDB6[161],
                        "Style" : SDB6[162],
                        },
                    "ScorpionsRampage" : {
                        "LevelCompletion" : SDB6[109],
                        "Style" : SDB6[159],
                        "NoPickupsUsed" : SDB6[164],
                        },
                    "CoupDEtat" : {
                        "LevelCompletion" : SDB6[110],
                        "Time" : SDB6[111],
                        "Perfect" : SDB6[112],
                        "Style" : SDB6[113],
                        },
                    "TheOffer" : {
                        "LevelCompletion" : SDB6[114],
                        "Time" : SDB6[115],
                        "Perfect" : SDB6[116],
                        "Style" : SDB6[117],
                        "RideGoblin" : SDB6[167],
                        },
                    "RaceAgainstTime" : {
                        "LevelCompletion" : SDB6[118],
                        "Time" : SDB6[119],
                        "Perfect" : SDB6[120],
                        },
                    "TheRazorsEdge" : {
                        "LevelCompletion" : SDB6[129],
                        "RBatsDestroyed" : SDB6[130],
                        "RemainingHealth" : SDB6[131],
                        "PickupsUsed" : SDB6[132],
                        "Style" : SDB6[133],
                        },
                    "BreakingAndEntering" : {
                        "LevelCompletion" : SDB6[134],
                        "Time" : SDB6[135],
                        "Perfect" : SDB6[136],
                        "SecretsFound" : SDB6[137],
                        "StealthBonus" : SDB6[138],
                        },
                    "ChemicalChaos" : {
                        "LevelCompletion" : SDB6[140],
                        "Time" : SDB6[141],
                        "Perfect" : SDB6[142],
                        },
                    "OscorpsUltimateWeapon" : {
                        "LevelCompletion" : SDB6[144],
                        "Time" : SDB6[145],
                        "Perfect" : SDB6[146],
                        "Style" : SDB6[147],
                        },
                    "EscapeFromOscorp" : {
                        "LevelCompletion" : SDB6[148],
                        "Perfect" : SDB6[149],
                        "SupersoldiersKilled" : SDB6[150],
                        "Style" : SDB6[151],
                        },
                    "MaryJaneKidnapped" : {
                        "LevelCompletion" : SDB6[152],
                        "Perfect" : SDB6[153],
                        },
                    "Other" : {
                        "UnknownBonus01" : SDB6[98],
                        "UnknownBonus02" : SDB6[103],
                        "UnknownBonus03" : SDB6[121],
                        "UnknownBonus04" : SDB6[122],
                        "UnknownBonus05" : SDB6[123],
                        "UnknownBonus06" : SDB6[124],
                        "UnknownBonus07" : SDB6[125],
                        "UnknownBonus08" : SDB6[126],
                        "UnknownBonus09" : SDB6[127],
                        "UnknownBonus10" : SDB6[128],
                        "UnknownBonus11" : SDB6[139],
                        "UnknownBonus12" : SDB6[143],
                        "UnknownBonus13" : SDB6[154],
                        "UnknownBonus14" : SDB6[155],
                        "UnknownBonus15" : SDB6[156],
                        "UnknownBonus16" : SDB6[157],
                        "UnknownBonus17" : SDB6[158],
                        "UnknownBonus18" : SDB6[163],
                        "UnknownBonus19" : SDB6[165],
                        "UnknownBonus20" : SDB6[166],
                        },
                    },
                "Options" : {
                    "UnknownVolume" : SDB6[7],
                    "MusicVolume" : SDB6[8],
                    "SFXVolume" : SDB6[9],
                    "VoiceVolume" : SDB6[10],
                    "MovieVolume" : SDB6[11],
                    "CameraMode" : SDB6[171],
                    "InvertCameraLook" : SDB6[177],
                    "ControllerVibration" : SDB6[178],
                    "SwapJumpAndWebInputs" : SDB6[174],
                    "SwapZipAndSwingInputs" : SDB6[175],
                    "ControllerMovementTweak" : SDB6[176],
                    "MovementToggles" : SDB6[169],
                    "TankControls" : SDB6[170],
                    "ShowStylePoints" : SDB6[172],
                    },
                "Miscellaneous" : {
                    "MainMenuState" : SDB6[1],
                    "UnknownString01" : SDB6[173],
                    "UnknownString02" : SDB6[179],
                    },
                },
            "Slot07" : { # Slot-tailored data.
                "Baseline" : {
                    "Difficulty" : SDB7[168],
                    "ContinueLevel" : SDB7[0],
                    "UnlocksLevelUNKNOWN" : SDB7[2],
                    "UnlocksLevelEASY" : SDB7[3],
                    "UnlocksLevelNORMAL" : SDB7[4],
                    "UnlocksLevelHERO" : SDB7[5],
                    "UnlocksLevelSUPERHERO" : SDB7[6],
                    "SecretStoreToggles" : SDB7[12],
                    },
                "CombatControls" : {
                    "FieldGoal_PPK" : SDB7[13],
                    "GravitySlam_PPJ" : SDB7[14],
                    "WebHit_PPW" : SDB7[15],
                    "BackflipKick_PKK" : SDB7[16],
                    "Sting_PKP" : SDB7[17],
                    "Palm_PKJ" : SDB7[18],
                    "HighWebHit_PKW" : SDB7[19],
                    "DiveBomb_PJJ" : SDB7[20],
                    "HeadHammer_PJP" : SDB7[21],
                    "DiveKick_PJK" : SDB7[22],
                    "Uppercut_KKP" : SDB7[23],
                    "FlipMule_KKJ" : SDB7[24],
                    "LowWebHit_KKW" : SDB7[25],
                    "ScissorKick_KPK" : SDB7[26],
                    "HighStomp_KPJ" : SDB7[27],
                    "Tackle_KJJ" : SDB7[28],
                    "Handspring_KJK" : SDB7[29],
                    "Haymaker_KJP" : SDB7[30],
                    "AdvWebDome_WCKK" : SDB7[31],
                    "AdvWebGloves_WCPP" : SDB7[32],
                    "AdvImpactWeb_WCW" : SDB7[33],
                    },
                "TrainingBestTimes" : {
                    "BasicAirCombat" : [SDB7[34], SDB7[35], SDB7[36]],
                    "BasicSwingTraining" : [SDB7[37], SDB7[38], SDB7[39]],
                    "AdvancedSwingTraining" : [SDB7[40], SDB7[41], SDB7[42]],
                    "ExpertSwingTraining" : [SDB7[43], SDB7[44], SDB7[45]],
                    "BasicZipTraining" : [SDB7[46], SDB7[47], SDB7[48]],
                    "AdvancedZipTraining" : [SDB7[49], SDB7[50], SDB7[51]],
                    "ExpertZipTraining" : [SDB7[52], SDB7[53], SDB7[54]],
                    "SwingRings" : [SDB7[55], SDB7[56], SDB7[57]],
                    "SwingPlatforms" : [SDB7[58], SDB7[59], SDB7[60]],
                    "ObstacleCourse" : [SDB7[61], SDB7[62], SDB7[63]],
                    },
                "LevelBonusPoints" : {
                    "SearchForJustice" : {
                        "LevelCompletion" : SDB7[64],
                        "Perfect" : SDB7[65],
                        "Combat" : SDB7[66],
                        "SecretsFound" : SDB7[67],
                        "Style" : SDB7[68],
                        },
                    "WarehouseHunt" : {
                        "LevelCompletion" : SDB7[69],
                        "StealthBonus" : SDB7[70],
                        "SecretsFound" : SDB7[71],
                        "Style" : SDB7[72],
                        },
                    "BirthOfAHero" : {
                        "LevelCompletion" : SDB7[73],
                        "Time" : SDB7[74],
                        "SecretsFound" : SDB7[75],
                        "Style" : SDB7[76],
                        },
                    "OscorpsGambit" : {
                        "LevelCompletion" : SDB7[77],
                        "Perfect" : SDB7[78],
                        "DefeatedHKs" : SDB7[79],
                        "Style" : SDB7[80],
                        },
                    "TheSubwayStation" : {
                        "LevelCompletion" : SDB7[81],
                        "Time" : SDB7[82],
                        "Perfect" : SDB7[83],
                        "Style" : SDB7[84],
                        },
                    "ChaseThroughTheSewer" : {
                        "LevelCompletion" : SDB7[85],
                        "Time" : SDB7[86],
                        "SecretsFound" : SDB7[87],
                        "Combat" : SDB7[88],
                        "Style" : SDB7[89],
                        },
                    "ShowdownWithShocker" : {
                        "LevelCompletion" : SDB7[90],
                        "Time" : SDB7[91],
                        "Perfect" : SDB7[92],
                        "SecretsFound" : SDB7[93],
                        "Style" : SDB7[94],
                        },
                    "VulturesLair" : {
                        "LevelCompletion" : SDB7[95],
                        "Time" : SDB7[96],
                        "Perfect" : SDB7[97],
                        },
                    "VultureEscapes" : {
                        "LevelCompletion" : SDB7[99],
                        "Time" : SDB7[100],
                        "Perfect" : SDB7[101],
                        "VultureProximity" : SDB7[102],
                        },
                    "AirDuelWithVulture" : {
                        "LevelCompletion" : SDB7[104],
                        "Time" : SDB7[105],
                        "Perfect" : SDB7[106],
                        "Style" : SDB7[107],
                        },
                    "Corralled" : {
                        "LevelCompletion" : SDB7[108],
                        "SecretsFound" : SDB7[160],
                        "ProtectedScorpion" : SDB7[161],
                        "Style" : SDB7[162],
                        },
                    "ScorpionsRampage" : {
                        "LevelCompletion" : SDB7[109],
                        "Style" : SDB7[159],
                        "NoPickupsUsed" : SDB7[164],
                        },
                    "CoupDEtat" : {
                        "LevelCompletion" : SDB7[110],
                        "Time" : SDB7[111],
                        "Perfect" : SDB7[112],
                        "Style" : SDB7[113],
                        },
                    "TheOffer" : {
                        "LevelCompletion" : SDB7[114],
                        "Time" : SDB7[115],
                        "Perfect" : SDB7[116],
                        "Style" : SDB7[117],
                        "RideGoblin" : SDB7[167],
                        },
                    "RaceAgainstTime" : {
                        "LevelCompletion" : SDB7[118],
                        "Time" : SDB7[119],
                        "Perfect" : SDB7[120],
                        },
                    "TheRazorsEdge" : {
                        "LevelCompletion" : SDB7[129],
                        "RBatsDestroyed" : SDB7[130],
                        "RemainingHealth" : SDB7[131],
                        "PickupsUsed" : SDB7[132],
                        "Style" : SDB7[133],
                        },
                    "BreakingAndEntering" : {
                        "LevelCompletion" : SDB7[134],
                        "Time" : SDB7[135],
                        "Perfect" : SDB7[136],
                        "SecretsFound" : SDB7[137],
                        "StealthBonus" : SDB7[138],
                        },
                    "ChemicalChaos" : {
                        "LevelCompletion" : SDB7[140],
                        "Time" : SDB7[141],
                        "Perfect" : SDB7[142],
                        },
                    "OscorpsUltimateWeapon" : {
                        "LevelCompletion" : SDB7[144],
                        "Time" : SDB7[145],
                        "Perfect" : SDB7[146],
                        "Style" : SDB7[147],
                        },
                    "EscapeFromOscorp" : {
                        "LevelCompletion" : SDB7[148],
                        "Perfect" : SDB7[149],
                        "SupersoldiersKilled" : SDB7[150],
                        "Style" : SDB7[151],
                        },
                    "MaryJaneKidnapped" : {
                        "LevelCompletion" : SDB7[152],
                        "Perfect" : SDB7[153],
                        },
                    "Other" : {
                        "UnknownBonus01" : SDB7[98],
                        "UnknownBonus02" : SDB7[103],
                        "UnknownBonus03" : SDB7[121],
                        "UnknownBonus04" : SDB7[122],
                        "UnknownBonus05" : SDB7[123],
                        "UnknownBonus06" : SDB7[124],
                        "UnknownBonus07" : SDB7[125],
                        "UnknownBonus08" : SDB7[126],
                        "UnknownBonus09" : SDB7[127],
                        "UnknownBonus10" : SDB7[128],
                        "UnknownBonus11" : SDB7[139],
                        "UnknownBonus12" : SDB7[143],
                        "UnknownBonus13" : SDB7[154],
                        "UnknownBonus14" : SDB7[155],
                        "UnknownBonus15" : SDB7[156],
                        "UnknownBonus16" : SDB7[157],
                        "UnknownBonus17" : SDB7[158],
                        "UnknownBonus18" : SDB7[163],
                        "UnknownBonus19" : SDB7[165],
                        "UnknownBonus20" : SDB7[166],
                        },
                    },
                "Options" : {
                    "UnknownVolume" : SDB7[7],
                    "MusicVolume" : SDB7[8],
                    "SFXVolume" : SDB7[9],
                    "VoiceVolume" : SDB7[10],
                    "MovieVolume" : SDB7[11],
                    "CameraMode" : SDB7[171],
                    "InvertCameraLook" : SDB7[177],
                    "ControllerVibration" : SDB7[178],
                    "SwapJumpAndWebInputs" : SDB7[174],
                    "SwapZipAndSwingInputs" : SDB7[175],
                    "ControllerMovementTweak" : SDB7[176],
                    "MovementToggles" : SDB7[169],
                    "TankControls" : SDB7[170],
                    "ShowStylePoints" : SDB7[172],
                    },
                "Miscellaneous" : {
                    "MainMenuState" : SDB7[1],
                    "UnknownString01" : SDB7[173],
                    "UnknownString02" : SDB7[179],
                    },
                },
            "Slot08" : { # Slot-tailored data.
                "Baseline" : {
                    "Difficulty" : SDB8[168],
                    "ContinueLevel" : SDB8[0],
                    "UnlocksLevelUNKNOWN" : SDB8[2],
                    "UnlocksLevelEASY" : SDB8[3],
                    "UnlocksLevelNORMAL" : SDB8[4],
                    "UnlocksLevelHERO" : SDB8[5],
                    "UnlocksLevelSUPERHERO" : SDB8[6],
                    "SecretStoreToggles" : SDB8[12],
                    },
                "CombatControls" : {
                    "FieldGoal_PPK" : SDB8[13],
                    "GravitySlam_PPJ" : SDB8[14],
                    "WebHit_PPW" : SDB8[15],
                    "BackflipKick_PKK" : SDB8[16],
                    "Sting_PKP" : SDB8[17],
                    "Palm_PKJ" : SDB8[18],
                    "HighWebHit_PKW" : SDB8[19],
                    "DiveBomb_PJJ" : SDB8[20],
                    "HeadHammer_PJP" : SDB8[21],
                    "DiveKick_PJK" : SDB8[22],
                    "Uppercut_KKP" : SDB8[23],
                    "FlipMule_KKJ" : SDB8[24],
                    "LowWebHit_KKW" : SDB8[25],
                    "ScissorKick_KPK" : SDB8[26],
                    "HighStomp_KPJ" : SDB8[27],
                    "Tackle_KJJ" : SDB8[28],
                    "Handspring_KJK" : SDB8[29],
                    "Haymaker_KJP" : SDB8[30],
                    "AdvWebDome_WCKK" : SDB8[31],
                    "AdvWebGloves_WCPP" : SDB8[32],
                    "AdvImpactWeb_WCW" : SDB8[33],
                    },
                "TrainingBestTimes" : {
                    "BasicAirCombat" : [SDB8[34], SDB8[35], SDB8[36]],
                    "BasicSwingTraining" : [SDB8[37], SDB8[38], SDB8[39]],
                    "AdvancedSwingTraining" : [SDB8[40], SDB8[41], SDB8[42]],
                    "ExpertSwingTraining" : [SDB8[43], SDB8[44], SDB8[45]],
                    "BasicZipTraining" : [SDB8[46], SDB8[47], SDB8[48]],
                    "AdvancedZipTraining" : [SDB8[49], SDB8[50], SDB8[51]],
                    "ExpertZipTraining" : [SDB8[52], SDB8[53], SDB8[54]],
                    "SwingRings" : [SDB8[55], SDB8[56], SDB8[57]],
                    "SwingPlatforms" : [SDB8[58], SDB8[59], SDB8[60]],
                    "ObstacleCourse" : [SDB8[61], SDB8[62], SDB8[63]],
                    },
                "LevelBonusPoints" : {
                    "SearchForJustice" : {
                        "LevelCompletion" : SDB8[64],
                        "Perfect" : SDB8[65],
                        "Combat" : SDB8[66],
                        "SecretsFound" : SDB8[67],
                        "Style" : SDB8[68],
                        },
                    "WarehouseHunt" : {
                        "LevelCompletion" : SDB8[69],
                        "StealthBonus" : SDB8[70],
                        "SecretsFound" : SDB8[71],
                        "Style" : SDB8[72],
                        },
                    "BirthOfAHero" : {
                        "LevelCompletion" : SDB8[73],
                        "Time" : SDB8[74],
                        "SecretsFound" : SDB8[75],
                        "Style" : SDB8[76],
                        },
                    "OscorpsGambit" : {
                        "LevelCompletion" : SDB8[77],
                        "Perfect" : SDB8[78],
                        "DefeatedHKs" : SDB8[79],
                        "Style" : SDB8[80],
                        },
                    "TheSubwayStation" : {
                        "LevelCompletion" : SDB8[81],
                        "Time" : SDB8[82],
                        "Perfect" : SDB8[83],
                        "Style" : SDB8[84],
                        },
                    "ChaseThroughTheSewer" : {
                        "LevelCompletion" : SDB8[85],
                        "Time" : SDB8[86],
                        "SecretsFound" : SDB8[87],
                        "Combat" : SDB8[88],
                        "Style" : SDB8[89],
                        },
                    "ShowdownWithShocker" : {
                        "LevelCompletion" : SDB8[90],
                        "Time" : SDB8[91],
                        "Perfect" : SDB8[92],
                        "SecretsFound" : SDB8[93],
                        "Style" : SDB8[94],
                        },
                    "VulturesLair" : {
                        "LevelCompletion" : SDB8[95],
                        "Time" : SDB8[96],
                        "Perfect" : SDB8[97],
                        },
                    "VultureEscapes" : {
                        "LevelCompletion" : SDB8[99],
                        "Time" : SDB8[100],
                        "Perfect" : SDB8[101],
                        "VultureProximity" : SDB8[102],
                        },
                    "AirDuelWithVulture" : {
                        "LevelCompletion" : SDB8[104],
                        "Time" : SDB8[105],
                        "Perfect" : SDB8[106],
                        "Style" : SDB8[107],
                        },
                    "Corralled" : {
                        "LevelCompletion" : SDB8[108],
                        "SecretsFound" : SDB8[160],
                        "ProtectedScorpion" : SDB8[161],
                        "Style" : SDB8[162],
                        },
                    "ScorpionsRampage" : {
                        "LevelCompletion" : SDB8[109],
                        "Style" : SDB8[159],
                        "NoPickupsUsed" : SDB8[164],
                        },
                    "CoupDEtat" : {
                        "LevelCompletion" : SDB8[110],
                        "Time" : SDB8[111],
                        "Perfect" : SDB8[112],
                        "Style" : SDB8[113],
                        },
                    "TheOffer" : {
                        "LevelCompletion" : SDB8[114],
                        "Time" : SDB8[115],
                        "Perfect" : SDB8[116],
                        "Style" : SDB8[117],
                        "RideGoblin" : SDB8[167],
                        },
                    "RaceAgainstTime" : {
                        "LevelCompletion" : SDB8[118],
                        "Time" : SDB8[119],
                        "Perfect" : SDB8[120],
                        },
                    "TheRazorsEdge" : {
                        "LevelCompletion" : SDB8[129],
                        "RBatsDestroyed" : SDB8[130],
                        "RemainingHealth" : SDB8[131],
                        "PickupsUsed" : SDB8[132],
                        "Style" : SDB8[133],
                        },
                    "BreakingAndEntering" : {
                        "LevelCompletion" : SDB8[134],
                        "Time" : SDB8[135],
                        "Perfect" : SDB8[136],
                        "SecretsFound" : SDB8[137],
                        "StealthBonus" : SDB8[138],
                        },
                    "ChemicalChaos" : {
                        "LevelCompletion" : SDB8[140],
                        "Time" : SDB8[141],
                        "Perfect" : SDB8[142],
                        },
                    "OscorpsUltimateWeapon" : {
                        "LevelCompletion" : SDB8[144],
                        "Time" : SDB8[145],
                        "Perfect" : SDB8[146],
                        "Style" : SDB8[147],
                        },
                    "EscapeFromOscorp" : {
                        "LevelCompletion" : SDB8[148],
                        "Perfect" : SDB8[149],
                        "SupersoldiersKilled" : SDB8[150],
                        "Style" : SDB8[151],
                        },
                    "MaryJaneKidnapped" : {
                        "LevelCompletion" : SDB8[152],
                        "Perfect" : SDB8[153],
                        },
                    "Other" : {
                        "UnknownBonus01" : SDB8[98],
                        "UnknownBonus02" : SDB8[103],
                        "UnknownBonus03" : SDB8[121],
                        "UnknownBonus04" : SDB8[122],
                        "UnknownBonus05" : SDB8[123],
                        "UnknownBonus06" : SDB8[124],
                        "UnknownBonus07" : SDB8[125],
                        "UnknownBonus08" : SDB8[126],
                        "UnknownBonus09" : SDB8[127],
                        "UnknownBonus10" : SDB8[128],
                        "UnknownBonus11" : SDB8[139],
                        "UnknownBonus12" : SDB8[143],
                        "UnknownBonus13" : SDB8[154],
                        "UnknownBonus14" : SDB8[155],
                        "UnknownBonus15" : SDB8[156],
                        "UnknownBonus16" : SDB8[157],
                        "UnknownBonus17" : SDB8[158],
                        "UnknownBonus18" : SDB8[163],
                        "UnknownBonus19" : SDB8[165],
                        "UnknownBonus20" : SDB8[166],
                        },
                    },
                "Options" : {
                    "UnknownVolume" : SDB8[7],
                    "MusicVolume" : SDB8[8],
                    "SFXVolume" : SDB8[9],
                    "VoiceVolume" : SDB8[10],
                    "MovieVolume" : SDB8[11],
                    "CameraMode" : SDB8[171],
                    "InvertCameraLook" : SDB8[177],
                    "ControllerVibration" : SDB8[178],
                    "SwapJumpAndWebInputs" : SDB8[174],
                    "SwapZipAndSwingInputs" : SDB8[175],
                    "ControllerMovementTweak" : SDB8[176],
                    "MovementToggles" : SDB8[169],
                    "TankControls" : SDB8[170],
                    "ShowStylePoints" : SDB8[172],
                    },
                "Miscellaneous" : {
                    "MainMenuState" : SDB8[1],
                    "UnknownString01" : SDB8[173],
                    "UnknownString02" : SDB8[179],
                    },
                },
            }
        # STEP 4: Return the dictionary save game to the caller.
        return SaveDataBetter # Not SaveDataBinary/SDB.
    except:
        return None
    pass
#

# ===================================================================================================
# NOTHING: Beyond this point.
