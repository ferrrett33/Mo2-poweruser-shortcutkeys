import mobase

from .poweruser_shortcutkeys import PowerUserShortcutKeys  # Always use relative import:

def createPlugin() -> mobase.IPlugin:

    return PowerUserShortcutKeys()
