from common.consts import checkFlVersion, MIN_FL_VERSION, formatVersion
import ui


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
