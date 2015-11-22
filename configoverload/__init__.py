try:
    from .version import version as __version__
except ImportError:
    __version__ = None

from configloverloader import (glob,
                               globfp,
                               register_default_context,
                               get_default_context,
                               )
