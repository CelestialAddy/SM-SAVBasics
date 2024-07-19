# PROJECT: SM-SAVBasics
# SPECIFY: Modules/StatusUpdate.py
# STARTED: 2024.July by CelestialAddy
# ===================================================================================================

def Signal(Text, RequireUserPressENTER):
    '''If RequireUserPressENTER is False, calls print(Text).
    If RequireUserPressENTER is True, calls input(Text).
    In error, returns None.'''
    # This will be given Opts["UI"] from the CLI/CON interface scripts.
    # That way, in CLI mode, errors are stated and no intervention is required.
    # (But users using CON mode will still need to decline errors before the CON exits suddenly.)
    try:
        if RequireUserPressENTER == False:
            print(Text)
        elif RequireUserPressENTER == True:
            input(Text)
        else:
            pass
    except:
        return None

# ===================================================================================================
# NOTHING: Beyond this point.
