# SAV/JSON Format
This document describes the context, operation and format of the SAV file, and also provides information on the JSON text representation of the data within.

All information relevant to this document and the SAVBasics code/project as a whole was determined through file hex editing and trial-and-error results observation.

- NOTE: "(d/h)" = decimal/hexadecimal = 10/0A.

## Context
The game supports eight unique save states/"slots" and writes save data in bulk to "/SavedGames0/spidermn.sav" (relative to the directory the executable is in). This file is 4792 bytes in size and consists of packed binary data. By default upon installation, this file does not yet exist.

## Operation
The save data contains a version-specific signature. If the signature the game version is expecting is different to the one found in the save data, the save data is classified as invalid and the game will act as if no save file exists at all.

There is little value validation outside of the header and footer - a select few variables per save slot have to be within correct ranges (otherwise the slot is considered empty by the game), however all else can be whatever - for example it is possible to have -1 as a level bonus score.

Nowhere is it stored explicitly which slots are empty and which are in use - instead slots which are believed to be empty have their validated values (mentioned prior) set to deliberately incorrect states when the game saves the whole file. This effectively enforces the illusion of "empty" slots up until the user directly saves to them, at which point the correct states will be saved instead.

A good amount of the available space appears to be used for nothing or as padding. Ignoring this, the structure is very efficient; data is not duplicated and inference is often used instead of explicitly having a value for everything (for instance, the total Secret Points count is derived from the summary of all individual level bonuses, which are stored).

## Format


### Overview
The save data is split into ten differently-sized chunks that follow one another. All values are little-endian (on Windows at least); integer signage can be ambiguous, and is not defined here (for the sake of functionality most integer values are considered signed on import/export by SAVBasics).
- Chunk 0 is a header that stores the version signature.
- Chunks 1-8 hold the slot data for slots 1-8 respectively (the struture of each is identical).
- Chunk 9 is a footer that stores information about the last save made to the file by the game.

This section will go on to provide variables/values with offsets for each chunk type, however the offsets given will be *relative*. To get the absolute offset, the offset of the chunk itself (relative to the size of the file as a whole) must be added - see the table below for chunk offsets and lengths.

| Chunk | Offset (d/h) | Size (bytes) |
| ----- | ------------ | ------------ |
| 0: Header | 0/0 | 16 |
| 1: Slot 1 | 16/10 | 592 |
| 2: Slot 2 | 608/260 | 592 |
| 3: Slot 3 | 1200/4B0 | 592 |
| 4: Slot 4 | 1792/700 | 592 |
| 5: Slot 5 | 2384/950 | 592 |
| 6: Slot 6 | 2976/BA0 | 592 |
| 7: Slot 7 | 3568/DF0 | 592 |
| 8: Slot 8 | 4160/1040 | 592 |
| 9: Footer | 4752/1290 | 40 |

Additionally, for each variable/value, a Type and JSON Variable will be listed.
- Type could be: "N/A" (padding/unused, seemingly), "N16" (16-bit integer/number), "N32" (32-bit integer/number), "BOO" (boolean flag, false/true, 0/1), "STR" (ASCII-encoded text).
- JSON Variables link a given piece of binary data to a variable in the JSON structure. A period separates sub-structures, and "Slot0#" refers to any slot (1-8). Brackets point to a specific item in an array by way of one-based index.

### Chunk 0: Header
- NOTE: If the signature contained in this chunk doesn't match the one the game version is expecting at runtime, the whole save file is considered empty.

| Offset (d/h) | Type | JSON Variable | Information |
| ------------ | ---- | ------------- | ----------- |
| 0/0 | STR | General.Signature | Version-specific signature, eight characters long. |
| 8/8 | N/A | N/A | Eight bytes long. |

### Chunks 1-8: Slots 1-8
- NOTE: Level ID and main menu state values are validated - if incorrect, that slot will be considered empty.

| Offset (d/h) | Type | JSON Variable | Information |
| ------------ | ---- | ------------- | ----------- |
| 0/0          | N/A | N/A | Sixteen bytes long. |
| 16/10 | N32 | Slot0#.Baseline.ContinueLevel | Level ID of the current/main menu "CONTINUE" level. |
| 20/14 | N32 | Slot0#.Miscellaneous.MainMenuState | Main menu setting: -1 disables "CONTINUE"/highlights "EXIT", 0 is invalid, and 1 is the default/standard behaviour. |
| 24/18 | N32 | Slot0#.Baseline.UnlocksLevelUNKNOWN | Unlock level for 0/UNKNOWN difficulty level. |
| 28/1C | N32 | Slot0#.Baseline.UnlocksLevelEASY | Unlock level for 1/EASY difficulty level. |
| 32/20 | N32 | Slot0#.Baseline.UnlocksLevelNORMAL | Unlock level for 2/NORMAL difficulty level. |
| 36/24 | N32 | Slot0#.Baseline.UnlocksLevelHERO | Unlock level for 3/HERO difficulty level. |
| 40/28 | N32 | Slot0#.Baseline.UnlocksLevelSUPERHERO | Unlock level for 4/SUPER HERO difficulty level. |
| 44/2C | N/A | N/A | Forty bytes long. |
| 84/54 | N32 | Slot0#.Options.UnknownVolume | Unknown volume level. |
| 88/58 | N32 | Slot0#.Options.MusicVolume | Volume level for MUSIC. |
| 92/5C | N32 | Slot0#.Options.SFXVolume | Volume level for SFX. |
| 96/60 | N32 | Slot0#.Options.VoiceVolume | Volume level for VOICE. |
| 100/64 | N32 | Slot0#.Options.MovieVolume | Volume level for MOVIE. |
| 104/68 | N/A | N/A | Ten bytes long. |
| 114/72 | N16 | Slot0#.Baseline.SecretStoreToggles | Secret Store enabled items flags, or similar. |
| 116/74 | N/A | N/A | Twenty-five bytes long. |
| 141/8D | BOO | Slot0#.CombatControls.FieldGoal_PPK | Combo unlock status for FIELD GOAL (P, P, K). |
| 142/8E | BOO | Slot0#.CombatControls.GravitySlam_PPJ | Combo unlock status for GRAVITY SLAM (P, P, J). |
| 143/8F | BOO | Slot0#.CombatControls.WebHit_PPW | Combo unlock status for WEB HIT (P, P, W). |
| 144/90 | BOO | Slot0#.CombatControls.BackflipKick_PKK | Combo unlock status for BACKFLIP KICK (P, K, K). |
| 145/91 | BOO | Slot0#.CombatControls.Sting_PKP | Combo unlock status for STING (P, K, P). |
| 146/92 | BOO | Slot0#.CombatControls.Palm_PKJ | Combo unlock status for PALM (P, K, J). |
| 147/93 | BOO | Slot0#.CombatControls.HighWebHit_PKW | Combo unlock status for HIGH WEB HIT (P, K, W). |
| 148/94 | BOO | Slot0#.CombatControls.DiveBomb_PJJ | Combo unlock status for DIVE-BOMB (P, J, J). |
| 149/95 | BOO | Slot0#.CombatControls.HeadHammer_PJP | Combo unlock status for HEAD HAMMER (P, J, P). |
| 150/96 | BOO | Slot0#.CombatControls.DiveKick_PJK | Combo unlock status for DIVE KICK (P, J, K). |
| 151/97 | N/A | N/A | Two bytes long. |
| 153/99 | BOO | Slot0#.CombatControls.Uppercut_KKP | Combo unlock status for UPPERCUT (K, K, P). |
| 154/9A | BOO | Slot0#.CombatControls.FlipMule_KKJ | Combo unlock status for FLIP MULE (K, K, J). |
| 155/9B | BOO | Slot0#.CombatControls.LowWebHit_KKW | Combo unlock status for LOW WEB HIT (K, K, W). |
| 156/9C | N/A | N/A | One byte long. |
| 157/9D | BOO | Slot0#.CombatControls.ScissorKick_KPK | Combo unlock status for SCISSOR KICK (K, P, K). |
| 158/9E | BOO | Slot0#.CombatControls.HighStomp_KPJ | Combo unlock status for HIGH STOMP (K, P, J). |
| 159/9F | N/A | N/A | One byte long. |
| 160/A0 | BOO | Slot0#.CombatControls.Tackle_KJJ | Combo unlock status for TACKLE (K, J, J). |
| 161/A1 | BOO | Slot0#.CombatControls.Handspring_KJK | Combo unlock status for HANDSPRING (K, J, K). |
| 162/A2 | BOO | Slot0#.CombatControls.Haymaker_KJP | Combo unlock status for HAYMAKER (K, J, P). |
| 163/A3 | N/A | N/A | Three bytes long. |
| 166/A6 | BOO | Slot0#.CombatControls.AdvWebDome_WCKK | Combo unlock status for ADV WEB DOME (WC+K, K). |
| 167/A7 | N/A | N/A | One byte long. |
| 168/A8 | BOO | Slot0#.CombatControls.AdvWebGloves_WCPP | Combo unlock status for ADV WEB GLOVES (WC+P, P). |
| 169/A9 | N/A | N/A | One byte long. |
| 170/AA | BOO | Slot0#.CombatControls.AdvImpactWeb_WCW | Combo unlock status for ADV IMPACT WEB (WC+W). |
| 171/AB | N/A | N/A | Thirteen bytes long. |
| 184/B8 | N32 | Slot0#.TrainingBestTimes.BasicAirCombat(1) | Best time #1 for BASIC AIR COMBAT in TRAINING. |
| 188/BC | N32 | Slot0#.TrainingBestTimes.BasicAirCombat(2) | Best time #2 for BASIC AIR COMBAT in TRAINING. |
| 192/C0 | N32 | Slot0#.TrainingBestTimes.BasicAirCombat(3) | Best time #3 for BASIC AIR COMBAT in TRAINING. |
| 196/C4 | N32 | Slot0#.TrainingBestTimes.BasicSwingTraining(1) | Best time #1 for BASIC SWING TRAINING in TRAINING. |
| 200/C8 | N32 | Slot0#.TrainingBestTimes.BasicSwingTraining(2) | Best time #2 for BASIC SWING TRAINING in TRAINING. |
| 204/CC | N32 | Slot0#.TrainingBestTimes.BasicSwingTraining(3) | Best time #3 for BASIC SWING TRAINING in TRAINING. |
| 208/D0 | N32 | Slot0#.TrainingBestTimes.AdvancedSwingTraining(1) | Best time #1 for ADVANCED SWING TRAINING in TRAINING. |
| 212/D4 | N32 | Slot0#.TrainingBestTimes.AdvancedSwingTraining(2) | Best time #2 for ADVANCED SWING TRAINING in TRAINING. |
| 216/D8 | N32 | Slot0#.TrainingBestTimes.AdvancedSwingTraining(3) | Best time #3 for ADVANCED SWING TRAINING in TRAINING. |
| 220/DC | N32 | Slot0#.TrainingBestTimes.ExpertSwingTraining(1) | Best time #1 for EXPERT SWING TRAINING in TRAINING. |
| 224/E0 | N32 | Slot0#.TrainingBestTimes.ExpertSwingTraining(2) | Best time #2 for EXPERT SWING TRAINING in TRAINING. |
| 228/E4 | N32 | Slot0#.TrainingBestTimes.ExpertSwingTraining(3) | Best time #3 for EXPERT SWING TRAINING in TRAINING. |
| 232/E8 | N32 | Slot0#.TrainingBestTimes.BasicZipTraining(1) | Best time #1 for BASIC ZIP TRAINING in TRAINING. |
| 236/EC | N32 | Slot0#.TrainingBestTimes.BasicZipTraining(2) | Best time #2 for BASIC ZIP TRAINING in TRAINING. |
| 240/F0 | N32 | Slot0#.TrainingBestTimes.BasicZipTraining(3) | Best time #3 for BASIC ZIP TRAINING in TRAINING. |
| 244/F4 | N32 | Slot0#.TrainingBestTimes.AdvancedZipTraining(1) | Best time #1 for ADVANCED ZIP TRAINING in TRAINING. |
| 248/F8 | N32 | Slot0#.TrainingBestTimes.AdvancedZipTraining(2) | Best time #2 for ADVANCED ZIP TRAINING in TRAINING. |
| 252/FC | N32 | Slot0#.TrainingBestTimes.AdvancedZipTraining(3) | Best time #3 for ADVANCED ZIP TRAINING in TRAINING. |
| 256/100 | N32 | Slot0#.TrainingBestTimes.ExpertZipTraining(1) | Best time #1 for EXPERT ZIP TRAINING in TRAINING. |
| 260/104 | N32 | Slot0#.TrainingBestTimes.ExpertZipTraining(2) | Best time #2 for EXPERT ZIP TRAINING in TRAINING. |
| 264/108 | N32 | Slot0#.TrainingBestTimes.ExpertZipTraining(3) | Best time #3 for EXPERT ZIP TRAINING in TRAINING. |
| 268/10C | N32 | Slot0#.TrainingBestTimes.SwingRings(1) | Best time #1 for SWING RINGS in TRAINING. |
| 272/110 | N32 | Slot0#.TrainingBestTimes.SwingRings(2) | Best time #2 for SWING RINGS in TRAINING. |
| 276/114 | N32 | Slot0#.TrainingBestTimes.SwingRings(3) | Best time #3 for SWING RINGS in TRAINING. |
| 280/118 | N32 | Slot0#.TrainingBestTimes.SwingPlatforms(1) | Best time #1 for SWING PLATFORMS in TRAINING. |
| 284/11C | N32 | Slot0#.TrainingBestTimes.SwingPlatforms(2) | Best time #2 for SWING PLATFORMS in TRAINING. |
| 288/120 | N32 | Slot0#.TrainingBestTimes.SwingPlatforms(3) | Best time #3 for SWING PLATFORMS in TRAINING. |
| 292/124 | N32 | Slot0#.TrainingBestTimes.ObstacleCourse(1) | Best time #1 for OBSTACLE COURSE in TRAINING. |
| 296/128 | N32 | Slot0#.TrainingBestTimes.ObstacleCourse(2) | Best time #2 for OBSTACLE COURSE in TRAINING. |
| 300/12C | N32 | Slot0#.TrainingBestTimes.ObstacleCourse(3) | Best time #3 for OBSTACLE COURSE in TRAINING. |
| 304/130 | N/A | N/A | Two bytes long. |
| 306/132 | N16 | Slot0#.LevelBonusPoints.SearchForJustice.LevelCompletion | Bonus points for "SEARCH FOR JUSTICE" / "Level Completion". |
| 308/134 | N16 | Slot0#.LevelBonusPoints.SearchForJustice.Perfect | Bonus points for "SEARCH FOR JUSTICE" / "Perfect". |
| 310/136 | N16 | Slot0#.LevelBonusPoints.SearchForJustice.Combat | Bonus points for "SEARCH FOR JUSTICE" / "Combat". |
| 312/138 | N16 | Slot0#.LevelBonusPoints.SearchForJustice.SecretsFound | Bonus points for "SEARCH FOR JUSTICE" / "Secret(s) Found". |
| 314/13A | N16 | Slot0#.LevelBonusPoints.SearchForJustice.Style | Bonus points for "SEARCH FOR JUSTICE" / "Style". |
| 316/13C | N16 | Slot0#.LevelBonusPoints.WarehouseHunt.LevelCompletion | Bonus points for "WAREHOUSE HUNT" / "Level Completion". |
| 318/13E | N16 | Slot0#.LevelBonusPoints.WarehouseHunt.StealthBonus | Bonus points for "WAREHOUSE HUNT" / "Stealth Bonus". |
| 320/140 | N16 | Slot0#.LevelBonusPoints.WarehouseHunt.SecretsFound | Bonus points for "WAREHOUSE HUNT" / "Secret(s) Found". |
| 322/142 | N16 | Slot0#.LevelBonusPoints.WarehouseHunt.Style | Bonus points for "WAREHOUSE HUNT" / "Style". |
| 324/144 | N16 | Slot0#.LevelBonusPoints.BirthOfAHero.LevelCompletion | Bonus points for "BIRTH OF A HERO" / "Level Completion". |
| 326/146 | N16 | Slot0#.LevelBonusPoints.BirthOfAHero.Time | Bonus points for "BIRTH OF A HERO" / "Time". | 
| 328/148 | N16 | Slot0#.LevelBonusPoints.BirthOfAHero.SecretsFound | Bonus points for "BIRTH OF A HERO" / "Secret(s) Found". |
| 330/14A | N16 | Slot0#.LevelBonusPoints.BirthOfAHero.Style | Bonus points for "BIRTH OF A HERO" / "Style". |
| 332/14C | N16 | Slot0#.LevelBonusPoints.OscorpsGambit.LevelCompletion | Bonus points for "OSCORP'S GAMBIT" / "Level Completion". |
| 334/14E | N16 | Slot0#.LevelBonusPoints.OscorpsGambit.Perfect | Bonus points for "OSCORP'S GAMBIT" / "Perfect". |
| 336/150 | N16 | Slot0#.LevelBonusPoints.OscorpsGambit.DefeatedHKs | Bonus points for "OSCORP'S GAMBIT" / "Defeated HKs". |
| 338/152 | N16 | Slot0#.LevelBonusPoints.OscorpsGambit.Style | Bonus points for "OSCORP'S GAMBIT" / "Style". |
| 340/154 | N16 | Slot0#.LevelBonusPoints.TheSubwayStation.LevelCompletion | Bonus points for "THE SUBWAY STATION" / "Level Completion". |
| 342/156 | N16 | Slot0#.LevelBonusPoints.TheSubwayStation.Time | Bonus points for "THE SUBWAY STATION" / "Time". |
| 344/158 | N16 | Slot0#.LevelBonusPoints.TheSubwayStation.Perfect | Bonus points for "THE SUBWAY STATION" / "Perfect". |
| 346/15A | N16 | Slot0#.LevelBonusPoints.TheSubwayStation.Style | Bonus points for "THE SUBWAY STATION" / "Style". |
| 348/15C | N16 | Slot0#.LevelBonusPoints.ChaseThroughTheSewer.LevelCompletion | Bonus points for "CHASE THROUGH THE SEWER" / "Level Completion". |
| 350/15E | N16 | Slot0#.LevelBonusPoints.ChaseThroughTheSewer.Time | Bonus points for "CHASE THROUGH THE SEWER" / "Time". |
| 352/160 | N16 | Slot0#.LevelBonusPoints.ChaseThroughTheSewer.SecretsFound | Bonus points for "CHASE THROUGH THE SEWER" / "Secret(s) Found". |
| 354/162 | N16 | Slot0#.LevelBonusPoints.ChaseThroughTheSewer.Combat | Bonus points for "CHASE THROUGH THE SEWER" / "Combat". |
| 356/164 | N16 | Slot0#.LevelBonusPoints.ChaseThroughTheSewer.Style | Bonus points for "CHASE THROUGH THE SEWER" / "Style". |
| 358/166 | N16 | Slot0#.LevelBonusPoints.ShowdownWithShocker.LevelCompletion | Bonus points for "SHOWDOWN WITH SHOCKER" / "Level Completion". |
| 360/168 | N16 | Slot0#.LevelBonusPoints.ShowdownWithShocker.Time | Bonus points for "SHOWDOWN WITH SHOCKER" / "Time". |
| 362/16A | N16 | Slot0#.LevelBonusPoints.ShowdownWithShocker.Perfect | Bonus points for "SHOWDOWN WITH SHOCKER" / "Perfect". |
| 364/16C | N16 | Slot0#.LevelBonusPoints.ShowdownWithShocker.SecretsFound | Bonus points for "SHOWDOWN WITH SHOCKER" / "Secret(s) Found". |
| 366/16E | N16 | Slot0#.LevelBonusPoints.ShowdownWithShocker.Style | Bonus points for "SHOWDOWN WITH SHOCKER" / "Style". |
| 368/170 | N16 | Slot0#.LevelBonusPoints.VulturesLair.LevelCompletion | Bonus points for "VULTURE'S LAIR" / "Level Completion". |
| 370/172 | N16 | Slot0#.LevelBonusPoints.VulturesLair.Time | Bonus points for "VULTURE'S LAIR" / "Time". |
| 372/174 | N16 | Slot0#.LevelBonusPoints.VulturesLair.Perfect | Bonus points for "VULTURE'S LAIR" / "Perfect". |
| 374/176 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus01 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 376/178 | N16 | Slot0#.LevelBonusPoints.VultureEscapes.LevelCompletion | Bonus points for "VULTURE ESCAPES" / "Level Completion" . |
| 378/17A | N16 | Slot0#.LevelBonusPoints.VultureEscapes.Time | Bonus points for "VULTURE ESCAPES" / "Time". |
| 380/17C | N16 | Slot0#.LevelBonusPoints.VultureEscapes.Perfect | Bonus points for "VULTURE ESCAPES" / "Perfect". |
| 382/17E | N16 | Slot0#.LevelBonusPoints.VultureEscapes.VultureProximity | Bonus points for "VULTURE ESCAPES" / "Vulture Proximity". |
| 384/180 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus02 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 386/182 | N16 | Slot0#.LevelBonusPoints.AirDuelWithVulture.LevelCompletion | Bonus points for "AIR DUEL WITH VULTURE" / "Level Completion". |
| 388/184 | N16 | Slot0#.LevelBonusPoints.AirDuelWithVulture.Time | Bonus points for "AIR DUEL WITH VULTURE" / "Time". |
| 390/186 | N16 | Slot0#.LevelBonusPoints.AirDuelWithVulture.Perfect | Bonus points for "AIR DUEL WITH VULTURE" / "Perfect". |
| 392/188 | N16 | Slot0#.LevelBonusPoints.AirDuelWithVulture.Style | Bonus points for "AIR DUEL WITH VULTURE" / "Style". |
| 394/18A | N16 | Slot0#.LevelBonusPoints.Corralled.LevelCompletion | Bonus points for "CORRALLED" / "Level Completion". |
| 396/18C | N16 | Slot0#.LevelBonusPoints.ScorpionsRampage.LevelCompletion | Bonus points for "SCORPION'S RAMPAGE" / "Level Completion". |
| 398/18E | N16 | Slot0#.LevelBonusPoints.CoupDEtat.LevelCompletion | Bonus points for "COUP D'ETAT" / "Level Completion". |
| 400/190 | N16 | Slot0#.LevelBonusPoints.CoupDEtat.Time | Bonus points for "COUP D'ETAT" / "Time". |
| 402/192 | N16 | Slot0#.LevelBonusPoints.CoupDEtat.Perfect | Bonus points for "COUP D'ETAT" / "Perfect". |
| 404/194 | N16 | Slot0#.LevelBonusPoints.CoupDEtat.Style | Bonus points for "COUP D'ETAT" / "Style". |
| 406/196 | N16 | Slot0#.LevelBonusPoints.TheOffer.LevelCompletion | Bonus points for "THE OFFER" / "Level Completion". |
| 408/198 | N16 | Slot0#.LevelBonusPoints.TheOffer.Time | Bonus points for "THE OFFER" / "Time". |
| 410/19A | N16 | Slot0#.LevelBonusPoints.TheOffer.Perfect | Bonus points for "THE OFFER" / "Perfect". |
| 412/19C | N16 | Slot0#.LevelBonusPoints.TheOffer.Style | Bonus points for "THE OFFER" / "Style". |
| 414/19E | N16 | Slot0#.LevelBonusPoints.RaceAgainstTime.LevelCompletion | Bonus points for "RACE AGAINST TIME" / "Level Completion". |
| 416/1A0 | N16 | Slot0#.LevelBonusPoints.RaceAgainstTime.Time | Bonus points for "RACE AGAINST TIME" / "Time". |
| 418/1A2 | N16 | Slot0#.LevelBonusPoints.RaceAgainstTime.Perfect | Bonus points for "RACE AGAINST TIME" / "Perfect". |
| 420/1A4 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus03 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 422/1A6 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus04 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 424/1A8 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus05 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 426/1AA | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus06 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 428/1AC | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus07 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 430/1AE | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus08 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 432/1B0 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus09 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 434/1B2 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus10 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 436/1B4 | N16 | Slot0#.LevelBonusPoints.TheRazorsEdge.LevelCompletion | Bonus points for "THE RAZOR'S EDGE" / "Level Completion". |
| 438/1B6 | N16 | Slot0#.LevelBonusPoints.TheRazorsEdge.RBatsDestroyed | Bonus points for "THE RAZOR'S EDGE" / "R-bats destroyed". |
| 440/1B8 | N16 | Slot0#.LevelBonusPoints.TheRazorsEdge.RemainingHealth | Bonus points for "THE RAZOR'S EDGE" / "Remaining health". |
| 442/1BA | N16 | Slot0#.LevelBonusPoints.TheRazorsEdge.PickupsUsed | Bonus points for "THE RAZOR'S EDGE" / "Pickups used". |
| 444/1BC | N16 | Slot0#.LevelBonusPoints.TheRazorsEdge.Style | Bonus points for "THE RAZOR'S EDGE" / "Style". |
| 446/1BE | N16 | Slot0#.LevelBonusPoints.BreakingAndEntering.LevelCompletion | Bonus points for "BREAKING AND ENTERING" / "Level Completion". |
| 448/1C0 | N16 | Slot0#.LevelBonusPoints.BreakingAndEntering.Time | Bonus points for "BREAKING AND ENTERING" / "Time". |
| 450/1C2 | N16 | Slot0#.LevelBonusPoints.BreakingAndEntering.Perfect | Bonus points for "BREAKING AND ENTERING" / "Perfect". |
| 452/1C4 | N16 | Slot0#.LevelBonusPoints.BreakingAndEntering.SecretsFound | Bonus points for "BREAKING AND ENTERING" / "Secret(s) Found". |
| 454/1C6 | N16 | Slot0#.LevelBonusPoints.BreakingAndEntering.StealthBonus | Bonus points for "BREAKING AND ENTERING" / "Stealth Bonus". |
| 456/1C8 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus11 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 458/1CA | N16 | Slot0#.LevelBonusPoints.ChemicalChaos.LevelCompletion | Bonus points for "CHEMICAL CHAOS" / "Level Completion". |
| 460/1CC | N16 | Slot0#.LevelBonusPoints.ChemicalChaos.Time | Bonus points for "CHEMICAL CHAOS" / "Time". |
| 462/1CE | N16 | Slot0#.LevelBonusPoints.ChemicalChaos.Perfect | Bonus points for "CHEMICAL CHAOS" / "Perfect". |
| 464/1D0 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus12 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 466/1D2 | N16 | Slot0#.LevelBonusPoints.OscorpsUltimateWeapon.LevelCompletion | Bonus points for "OSCORP'S ULTIMATE WEAPON" / "Level Completion". |
| 468/1D4 | N16 | Slot0#.LevelBonusPoints.OscorpsUltimateWeapon.Time | Bonus points for "OSCORP'S ULTIMATE WEAPON" / "Time". |
| 470/1D6 | N16 | Slot0#.LevelBonusPoints.OscorpsUltimateWeapon.Perfect | Bonus points for "OSCORP'S ULTIMATE WEAPON" / "Perfect". |
| 472/1D8 | N16 | Slot0#.LevelBonusPoints.OscorpsUltimateWeapon.Style | Bonus points for "OSCORP'S ULTIMATE WEAPON" / "Style". |
| 474/1DA | N16 | Slot0#.LevelBonusPoints.EscapeFromOscorp.LevelCompletion | Bonus points for "ESCAPE FROM OSCORP" / "Level Completion". |
| 476/1DC | N16 | Slot0#.LevelBonusPoints.EscapeFromOscorp.Perfect | Bonus points for "ESCAPE FROM OSCORP" / "Perfect". |
| 478/1DE | N16 | Slot0#.LevelBonusPoints.EscapeFromOscorp.SupersoldiersKilled | Bonus points for "ESCAPE FROM OSCORP" / "Supersoldiers Killed". |
| 480/1E0 | N16 | Slot0#.LevelBonusPoints.EscapeFromOscorp.Style | Bonus points for "ESCAPE FROM OSCORP" / "Style". |
| 482/1E2 | N16 | Slot0#.LevelBonusPoints.MaryJaneKidnapped.LevelCompletion | Bonus points for "MARY JANE KIDNAPPED" / "Level Completion". |
| 484/1E4 | N16 | Slot0#.LevelBonusPoints.MaryJaneKidnapped.Perfect | Bonus points for "MARY JANE KIDNAPPED" / "Perfect". |
| 486/1E6 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus13 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 488/1E8 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus14 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 490/1EA | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus15 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 492/1EC | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus16 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 494/1EE | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus17 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 496/1F0 | N16 | Slot0#.LevelBonusPoints.ScorpionsRampage.Style | Bonus points for "SCORPION'S RAMPAGE" / "Style". |
| 498/1F2 | N16 | Slot0#.LevelBonusPoints.Corralled.SecretsFound | Bonus points for "CORRALLED" / "Secret(s) Found". |
| 500/1F4 | N16 | Slot0#.LevelBonusPoints.Corralled.ProtectedScorpion | Bonus points for "CORRALLED" / "Protected Scorpion". |
| 502/1F6 | N16 | Slot0#.LevelBonusPoints.Corralled.Style | Bonus points for "CORRALLED" / "Style". |
| 504/1F8 | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus18 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 506/1FA | N16 | Slot0#.LevelBonusPoints.ScorpionsRampage.NoPickupsUsed | Bonus points for "SCORPION'S RAMPAGE" / "No Pickups Used". |
| 508/1FC | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus19 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 510/1FE | N16 | Slot0#.LevelBonusPoints.Other.UnknownBonus20 | Bonus points for an unknown level/bonus, does add to total Secret Points count. |
| 512/200 | N16 | Slot0#.LevelBonusPoints.TheOffer.RideGoblin | Bonus points for "THE OFFER" / "Ride Goblin". |
| 514/202 | N/A | N/A | Six bytes long. |
| 520/208 | N32 | Slot0#.Baseline.Difficulty | Difficulty level ID. |
| 524/20C | N32 | Slot0#.Options.MovementToggles | Movement setting flags, or similar. |
| 528/210 | BOO | Slot0#.Options.TankControls | Toggle status for an alternative player character movement/rotation style. |
| 529/211 | N/A | N/A | Eleven bytes long. |
| 540/21C | N16 | Slot0#.Options.CameraMode | Setting for "CAMERA MODE": 0 is "PASSIVE" and 1 is "ACTIVE". |
| 542/21E | N16 | Slot0#.Options.ShowStylePoints | Toggle status for style points UI displays: 0 is disabled, 1 is enabled. |
| 544/220 | N/A | N/A | Two bytes long. |
| 546/222 | STR | Slot0#.Miscellaneous.UnknownString01 | Two characters long. Typically reads "HC". |
| 548/224 | N/A | N/A | Six bytes long. |
| 554/22A | BOO | Slot0#.Options.SwapJumpAndWebInputs | Toggle status for a feature that inverts the functions of the JUMP and WEB inputs. |
| 555/22B | N/A | N/A | One byte long. |
| 556/22C | BOO | Slot0#.Options.SwapZipAndSwingInputs | Toggle status for a feature that inverts the functions of the ZIP and SWING inputs. |
| 557/22D | N/A | N/A | One byte long. |
| 558/22E | BOO | Slot0#.Options.ControllerMovementTweak | Seems to attempt to change controller input (if present) so that the D-PAD is responsible for movement and the stick is responsible for all web combo moves. In my personal experience everything works except left/right D-PAD/character movement. |
| 559/22F | N/A | N/A | One byte long. |
| 560/230 | N32 | Slot0#.Options.InvertCameraLook | Setting for "INVERT CAMERA LOOK": 0 is "OFF" and 1 is "ON". |
| 564/234 | N32 | Slot0#.Options.ControllerVibration | Setting for "CONTROLLER VIBRATION" - 0 is "OFF" and 1 is "ON". |
| 568/238 | N/A | N/A | Eight bytes long. |
| 576/240 | STR | Slot0#.Miscellaneous.UnknownString02 | Eight characters long. Typically reads "fakehero". |
| 584/248 | N/A | N/A | Eight bytes long. |

### Chunk 9: Footer
- NOTE: Though this data is written every time by the game, it doesn't appear to be used/displayed anywhere. However, these values are validated and erroneous data marks the whole save file as empty.

| Offset (d/h) | Type | JSON Variable | Information |
| ------------ | ---- | ------------- | ----------- |
| 0/0 | N/A | N/A | Sixteen bytes long. |
| 16/10 | N16 | General.LastSaveSlot | Last save slot saved to (0 = slot 1, 7 = slot 8). |
| 18/12 | N/A | N/A | Two bytes long. |
| 20/14 | N16 | General.LastSaveYear | Year upon last save (2024 = 2024). |
| 22/16 | N16 | General.LastSaveMonth | Month upon last save (1 = January, 12 = December). |
| 24/18 | N16 | General.LastSaveWeekday | Weekday upon last save (0 = Sunday, 7 = Saturday). |
| 26/1A | N16 | General.LastSaveDay | Day upon last save (1-31 range typically). |
| 28/1C | N16 | General.LastSaveHour | Hour upon last save (0 = 00:##:##). |
| 30/1E | N16 | General.LastSaveMinute | Minute upon last save (0 = ##:00:##). |
| 32/20 | N16 | General.LastSaveSecond | Second upon last save (0 = ##:##:00). |
| 34/22 | N/A | N/A | Six bytes long. |

## Supporting information


### Known signatures
| Signature (ASCII) | Version |
| ----------------- | ------- |
| 13:56:03 | WINDOWS/1.0 |
| 09:18:13 | WINDOWS/1.3 |

### Difficulty IDs
| ID | Difficulty |
| -- | ---------- |
| 0 | UNKNOWN - Whilst active, attempting to start a new game automatically highlights SUPER HERO difficulty, however gameplay (with regards to damage intake/output and tutorial/pickup presence) reflects or is more lenient than EASY difficulty. Some levels adapt further than others, and a few are broken/incompletable. |
| 1 | EASY |
| 2 | NORMAL |
| 3 | HERO |
| 4 | SUPER HERO |

### Difficulty-specific unlock levels
A separate "unlock level" is stored for each of the five difficulty levels. This value is equal to that of the level ID for the furthest level in the game reached on that difficulty on that save file, and is used to determine what progression (not Secret Points)-based things to unlock. All unlock levels are allowed to affect the unlocked items in the Gallery and Secret Store, but only the unlock level matching the difficulty of the save file is allowed to affect the unlocked Level Warp scope.

Five separate counts are maintained so that the "don't reset Bonus Points/Gallery on new game" feature is able to function.

With regards to Gallery and Secret Store unlocks cross-unlock levels in a single save slot, the game takes a summary-based approach; if at least one unlock level is high enough to indicate that a thing should be unlocked, then that thing will be unlocked, even if other unlock levels contradict this.

### Level IDs
| ID | Level |
| -- | ----- |
| 1 | SEARCH FOR JUSTICE |
| 2 | WAREHOUSE HUNT |
| 3 | BIRTH OF A HERO |
| 4 | OSCORP'S GAMBIT |
| 5 | THE SUBWAY STATION |
| 6 | CHASE THROUGH THE SEWER |
| 7 | SHOWDOWN WITH SHOCKER |
| 8 | VULTURE'S LAIR |
| 9 | VULTURE ESCAPES |
| 10 | AIR DUEL WITH VULTURE |
| 11 | CORRALLED |
| 12 | SCORPION'S RAMPAGE |
| 13 | COUP D'ETAT |
| 14 | THE OFFER |
| 15 | RACE AGAINST TIME |
| 16 | KRAVEN'S TEST (see NOTE) |
| 17 | THE MIGHTY HUNTER (see NOTE) |
| 18 | THE RAZOR'S EDGE |
| 19 | BREAKING AND ENTERING |
| 20 | CHEMICAL CHAOS |
| 21 | OSCORP'S ULTIMATE WEAPON |
| 22 | ESCAPE FROM OSCORP |
| 23 | MARY JANE KIDNAPPED |
| 24 | FACE-OFF AT THE BRIDGE |
| 25 | CONCLUSION |

* NOTE: Levels "KRAVEN'S TEST" and "THE MIGHTY HUNTER" are not implemented in non-Xbox console versions of the game. On Windows, setting either as a save slot's continue level shows the correct save icon/name, however the former leads to THE RAZOR'S EDGE and the latter crashes. Setting either as the difficulty unlock/Level Warp level makes the scrolling on the Level Warp selection behave oddly.

### Unknown bonuses
There are twenty unknown bonus scores scattered in-between the known ones. These bonuses *do* also contribute to the total Secret Points count (relevant to and viewable in the Secret Store), but don't appear under any specific level/bonus listing. It is possible these slots were intended/allocated to hold bonuses that were removed before the game was finalised.

## JSON-exclusive variables
The JSON representation's "Meta" structure is designated as the holding spot for various metadata - things added/verified by SAVBasics but not directly copied over from the SAV file.

| JSON Variable | Information |
| ------------- | ----------- |
| Meta.DataType | This should always be "Spider-Man (2002/Windows) save data as handled by SM-SAVBasics". If it isn't, JSON to SAV conversion will be refused. |
| Meta.DataForm | A digit representing the version of the SAVBasics JSON export format in use for the given file. There's currently only one (1), but if the format is ever updated in a way where the JSON output needs to change, this value will increment. Unrecognised values will be refused in JSON to SAV conversion. |
| Meta.SignatureMatch | On SAV to JSON conversion, if the save data signature matches a known one, the relevant signature's attached game version string will be set here, otherwise this will read "N/A". Added only for convenience at the moment, is not handled at all on JSON to SAV conversion. |

## JSON representation quirks
Some of the SAV file data isn't fully understood by me yet (or is odd to handle currently), and hence is handled/JSON-exported as a raw digit value (or a series of raw digit values) by SAVBasics. This data can technically be edited and re-imported to SAV, but results will vary, and the optimal values (if any) will seem odd. Relevant data currently includes:
- Text strings in ASCII (currently exported as an array of integers that make up the encoded ASCII string).
- Secret Store/movement flag carriers (each is represented numerically, exact functionality is not currently understood).
- Volume levels and TRAINING level best times (currently all represented as numbers, the exact transformation from numeric value to in-game use is not currently understood).

Additionally, JSON exports retain some of the potentially interesting data type/range usage from the original SAV file structure:

- Some settings are effectively boolean values to the game but are stored and handled as numeric values anyway.
- The footer's "last slot saved" value is zero-based.
- The footer's "weekday upon last save" value (1-7) indexes from Sunday to Saturday (so Wednesday would be 4, for example).  
  
----------  
  
