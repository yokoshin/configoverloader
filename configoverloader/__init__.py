try:
    from .version import version as __version__
except ImportError:
    __version__ = None

from configoverloader import (get_filenames,
                              register_context,
                              get_context,
                               )
