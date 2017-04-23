#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
nbmeta.interfaces
------------------

"""


class IReprHTML:
    def _repr_html_(self):
        """Return HTML as a unicode string

        Returns:
            unicode: HTML string
        """
        raise NotImplementedError()


