# coding: utf-8
from __future__ import print_function, unicode_literals
import sys

if sys.version.startswith('2.'):
    class FileNotFoundError(RuntimeError):
        def __init__(self, msg):
            self.message = 'FileNotFoundError: {}'.format(msg)
