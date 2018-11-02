#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

from . import version
from .compat import (urlquote, urlunquote, urlparse, to_bytes, to_string, to_unicode)

__author__ = 'Rayvision'
__version__ = version.__version__

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())