# SPDX-License-Identifier: MIT

"""An API Wrapper for rustmaps.com written in Python."""

import logging
from typing import Final

from .client import *
from .errors import *
from .http import *

__version__: Final[str] = "0.1.0"
__author__: Final[str] = "OseSem"
__license__: Final[str] = "MIT"
__title__: Final[str] = "rustmaps.py"

logging.getLogger(__name__).addHandler(logging.NullHandler())
