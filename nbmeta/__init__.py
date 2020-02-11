#!/usr/bin/env python
"""
nbmeta
-------
Top-level package for nbmeta.

* Src: https://github.com/westurner/nbmeta
"""
__author__ = """Wes Turner"""
__email__ = 'wes@wrd.nu'
__version__ = '0.1.0'


from .utils import (
    DisplayConfig,
    EmitConfig,

    get_store,
    emit

)

# from nodes import (
#     'Meta',

__ALL__ = ['utils',
           'DisplayConfig',
           'EmitConfig',
           'get_store',
           'emit']
