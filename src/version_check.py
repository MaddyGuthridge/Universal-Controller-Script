from common.consts import checkFlVersion, MIN_FL_VERSION, formatVersion
import ui


def versionCheck():
    try:
        # If we can import fl_model, that means we're running outside of FL
        # Studio - don't block the version check
        import fl_model
        del fl_model
        return
    except ImportError:
        pass
    if not checkFlVersion():
        print()
        print("CRITICAL ERROR!")
        print("=" * 30)
        print()
        print(f"Your version of FL Studio ({ui.getVersion()}) is too low")
        print(f"Please update to FL Studio >= {formatVersion(MIN_FL_VERSION)}")
        print()
        print()

        raise Exception("Script load cancelled")


versionCheck()
