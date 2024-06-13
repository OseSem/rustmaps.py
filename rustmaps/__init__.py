# SPDX-License-Identifier: MIT

"""An API Wrapper for rustmaps.com written in Python."""

import logging

from .client import *
from .errors import *
from .http import *

__version__ = "0.1.0"
__author__ = "OseSem"
__license__ = "MIT"
__title__ = "rustmaps.py"

logging.getLogger(__name__).addHandler(logging.NullHandler())
