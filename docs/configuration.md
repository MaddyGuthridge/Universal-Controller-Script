
# Script Configuration

The script contains many options that can be customized to make it work the way
you want it to.

## Setup

In order for settings to be persisted when the script is updated, a small
amount of setup is required.

1. Navigate to the installation location for the script in your file manager.
   It can be found at `~/Documents/Image-Line/FL Studio/Settings/Hardware`.

2. Copy the `ucs_config` folder from within your `UniversalController` folder
   to the `Hardware` folder.

3. Inside the `ucs_config` folder, edit `config.py` as necessary.

## Configuration Options

The script is configured using a default configuration, and a user
configuration. Both configurations are loaded, then changes in the user
configuration are used to override the defaults. Note that if an invalid key
is given, the script will give an error and will fail to function. Make sure to
open the script output window (view > script output) after modifying your
settings.

The configuration is stored as a nested set of Python dictionaries, which can
be used much like JSON. One key difference is that dots can be used within a
key in order to specify depth. This means that `"deeply.nested.key": 42`
will result in the following structure:
```py
{
    "deeply": {
        "nested": {
            "key": 42
        },
    },
}
```

For full details and documentation of the available settings, refer the default
configuration, which can be found within `common/default_config.py`.
